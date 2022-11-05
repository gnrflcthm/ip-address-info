import json
from typing import Dict  # For specifying a Dict return type in functions
from requests import get  # For http requests


def ip_info(address=None) -> Dict:
    IP_API_URL = "https://ipapi.co"
    res = get(
        f'{IP_API_URL}/{address}/json') if address else get(f'{IP_API_URL}/json')
    if res.text == None:
        raise Exception("An Error has occured fetching IP Address Information")
    ipInfo = json.loads(res.text)
    return ipInfo


def test_ip_info():
    ipInfo = ip_info('8.8.8.8')

    for key, val in ipInfo.items():
        assert key != None
        assert type(key) == str
        assert val != None
