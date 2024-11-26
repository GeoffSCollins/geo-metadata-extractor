from bs4 import BeautifulSoup
from typing import List, Iterable, Optional

from extract.GeoSeries import GeoSeries
from extract.GeoPlatform import GeoPlatform
from extract.GeoSample import GeoSample


class GeoMetadataExtractor:
    miniml_file_location: str
    series: List[GeoSeries]
    platforms: List[GeoPlatform]
    samples: List[GeoSample]

    extraction_successful: bool
    extraction_error: Optional[str] = None

    _print_to_console: bool

    def __init__(self, miniml_file_location: str, print_to_console: bool = False):
        self.miniml_file_location = miniml_file_location
        self._print_to_console = print_to_console
        self.extraction_successful = self._extract_geo_metadata()


    def _extract_geo_metadata(self) -> bool:
        try:
            with open(self.miniml_file_location, 'r', encoding='utf-8') as file:
                xml_data = file.read()
        except FileNotFoundError as e:
            self.extraction_error = str(e)
            return False
        except UnicodeDecodeError as e:
            self.extraction_error = str(e)
            return False

        soup = BeautifulSoup(xml_data, 'xml')

        series_dict = self._extract_xml_data(
            soup=soup,
            extraction_key='Series',
            log_file_location='logs/extract_platform.log',
            print_to_console=self._print_to_console
        )

        self.series = [GeoSeries(x) for x in series_dict]

        platform_dict = self._extract_xml_data(
            soup=soup,
            extraction_key='Platform',
            log_file_location='logs/extract_platform.log',
            print_to_console=self._print_to_console
        )

        self.platforms = [GeoPlatform(x) for x in platform_dict]

        samples_dict = self._extract_xml_data(
            soup=soup,
            extraction_key='Sample',
            log_file_location='logs/extract_samples.log',
            print_to_console=self._print_to_console
        )

        self.samples = [GeoSample(x) for x in samples_dict]
        return True

    def _warn_if_additionally_nested_data(
        self,
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


    def _convert_soup_to_dict(self, soup: BeautifulSoup, nodes_to_skip: Iterable[str] = tuple()) -> dict:
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

    def _remove_data_tables(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Removes all elements labeled "Data-Table" within the parsed XML of the BeautifulSoup object

        :param soup: The BeautifulSoup object containing the parsed xml
        :return:The cleaned BeautifulSoup object without the Data-Table nodes
        """
        for data_table in soup.find_all('Data-Table'):
            data_table.decompose()

        return soup

    def _reformat_status(self, soup: BeautifulSoup, data: dict) -> dict:
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


    def _extract_xml_data(
        self,
        soup: BeautifulSoup,
        extraction_key: str,
        log_file_location: str,
        print_to_console: bool = False
    ) -> List[dict]:
        """
        Extracts a list of dictionary objects for the platform section of the MINiML file

        :param soup: The BeautifulSoup object created from the XML file
        :param extraction_key: The name of the XML element to parse
        :param log_file_location: The path to the log file for the platform extraction step
        :param print_to_console: If true, also outputs the warnings to stdout using the print statement
        :return: A list of dictionaries
        """
        # remove any data tables
        soup = self._remove_data_tables(soup)

        # Extract the data from the given extraction key
        extracted_soup = soup.find_all(extraction_key)

        data = []

        for child_node in extracted_soup:
            self._warn_if_additionally_nested_data(
                soup=child_node,
                log_file_location=log_file_location,
                expected_non_terminal_node_names=['Status'],
                print_to_console=print_to_console
            )

            child_data = self._convert_soup_to_dict(child_node, nodes_to_skip=['Status'])
            child_data = self._reformat_status(child_node, child_data)
            data.append(child_data)

        return data

