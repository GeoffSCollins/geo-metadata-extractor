import psycopg2
import time
import glob

from download.download_geo_metadata import GeoMetadataDownloader
from extract.GeoMetadataExtractor import GeoMetadataExtractor
from load_geo_metadata import load_series, load_platforms, load_samples


def load_miniml_file(conn: psycopg2._psycopg.connection, miniml_file_location: str):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO miniml_file (path)
            VALUES (%s)
            RETURNING id
            """,
            (miniml_file_location,)
        )

        return cursor.fetchone()[0]


def load_extraction_failure(conn: psycopg2._psycopg.connection, miniml_file_id: int, error_message: str) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO extraction_failure (
                miniml_file_id,
                error_message
            )
            VALUES (%s, %s)
            """,
            (
                miniml_file_id,
                error_message
            )
        )


if __name__ == '__main__':
    conn = psycopg2.connect("postgresql://postgres:password@localhost:5432/postgres")

    start = 1
    end = 1000
    batch_size = 150
    output_directory = "xml_files"

    start_time = time.time()

    GeoMetadataDownloader(
        output_directory="xml_files",
        start_gse_id=start,
        end_gse_id=end,
        batch_size=batch_size
    ).download_all()

    end_time = time.time()
    print(f"Time taken to download {end - start} MINiML files: {end_time - start_time} seconds")

    for miniml_file_location in glob.glob(output_directory + "/*family.xml"):
        geo_metadata_extractor = GeoMetadataExtractor(
            miniml_file_location=miniml_file_location,
            print_to_console=False
        )

        miniml_file_id = load_miniml_file(conn, geo_metadata_extractor.miniml_file_location)

        if not geo_metadata_extractor.extraction_successful:
            load_extraction_failure(conn, miniml_file_id, geo_metadata_extractor.extraction_error)
            continue

        series_id = load_series(conn, miniml_file_id, geo_metadata_extractor.series)
        load_platforms(conn, geo_metadata_extractor.platforms, series_id)
        load_samples(conn, geo_metadata_extractor.samples, series_id)

    conn.commit()