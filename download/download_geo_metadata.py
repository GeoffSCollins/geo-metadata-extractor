import os
import shutil

import requests
import tarfile
import threading
import psycopg2

from typing import Optional

class DownloadAttempt:
    gse_id: str
    url: str
    local_path: str
    success: bool
    error_message: Optional[str]

    def __init__(self, gse_id: str, url: str, local_path: str, success: bool, error_message: Optional[str]):
        self.gse_id = gse_id
        self.url = url
        self.local_path = local_path
        self.success = success
        self.error_message = error_message


class GeoMetadataDownloader:
    conn: psycopg2._psycopg.connection
    MAX_BATCH_SIZE = 150

    _output_directory: str
    _start_gse_id: int
    _end_gse_id: int
    _batch_size: int

    def __init__(self, output_directory: str, start_gse_id: int, end_gse_id: int, batch_size: int):
        self._output_directory = output_directory
        self._start_gse_id = start_gse_id
        self._end_gse_id = end_gse_id
        self._batch_size = batch_size

        self.conn = psycopg2.connect("postgresql://postgres:password@localhost:5432/postgres")

        if batch_size > self.MAX_BATCH_SIZE:
            print(f"A batch size of {batch_size} is too large. Setting it to {self.MAX_BATCH_SIZE}")
            self._batch_size = self.MAX_BATCH_SIZE

        if not os.path.isdir(output_directory):
            print(f"{output_directory} does not exist. Creating it")
            os.makedirs(output_directory)


    def download_all(self):
        for i in range(self._start_gse_id, self._start_gse_id + self._end_gse_id, self._batch_size):
            batch_end = min(i + self._batch_size, self._end_gse_id)
            print(f"Downloading MINiML files {i} to {batch_end - 1}")

            threads = []
            for j in range(i, batch_end):
                gse_id = "GSE" + str(j)
                thread = threading.Thread(target=self.get_metadata, args=(gse_id,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()


    def get_metadata(self, gse_id: str) -> bool:
        """
        Downloads and unzips the metadata from GEO

        :param gse_id: The GEO GSE identifier
        :return: True if the metadata was downloaded and unzipped successfully
        """
        temp_directory = os.path.join(self._output_directory, gse_id)
        gzipped_miniml_file_location = f"{temp_directory}/{gse_id}_family.xml.tgz"
        miniml_file_location = f"{self._output_directory}/{gse_id}_family.xml"

        # If the file already exists, then quit early
        if os.path.exists(miniml_file_location):
            return True

        os.makedirs(temp_directory, exist_ok=True)

        download_attempt = self.download_miniml_file(
            gse_id,
            gzipped_miniml_file_location=gzipped_miniml_file_location
        )

        if not download_attempt.success:
            shutil.rmtree(temp_directory)
            self.load_download_attempt(download_attempt)

            return False

        # Extract the downloaded archive
        try:
            with tarfile.open(gzipped_miniml_file_location, 'r:gz') as tar:
                tar.extractall(path=temp_directory)

        except tarfile.TarError as e:
            download_attempt.success = False
            download_attempt.error_message = f"Extraction failed: {e}"

            shutil.rmtree(temp_directory)
            self.load_download_attempt(download_attempt)

            return False

        shutil.move(f"{temp_directory}/{gse_id}_family.xml", miniml_file_location)
        shutil.rmtree(temp_directory)

        download_attempt.local_path = miniml_file_location

        self.load_download_attempt(download_attempt)


    @staticmethod
    def download_miniml_file(gse_id: str, gzipped_miniml_file_location: str) -> DownloadAttempt:
        # replace the last three characters that are not GSE with nnn
        stub = "GSE" + gse_id[3:-3] + 'nnn'
        url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{stub}/{gse_id}/miniml/{gse_id}_family.xml.tgz"

        try:
            # Send an HTTP GET request to download the file
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save the downloaded file
            with open(gzipped_miniml_file_location, 'wb') as file:
                file.write(response.content)

            return DownloadAttempt(
                gse_id=gse_id,
                url=url,
                local_path='',
                success=True,
                error_message=None
            )

        except requests.exceptions.RequestException as e:
            return DownloadAttempt(
                gse_id=gse_id,
                url=url,
                local_path='',
                success=False,
                error_message=str(e)
            )


    def load_download_attempt(self, download_attempt: DownloadAttempt) -> None:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO download_attempt (
                    gse_id,
                    url,
                    local_path,
                    success,
                    error_message
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    download_attempt.gse_id,
                    download_attempt.url,
                    download_attempt.local_path,
                    download_attempt.success,
                    download_attempt.error_message
                )
            )

        self.conn.commit()
