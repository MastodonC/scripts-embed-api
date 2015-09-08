#!/usr/bin/python
import sys
# import csv
import time
# import json
import requests
import send_requests as sr
from requests.auth import HTTPBasicAuth

# URL = "https://www.getembed.com/4/"
URL = "http://localhost:8010/4/"


def get_all_programmes(user, password):
    '''Print out the names and ids of
    existing Embed programmes.'''
    url = URL + "programmes/"
    data = sr.get_request(user, password, url)
    for d in data:
        print d['name'], " - ", d['programme_id']


def get_programme_by_id(user, password, programme_id):
    auth = HTTPBasicAuth(user, password)
    url = URL + "programmes/" + programme_id
    print url
    try:
        r = requests.get(url=url, auth=auth)
        time.sleep(2)
        if r.status_code == requests.codes.ok:
            print "The request was accepted! =)"
            response = r.json()
            print("Programme: ", response['name'],
                  " - ", response['programme_id'])
        else:
            print "Something went wrong! :-/"
        # if r.status_code == 200:
        #     print("Programme: ", r.json()['name'],
        # " - ", r.json()['programme_id'])
        # else:
        #     print "**else block** "
        #     r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        print "**except block** - Connection error. ", e
    except requests.exceptions.ConnectTimeout as e:
        print "**except block** - Connection timed out. ", e
    except requests.exceptions.RequestException as e:
        print "**except block** - Request exception. ", e
        sys.exit()


if __name__ == "__main__":
    get_all_programmes(sys.argv[1], sys.argv[2])
    # get_programme_by_id(sys.argv[1], sys.argv[2],
    # "d0b152a1-8a5d-4062-9163-e1adb3a2853d")
