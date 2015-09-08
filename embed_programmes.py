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

# Info available for a programme:
PROGRAMME_INFO = ['name', 'programme_id',
                  'description', 'lead_page_text',
                  'projects', 'leaders', 'created_at',
                  'public_access', 'home_page_text',
                  'admin', 'editable', 'updated_at']

DEFAULT_INFO = ['name', 'programme_id']

EXTRA_INFO = set(PROGRAMME_INFO) - set(DEFAULT_INFO)


def get_all_programmes(user, password, *args):
    '''Print out the names and ids of
    existing Embed programmes.'''
    url = URL + "programmes/"
    data = sr.get_request(user, password, url)
    print args
    for d in data:
        if not args or set(args) < set(DEFAULT_INFO):
            results = [i + ": " + d[i] for i in DEFAULT_INFO]
            print (" - ").join(results)
        elif set(args) < set(PROGRAMME_INFO):
            print '***'
            new_args = set(args) - set(DEFAULT_INFO)
            print new_args
            results = [i + ": " + d[i] for i in DEFAULT_INFO]
            results.extend([i + ": " + d[i] for i in new_args if d[i]])
            print ("\n").join(results)


def get_programme_by_id(user, password, programme_id):
    url = URL + "programmes/" + programme_id
    data = sr.get_request(user, password, url)
    print data['name'], " - ", data['programme_id']


if __name__ == "__main__":
    print EXTRA_INFO
    # get_all_programmes(sys.argv[1], sys.argv[2])
    get_all_programmes(sys.argv[1], sys.argv[2], 'description',
                       'name')
    # get_programme_by_id(sys.argv[1], sys.argv[2],
    # "d0b152a1-8a5d-4062-9163-e1adb3a2853d")
