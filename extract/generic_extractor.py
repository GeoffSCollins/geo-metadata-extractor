from bs4 import BeautifulSoup
from typing import List

from utils.utils import (
    _warn_if_additionally_nested_data,
    _convert_soup_to_dict,
    _remove_data_tables,
    _reformat_status
)

def extract_xml_data(
    soup: BeautifulSoup,
    extraction_key: str,
    log_file_location: str,
    print_to_console: bool = False
) -> List[dict]:
    """
    Extracts a list of dictionary objects for the platform section of the MINiML file

    :param miniml_file_location: The path to the MINiML file
    :param extraction_key: The name of the XML element to parse
    :param log_file_location: The path to the log file for the platform extraction step
    :param print_to_console: If true, also outputs the warnings to stdout using the print statement
    :return: A list of dictionaries
    """
    # remove any data tables
    soup = _remove_data_tables(soup)

    # Extract the data from the given extraction key
    extracted_soup = soup.find_all(extraction_key)

    data = []

    for child_node in extracted_soup:
        _warn_if_additionally_nested_data(
            soup=child_node,
            log_file_location=log_file_location,
            expected_non_terminal_node_names=['Status'],
            print_to_console=print_to_console
        )

        child_data = _convert_soup_to_dict(child_node, nodes_to_skip=['Status'])
        child_data = _reformat_status(child_node, child_data)
        data.append(child_data)

    return data
