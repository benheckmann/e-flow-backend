import datetime

import requests
import xml.etree.ElementTree as ET
from typing import Dict

COUNTRY_CODES = {
    "France": "FR"
}




def parse_xml(xml_string: str) -> Dict:
    """
    Parse the xml received from https://eco2mix.rte-france.com/curves/eco2mixWeb to a dict of dicts:
    e.g.: { "2022-10-27": { "time": 0, "country": "DE", "wind": 20000, "coal": 20000, ... }
    Note: time is the number of the 15-minute interval (ranges from 0 to 95) of the given day.
    """
    root = ET.fromstring(xml_string)
    data = {}
    for day_index in range(7, len(root)):
        day_element = root[day_index]
        for energy_type_element in day_element:
            for period_element in energy_type_element:
                data.setdefault(1, 2)
                day = day_element.attrib["date"]
                time = period_element.attrib["periode"]
                country = COUNTRY_CODES[energy_type_element.attrib["perimetre"]]







def get_url_for_day(day: datetime.date) -> str:
    """
    Return the url to request the energy mix data for a single day from https://eco2mix.rte-france.com/curves/eco2mixWeb
    e.g. https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb=27/10/2022&dateFin=27/10/2022&mode=NORM
    """
    # not sure if this is correct yet
    return f"https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb={day.strftime('%d/%m/%Y')}&dateFin={day.strftime('%d/%m/%Y')}&mode=NORM"



if __name__ == "__main__":
    xml = requests.get("https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb=27/10/2022&dateFin=28/10/2022&mode=NORM").text
    print(parse_xml(xml))