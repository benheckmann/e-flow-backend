import datetime
from typing import Dict

import xml.etree.ElementTree as ET
import requests as requests

from energy_mix_parser import parse_xml, get_url_for_day, get_unix_timestamp, ENERGY_TYPES


def parse_latest_timepoint(day: datetime.date) -> Dict:
    """
    Parse the latest timepoint from the energy mix data for a single day.
    Note: Country will be hardcoded to FR for now.
    """
    url = get_url_for_day(day)
    xml_string = requests.get(url).text
    root = ET.fromstring(xml_string)
    day_element = root[7]
    result = {
        "time": get_unix_timestamp(day_element.attrib["date"], len(day_element[0])),
        "country": "FR"
    }
    for energy_type_element in day_element:
        for period_element in energy_type_element:
            energy_type = ENERGY_TYPES[energy_type_element.attrib["v"]]
            try:
                value = int(period_element.text)
            except ValueError:
                value = 0
            energy_sum = result.get(energy_type, 0)
            energy_sum += value
            result[energy_type] = energy_sum
    return result


if __name__ == "__main__":
    print(parse_latest_timepoint(datetime.date.today()))
