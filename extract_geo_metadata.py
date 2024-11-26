from bs4 import BeautifulSoup
from typing import List, Optional

from extract.generic_extractor import extract_xml_data


class GeoSeries:
    series_dict: dict

    title: str
    accession: str
    pubmed_id: Optional[str]
    summary: str
    type: str
    submission_date: str
    release_date: str
    last_updated_date: str

    additional_metadata: dict

    def __init__(self, series_dict: dict):
        self.series_dict = series_dict

        self.title = series_dict['Title']
        self.accession = series_dict['Accession']
        self.pubmed_id = series_dict.get('Pubmed-ID')
        self.summary = series_dict['Summary']
        self.type = series_dict['Type']
        self.submission_date = series_dict['Status']['Submission-Date']
        self.release_date = series_dict['Status']['Release-Date']
        self.last_updated_date = series_dict['Status']['Last-Update-Date']

        self.additional_metadata = {
            key: value
            for key, value in series_dict.items()
            if key not in {
                'Title',
                'Accession',
                'Pubmed-ID',
                'Summary',
                'Type',
                'Status'
            }
        }


class GeoPlatform:
    platform_dict: dict

    title: str
    accession: str
    technology: str
    distribution: str
    organism: str
    description: str
    submission_date: str
    release_date: str
    last_updated_date: str

    additional_metadata: dict

    def __init__(self, platform_dict: dict):
        self.platform_dict = platform_dict

        self.title = platform_dict['Title']
        self.accession = platform_dict['Accession']
        self.technology = platform_dict['Technology']
        self.distribution = platform_dict['Distribution']
        self.organism = platform_dict['Organism']
        self.description = platform_dict['Description']
        self.submission_date = platform_dict['Status']['Submission-Date']
        self.release_date = platform_dict['Status']['Release-Date']
        self.last_updated_date = platform_dict['Status']['Last-Update-Date']

        self.additional_metadata = {
            key: value
            for key, value in platform_dict.items()
            if key not in {
                'Title',
                'Accession',
                'Technology',
                'Distribution',
                'Organism',
                'Description',
                'Status'
            }
        }


class GeoSample:
    sample_dict: dict

    title: str
    accession: str
    type: str
    description: str
    submission_date: str
    release_date: str
    last_updated_date: str

    additional_metadata: dict

    def __init__(self, sample_dict: dict):
        self.sample_dict = sample_dict

        self.title = sample_dict['Title']
        self.accession = sample_dict['Accession']
        self.type = sample_dict['Type']
        self.description = sample_dict['Description']
        self.submission_date = sample_dict['Status']['Submission-Date']
        self.release_date = sample_dict['Status']['Release-Date']
        self.last_updated_date = sample_dict['Status']['Last-Update-Date']

        self.additional_metadata = {
            key: value
            for key, value in sample_dict.items()
            if key not in {
                'Title',
                'Accession',
                'Type',
                'Description',
                'Status'
            }
        }


class GeoMetadataExtractor:
    gse_id: int
    miniml_file_location: str
    series: List[GeoSeries]
    platforms: List[GeoPlatform]
    samples: List[GeoSample]

    _print_to_console: bool

    def __init__(self, gse_id: int, miniml_file_location: str, print_to_console: bool = False):
        self.gse_id = gse_id
        self.miniml_file_location = miniml_file_location
        self._print_to_console = print_to_console
        self._extract_geo_metadata()


    def _extract_geo_metadata(self) -> None:
        with open(self.miniml_file_location, 'r', encoding='utf-8') as file:
            xml_data = file.read()

        soup = BeautifulSoup(xml_data, 'xml')

        series_dict = extract_xml_data(
            soup=soup,
            extraction_key='Series',
            log_file_location='logs/extract_platform.log',
            print_to_console=self._print_to_console
        )

        self.series = [GeoSeries(x) for x in series_dict]

        platform_dict = extract_xml_data(
            soup=soup,
            extraction_key='Platform',
            log_file_location='logs/extract_platform.log',
            print_to_console=self._print_to_console
        )

        self.platforms = [GeoPlatform(x) for x in platform_dict]

        samples_dict = extract_xml_data(
            soup=soup,
            extraction_key='Sample',
            log_file_location='logs/extract_samples.log',
            print_to_console=self._print_to_console
        )

        self.samples = [GeoSample(x) for x in samples_dict]
