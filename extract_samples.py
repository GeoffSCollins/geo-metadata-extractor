from bs4 import BeautifulSoup
from typing import List

from utils import (
    _warn_if_additionally_nested_data,
    _remove_data_tables,
    _convert_soup_to_dict,
    _reformat_status
)


def extract_samples_data(
    miniml_file_location: str,
    log_file_location: str = 'extract_samples.log',
    print_to_console: bool = False
) -> List[dict]:
    with open(miniml_file_location, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    soup = BeautifulSoup(xml_data, 'xml')

    # remove any data tables
    soup = _remove_data_tables(soup)

    # Extract the Platform data
    samples = soup.find_all('Sample')
    samples_data = []

    for sample in samples:
        _warn_if_additionally_nested_data(
            soup=sample,
            log_file_location=log_file_location,
            expected_non_terminal_node_names=["Status"],
            print_to_console=print_to_console
        )

        sample_data =_convert_soup_to_dict(sample, nodes_to_skip=['Status'])

        sample_data = _reformat_status(sample, sample_data)

        samples_data.append(sample_data)

    return samples_data
