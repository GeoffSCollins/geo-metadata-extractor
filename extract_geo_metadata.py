from extract_platform import extract_platform_data
from extract_samples import extract_samples_data
from extract_series import extract_series_data


def extract_geo_metadata(miniml_file_location: str, print_to_console: bool = False) -> dict:
    d = {
        "series": extract_series_data(miniml_file_location, print_to_console=print_to_console),
        "platform": extract_platform_data(miniml_file_location, print_to_console=print_to_console),
        "samples": extract_samples_data(miniml_file_location, print_to_console=print_to_console)
    }

    return d


if __name__ == '__main__':
    x = []

    for i in range(1, 10):
        input_file = f"GSE{i}_family.xml"

        sample_data = extract_geo_metadata(input_file)

        x.append(sample_data)

    import json
    with open('out.json', 'w') as file:
        json.dump(x[-1], file, indent=4)
