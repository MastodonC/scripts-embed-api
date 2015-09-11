#!/usr/bin/python
import sys
import csv
import requests
import send_requests as sr
from requests.auth import HTTPBasicAuth
from datetime import datetime

BASE_URL = "https://www.getembed.com/4/entities/"
# BASE_URL = "http://localhost:8010/4/entities/"

# Info available for a profile:
# PROFILE_INFO = []
DEFAULT_INFO = ['profile_data', 'profile_id']


def results_to_return(data):
    "Print the results to your terminal"
    profiles = {"As built": [], "As designed": []}
    for d in data:
        if d["profile_data"]["event_type"] == "As built":
            profiles["As built"].append({d["profile_id"]:
                                     d["profile_data"]})
        elif d["profile_data"]["event_type"] == "As designed":
            profiles["As designed"].append({d["profile_id"]:
                                         d["profile_data"]})
        else:
            print "I didn't expect this type of property profile!"
    return profiles


def results_to_csv(data):
    "Write the results to a csv file"
    format = "%Y%m%d_%H%M%S"
    date = datetime.now().strftime(format)
    filename = "~/report_" + date
    print filename
    with open(filename, 'w') as f:
        report_writer = csv.writer(f, delimiter=',', quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
        print ">> CSV file written!"


def get_all_profiles(user, password, entity_id, action):
    '''Return info on all your profiles for this entity:
    [action]: Results can be printed and/or written to 
    a csv file. Value should be 'stdout', 'csv', 'both'
    or 'return'.'''
    url = BASE_URL + entity_id + "/profiles/"
    data = sr.get_request(user, password, url)
    if action == 'stdout':
        print results_to_return(data)
    elif action == 'csv':
        results_to_csv(data)
    elif action == 'both':
        print results_to_return(data)
        results_to_csv(data)
    elif action == 'return':
        return results_to_return(data)
    else:
        print """The only actions available are 
        'stdout', 'csv' or 'both'."""


if __name__ == "__main__":
    get_all_profiles(sys.argv[1], sys.argv[2],
                     "df8d259dce700d4ca07e854a86d45b4c00250b90",
                     "return")
