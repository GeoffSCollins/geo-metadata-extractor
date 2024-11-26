import json

from typing import List

from extract.GeoPlatform import GeoPlatform
from extract.GeoSample import GeoSample
from extract.GeoSeries import GeoSeries


def load_series(conn, miniml_file_id: int, series: List[GeoSeries]) -> int:
    """
    Loads data into the series table

    :param conn: The database connection
    :param miniml_file_id: The miniml file record identifier
    :param series: A list of series objects
    :return: The ID of the series record inserted in the database
    """
    series_ids = []

    with conn.cursor() as cursor:
        for ser in series:
            cursor.execute(
                """
                INSERT INTO series (
                    miniml_file_id,
                    title,
                    accession,
                    pubmed_id,
                    summary,
                    type,
                    submission_date,
                    release_date,
                    last_update_date,
                    additional_metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    miniml_file_id,
                    ser.title,
                    ser.accession,
                    ser.pubmed_id,
                    ser.summary,
                    ser.type,
                    ser.submission_date,
                    ser.release_date,
                    ser.last_updated_date,
                    json.dumps(ser.additional_metadata)
                )
            )

            series_ids.append(
                int(cursor.fetchone()[0])
            )

        return series_ids[0]


def load_platforms(conn, platforms: List[GeoPlatform], series_id: int) -> None:
    """
    Loads data into the platform table

    :param conn: The database connection
    :param platforms: A list of platform objects
    """
    data = [
        (
            series_id,
            platform.title,
            platform.accession,
            platform.technology,
            platform.distribution,
            platform.organism,
            platform.description,
            platform.submission_date,
            platform.release_date,
            platform.last_updated_date,
            json.dumps(platform.additional_metadata)
        )
        for platform in platforms
    ]

    with conn.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO platform (
                series_id,
                title,
                accession,
                technology,
                distribution,
                organism,
                description,
                submission_date,
                release_date,
                last_update_date,
                additional_metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            data
        )


def load_samples(conn, samples: List[GeoSample], series_id) -> None:
    """
    Loads data into the sample table

    :param conn: The database connection
    :param samples: A list of sample objects
    """
    data = [
        (
            series_id,
            sample.title,
            sample.accession,
            sample.type,
            sample.description,
            sample.submission_date,
            sample.release_date,
            sample.last_updated_date,
            json.dumps(sample.additional_metadata)
        )
        for sample in samples
    ]

    with conn.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO sample (
                series_id,
                title,
                accession,
                type,
                description,
                submission_date,
                release_date,
                last_update_date,
                additional_metadata
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            data
        )
