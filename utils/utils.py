from bs4 import BeautifulSoup
from typing import Iterable

def _warn_if_additionally_nested_data(
    soup: BeautifulSoup,
    log_file_location: str,
    expected_non_terminal_node_names: Iterable[str] = tuple(),
    print_to_console: bool = False
) -> None:
    """
    Writes warnings of XML tag names with more than one level to the log file

    :param soup: The BeautifulSoup object containing the parsed xml
    :param log_file_location: The location of the log file to append to
    :param expected_non_terminal_node_names: A list of node names that will not be appended to the log file
    :param print_to_console: If true, also outputs the warnings to stdout using the print statement
    """
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
    """
    Converts the BeautifulSoup object to a dictionary of key value pairs.
    Note that this only goes one level deep (non recursive)

    :param soup: The BeautifulSoup object containing the parsed xml
    :param nodes_to_skip: Nodes to not include in the resulting dictionary
    :return: A dictionary with keys of the node name and values of the node string contents
    """
    data = {}

    for child in soup.find_all(recursive=False):
        if child.name in nodes_to_skip:
            continue

        # Only add the data if its not whitespace
        if child.text.strip():
            data[child.name] = child.text.strip()

    return data


def _remove_data_tables(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes all elements labeled "Data-Table" within the parsed XML of the BeautifulSoup object

    :param soup: The BeautifulSoup object containing the parsed xml
    :return:The cleaned BeautifulSoup object without the Data-Table nodes
    """
    for data_table in soup.find_all('Data-Table'):
        data_table.decompose()

    return soup


def _reformat_status(soup: BeautifulSoup, data: dict) -> dict:
    """
    Adds the Status to the data dictionary

    :param soup: The BeautifulSoup object containing the parsed xml
    :param data: The dictionary of key value pairs previously parsed using _convert_soup_to_dict()
    :return: The data dictionary with a key of "Status" and the child node contents within that object
    """
    data['Status'] = {}
    status = soup.find_all('Status')[0]

    for child in status.find_all():
        data['Status'][child.name] = child.text.strip()

    return data
