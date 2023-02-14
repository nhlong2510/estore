import json
from urllib.request import urlopen


def read_json_internet(url):
    data = []
    try:
        url_response = urlopen(url)
        data = json.loads(url_response.read().decode())
    except Exception as ex:
        print(ex)
    return data
