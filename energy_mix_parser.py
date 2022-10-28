import datetime

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List

ENERGY_TYPES = {
    "Nucléaire": "nuclear",
    "Charbon": "coal",
    "Gaz": "gas",
    "Fioul": "heavy-oil",
    "Pointe": "oil",
    "Fioul + Pointe": "oil",
    "Hydraulique": "hydro",
    "Eolien": "wind",
    "Solde": "others",
    "Autres": "others",
    "Pompage": "pumped-storage",  # negative (being stored)
    "Solaire": "solar",
    "Consommation": "consumption"
}


def get_unix_timestamp(date_str: str, period: int) -> int:
    """
    Convert a string of the form "2022-10-27" and an integer corresponding to the
    15-minute time interval to a unix timestamp.
    This function assumes does not consider time shifts and assumes the given time zone is utc.
    """
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return int((date + datetime.timedelta(minutes=period * 15)).timestamp())


def parse_xml_day(day_element: ET.Element) -> List[Dict]:
    """
    Note: will insert 0 if API says 'ND'
    """
    result = [
        {
            "time": get_unix_timestamp(day_element.attrib["date"], period),
            "country": "FR"
        }
        for period in range(len(day_element[0]))  # current length of the day
    ]
    for energy_type_element in day_element:
        for period_element in energy_type_element:
            energy_type = ENERGY_TYPES[energy_type_element.attrib["v"]]
            try:
                value = int(period_element.text)
            except ValueError:
                value = 0
            energy_sum = result[int(period_element.attrib["periode"])].get(energy_type, 0)
            energy_sum += value
            result[int(period_element.attrib["periode"])][energy_type] = energy_sum
    return result


def parse_xml(xml_string: str) -> List[Dict]:
    """
    Parse the xml received from https://eco2mix.rte-france.com/curves/eco2mixWeb to a dict of dicts:
    e.g.: [{ "time": 234987239847, "country": "FR", "wind": 20000, "coal": 20000, ... }]
    Note: Country will be hardcoded to FR for now.
    """
    root = ET.fromstring(xml_string)
    result = []
    for day_index in range(7, len(root)):
        day_element = root[day_index]
        result += parse_xml_day(day_element)
    return result


def get_url_for_day(day: datetime.date) -> str:
    """
    Return the url to request the energy mix data for a single day from https://eco2mix.rte-france.com/curves/eco2mixWeb
    e.g. https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb=27/10/2022&dateFin=27/10/2022&mode=NORM
    """
    return f"https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb={day.strftime('%d/%m/%Y')}&dateFin={day.strftime('%d/%m/%Y')}&mode=NORM"


if __name__ == "__main__":
    xml = requests.get(
        "https://eco2mix.rte-france.com/curves/eco2mixWeb?type=mix&dateDeb=27/10/2022&dateFin=28/10/2022&mode=NORM").text
    p = parse_xml(xml)
    print(p)
