from bs4 import BeautifulSoup

from utils.utils import (
    _warn_if_additionally_nested_data,
    _convert_soup_to_dict,
    _remove_data_tables,
    _reformat_status
)

def extract_platform_data(
    miniml_file_location: str,
    log_file_location: str = 'logs/extract_platform.log',
    print_to_console: bool = False
) -> dict:
    """
    Extracts a dictionary object for the platform section of the MINiML file

    :param miniml_file_location: The path to the MINiML file
    :param log_file_location: The path to the log file for the platform extraction step
    :param print_to_console: If true, also outputs the warnings to stdout using the print statement
    :return: A dictionary
    """
    with open(miniml_file_location, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    soup = BeautifulSoup(xml_data, 'xml')

    # remove any data tables
    soup = _remove_data_tables(soup)

    # Extract the Platform data
    platform = soup.find_all('Platform')[0]

    _warn_if_additionally_nested_data(
        soup=platform,
        log_file_location=log_file_location,
        expected_non_terminal_node_names=['Status'],
        print_to_console=print_to_console
    )

    platform_data = _convert_soup_to_dict(platform, nodes_to_skip=['Status'])
    platform_data = _reformat_status(platform, platform_data)

    return platform_data
