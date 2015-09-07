#!/usr/bin/python
import sys
import csv
import time
import json
import requests
from requests.auth import HTTPBasicAuth

URL = "https://www.getembed.com/4/"


def get_all_programmes(user, password):
    '''Print out the names and ids of
    existing Embed programmes.'''
    auth = HTTPBasicAuth(user, password)
    url = URL + "programmes/"
    try:
        r = requests.get(url=url, auth=auth)
        time.sleep(2)
        print r.status_code, r.reason
        if r.status_code == 200:
            print "The programmes are:"
            for p in r.json():
                print p['name'], " - ", p['programme_id']
    except requests.exceptions.ConnectionError as e:
        print "Connection error. ", e
    except requests.exceptions.ConnectTimeout as e:
        print "Connection timed out. ", e

if __name__ == "__main__":
    get_all_programmes(sys.argv[1], sys.argv[2])
