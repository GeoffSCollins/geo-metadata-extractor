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