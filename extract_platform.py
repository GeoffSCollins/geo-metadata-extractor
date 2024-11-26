from bs4 import BeautifulSoup

from utils import (
    _warn_if_additionally_nested_data,
    _convert_soup_to_dict,
    _remove_data_tables,
    _reformat_status
)

def extract_platform_data(
    miniml_file_location: str,
    log_file_location: str = 'extract_platform.log',
    print_to_console: bool = False
) -> dict:
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

    # convert the platform data to a dictionary
    platform_data = _convert_soup_to_dict(platform, nodes_to_skip=['Status'])

    # extract the status nested data into a separate part of the JSON
    platform_data = _reformat_status(platform, platform_data)

    return platform_data


if __name__ == '__main__':
    x = []

    for i in range(1, 10):
        input_file = f"GSE{i}_family.xml"

        platform_data = extract_platform_data(input_file)

        x.append(platform_data)

    # Just some temp code for understanding which keys are always present

    # from collections import Counter
    #
    # # Initialize a Counter to count the occurrences of keys
    # key_counter = Counter()
    #
    # # Iterate through each dictionary in the list
    # for dictionary in x:
    #     # Update the counter with the keys of the current dictionary
    #     key_counter.update(dictionary.keys())
    #
    # # Print the key counts
    # for key, count in key_counter.items():
    #     print(f"Key: {key}, Count: {count}")
