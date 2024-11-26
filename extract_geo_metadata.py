from extract.extract_platform import extract_platform_data
from extract.extract_samples import extract_samples_data
from extract.extract_series import extract_series_data


def extract_geo_metadata(miniml_file_location: str, print_to_console: bool = False) -> dict:
    d = {
        "series": extract_series_data(miniml_file_location, print_to_console=print_to_console),
        "platform": extract_platform_data(miniml_file_location, print_to_console=print_to_console),
        "samples": extract_samples_data(miniml_file_location, print_to_console=print_to_console)
    }

    return d
