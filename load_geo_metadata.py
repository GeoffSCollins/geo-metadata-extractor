

def load_series(conn, series: dict) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO series (title, accession, pubmed_id, summary, type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                series['Title'],
                series['Accession'],
                series.get('Pubmed-ID'),
                series['Summary'],
                series['Type']
            )
        )

        cursor.execute("SELECT * FROM series")

        print(cursor.rowcount)
