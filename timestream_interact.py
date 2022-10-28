from sqlite3 import DatabaseError
from const import *
import boto3
from botocore.config import Config

def database_info(client):
  print(f"getting db info for {DATABASE_NAME}")
  result = client.describe_database(DatabaseName=DATABASE_NAME)
  print(result)


def main():
  print("Starting!")
  session = boto3.Session()
  print(session)
  client = session.client('timestream-write', config=Config(read_timeout=20, max_pool_connections=5000,
                                                            retries={'max_attempts': 10}))
  database_info(client)

if __name__ == '__main__':
  main()
