from typing import Dict
from requests import get
import json
import sys

"""API Used for getting ip address information"""
IP_API_URL = "https://ipapi.co"

"""Gets the ip address information on the given public IP Address"""
def get_ip_adress_info(address=None) -> Dict:
    res = get(f'{IP_API_URL}/{address}/json') if address else get(f'{IP_API_URL}/json')
    if res.text == None:
        raise Exception("An Error has occured fetching IP Address Information")
    """Returns IP Address Information as a Python Dictionary"""
    return json.loads(res.text)

"""Formats output returned from the API"""
def print_formatted(title: str, data: Dict) -> None:
    print(f"\n{title.title()}\n")
    for key, val in data.items():
        key: str = key
        print(key.replace(",", " ").title(), "." * (45 - len(key)), f": {str(val)}", sep="")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        data = get_ip_adress_info()
        print_formatted("IP Address Information", data)
    else:
        address = args[0]
        data = get_ip_adress_info(address)
        print_formatted("IP Address Information", data)

