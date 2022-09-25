import socket
from typing import Dict
from requests import get
import re
import json
import sys

"""API Used for getting ip address information"""
IP_API_URL = "https://ipapi.co/{}/json/"

"""Public site for retrieving machine's public ip address"""
PUBLIC_IP_API_URL = "https://www.ipchicken.com/"

"""Gets the machine's local IP Address"""
def get_local_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


"""Gets the ip address information on the given public IP Address"""
def get_ip_adress_info(address="0.0.0.0") -> Dict:
    res = get(IP_API_URL.format(address))
    if res.text == None:
        raise Exception("An Error has occured fetching IP Address Information")
    """Returns IP Address Information as a Python Dictionary"""
    return json.loads(res.text)


"""Gets the machine's public IP address"""
def get_public_ip_address() -> str:
    res = get(PUBLIC_IP_API_URL)
    try:
        """Makes use of RegEx to match the pattern resembling an IP Address"""
        return re.findall(r"\d+\.\d+\.\d+\.\d+", res.text)[0]
    except:
        raise Exception("An Error has occured.")

def print_formatted(title: str, data: Dict) -> None:
    print(f"\n{title.title()}\n")
    for key, val in data.items():
        key: str = key
        print(key.replace(",", " ").title(), "." * (45 - len(key)), f": {str(val)}", sep="")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        data = get_ip_adress_info(get_public_ip_address())
        print_formatted("IP Address Information", data)
    else:
        address = args[0]
        data = get_ip_adress_info(address)
        print_formatted("IP Address Information", data)

