import psycopg2

from extract_geo_metadata import GeoMetadataExtractor
from load_geo_metadata import load_series, load_platforms, load_samples

if __name__ == '__main__':
    conn = psycopg2.connect("postgresql://postgres:password@localhost:5432/postgres")

    for i in range(1, 10):
        miniml_file_location = f"xml_files/GSE{i}_family.xml"

        geo_metadata_extractor = GeoMetadataExtractor(
            gse_id=i,
            miniml_file_location=miniml_file_location,
            print_to_console=False
        )

        series_id = load_series(conn, geo_metadata_extractor.series)
        load_platforms(conn, geo_metadata_extractor.platforms, series_id)
        load_samples(conn, geo_metadata_extractor.samples, series_id)

    conn.commit()