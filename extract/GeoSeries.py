from typing import Optional

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