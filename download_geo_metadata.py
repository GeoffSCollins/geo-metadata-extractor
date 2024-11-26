from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import tarfile
import time
import threading

ERROR_LOG = "error_log.txt"


def download_miniml_file(gse_id: str, gzipped_miniml_file_location: str) -> bool:
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

        return True

    except requests.exceptions.RequestException as e:
        return False


def get_metadata(gse_id: str) -> bool:
    # create a directory named gse_id
    os.makedirs(gse_id, exist_ok=True)

    gzipped_miniml_file_location = f"{gse_id}/{gse_id}_family.xml.tgz"
    miniml_file_location = f"{gse_id}_family.xml"

    download_successful = download_miniml_file(
        gse_id,
        gzipped_miniml_file_location=gzipped_miniml_file_location
    )

    if not download_successful:
        os.system(f"rm -rf {gse_id}")

        with open(ERROR_LOG, 'a') as file:
            file.write(f"Failed to download MINiML file for accession {gse_id}\n")

        return False

    # Extract the downloaded archive
    try:
        with tarfile.open(gzipped_miniml_file_location, 'r:gz') as tar:
            tar.extractall(path=gse_id)
    except tarfile.TarError as e:
        with open(ERROR_LOG, 'a') as file:
            file.write(f"Failed to extract the downloaded archive for accession {gse_id}\n{e}\n")
        return False

    os.system(f"mv {gse_id}/{gse_id}_family.xml {miniml_file_location}")
    os.system(f"rm -rf {gse_id}")


if __name__ == '__main__':
    start = 1
    end = 10
    batch_size = 150

    start_time = time.time()

    for i in range(start, start + end, batch_size):
        batch_end = min(i + batch_size, end)
        print(f"Downloading MINiML files {i} to {batch_end - 1}")

        threads = []
        for j in range(i, batch_end):
            gse_id = "GSE" + str(j)
            thread = threading.Thread(target=get_metadata, args=(gse_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    end_time = time.time()
    print(f"Time taken to download {end - start} MINiML files: {end_time - start_time} seconds")
