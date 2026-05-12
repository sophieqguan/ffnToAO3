import io
import zipfile
import requests

from util.util import lprint

# static
BASE_API_URL = 'https://fichub.net'
API_REQ_URL = f'{BASE_API_URL}/api/v0/epub?q='


def api_content_request(download_html_url):
    try:
        response = requests.get(f'{BASE_API_URL}{download_html_url}')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        lprint(f'API request failed.')
        raise Exception(f'API request failed: {e}')

    zip_content = response.content
    zip_file = zipfile.ZipFile(io.BytesIO(zip_content))

    # Iterate over each file in the zip archive and unzip html to html
    # should only have 1 item
    for file_info in zip_file.infolist():
        return zip_file.read(file_info.filename).decode()
