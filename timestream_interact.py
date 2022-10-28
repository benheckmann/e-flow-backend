from const import *
import time
import boto3
from botocore.config import Config

def database_info(client):
  print(f"Getting db info for {DATABASE_NAME}")
  result = client.describe_database(DatabaseName=DATABASE_NAME)
  print(result)

def write_reading(client, reading):
  print(f"Writing reading {reading}")
  dimensions = [
    {'Name': 'Coal', 'Value': '101'},
    {'Name': 'Wind', 'Value': '102'},
    {'Name': 'Solar', 'Value': '103'},
    {'Name': 'Nuclear', 'Value': '104'},
    {'Name': 'Gas', 'Value': '10'},
  ]
  reading_time = reading['Time']
  print(reading_time)
  reading_dims = {'Time': reading_time} | {'Dimensions': dimensions, 'MeasureName': 'Country', 'MeasureValue': 'FR' ,'MeasureValueType': 'VARCHAR'}
  try:
    result = client.write_records(DatabaseName=DATABASE_NAME, TableName=TABLE_NAME,
                                      Records=[reading_dims], CommonAttributes={})
    print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
  except client.exceptions.RejectedRecordsException as err:
    print(f"Rejected: {err}")
    for rr in err.response["RejectedRecords"]:
      print("Rejected Index " + str(rr["RecordIndex"]) + ": " + rr["Reason"])
      if "ExistingVersion" in rr:
        print("Rejected record existing version: ", rr["ExistingVersion"])
  except Exception as err:
    print("Error:", err)

def run_query(client, query):
    try:
      result = client.query(QueryString=query)
      return (result['Rows'], result['ColumnInfo'])
    except Exception as err:
        print("Exception while running query:", err)

def get_readings(client):
  query = f'select * from "{DATABASE_NAME}"."{TABLE_NAME}"'
  return run_query(client, query)

def main():
  session = boto3.Session()
  clientWrite = session.client('timestream-write', config=Config(read_timeout=20, max_pool_connections=5000,
                                                              retries={'max_attempts': 10}))
  database_info(clientWrite)
  reading = {
    'Time': str(int(round(time.time() * 1000)))
  }
  write_reading(clientWrite, reading)

  clientRead = session.client('timestream-query', config=Config(read_timeout=20, max_pool_connections=5000,
                                                              retries={'max_attempts': 10}))
  (readings, columns) = get_readings(clientRead)

  for reading in readings:
    print(dict((column['Name'], data['ScalarValue']) for (data, column) in zip(reading['Data'], columns)))
    print()
  

if __name__ == '__main__':
  main()
