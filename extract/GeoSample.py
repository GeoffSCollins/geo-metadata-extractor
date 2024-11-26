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