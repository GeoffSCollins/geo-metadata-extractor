from bs4 import BeautifulSoup

from utils.utils import (
    _warn_if_additionally_nested_data,
    _convert_soup_to_dict,
    _reformat_status
)


def extract_series_data(
    miniml_file_location: str,
    log_file_location: str = 'logs/series.log',
    print_to_console: bool = False
) -> dict:
    """
    Extracts a dictionary object for the series section of the MINiML file

    :param miniml_file_location: The path to the MINiML file
    :param log_file_location: The path to the log file for the series extraction step
    :param print_to_console: If true, also outputs the warnings to stdout using the print statement
    :return: A dictionary
    """
    with open(miniml_file_location, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    soup = BeautifulSoup(xml_data, 'xml')

    series = soup.find_all('Series')[0]

    _warn_if_additionally_nested_data(
        soup=series,
        log_file_location=log_file_location,
        expected_non_terminal_node_names=["Status"],
        print_to_console=print_to_console
    )

    series_data = _convert_soup_to_dict(series, nodes_to_skip=['Status'])
    series_data = _reformat_status(series, series_data)

    return series_data
