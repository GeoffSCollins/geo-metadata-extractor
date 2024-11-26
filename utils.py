from bs4 import BeautifulSoup
from typing import Iterable

def _warn_if_additionally_nested_data(
    soup: BeautifulSoup,
    log_file_location: str,
    expected_non_terminal_node_names: Iterable[str] = tuple(),
    print_to_console: bool = False
) -> None:
    with open(log_file_location, 'a') as file:
        for child in soup.children:
            if isinstance(child, str):
                continue

            if child.name in expected_non_terminal_node_names:
                continue

            if len(child.find_all()) > 0:
                file.write(f"Additional nesting found in {child.name}\n")

                if print_to_console:
                    print(f"Additional nesting found in {child.name}")


def _convert_soup_to_dict(soup: BeautifulSoup, nodes_to_skip: Iterable[str] = tuple()) -> dict:
    # Create a dictionary to hold the key-value pairs.
    data = {}

    for child in soup.find_all(recursive=False):
        if child.name in nodes_to_skip:
            continue

        # Use the tag name as the key and the text as the value.
        data[child.name] = child.text.strip()

    return data


def _remove_data_tables(soup: BeautifulSoup):
    for data_table in soup.find_all('Data-Table'):
        data_table.decompose()

    return soup


def _reformat_status(soup: BeautifulSoup, data: dict) -> dict:
    data['Status'] = {}
    status = soup.find_all('Status')[0]

    for child in status.find_all():
        data['Status'][child.name] = child.text.strip()

    return data
