import psycopg2

from extract_geo_metadata import extract_geo_metadata
from load_geo_metadata import load_series

if __name__ == '__main__':
    conn = psycopg2.connect("postgresql://postgres:password@localhost:5432/postgres")

    for i in range(1, 10):
        input_file = f"xml_files/GSE{i}_family.xml"

        geo_metadata = extract_geo_metadata(input_file)
        series = geo_metadata['series']

        load_series(conn, series)

    conn.commit()