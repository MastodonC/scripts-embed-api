#!/usr/bin/python
import sys
# import csv
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


def results_to_stdout(data, *args):
    "Print the results to your terminal"
    args = args[0]
    for d in data:
        if not args or set(args) < set(DEFAULT_INFO):
            results = [i + ": " + d[i] for i in DEFAULT_INFO]
            print (" - ").join(results)
        elif set(args) < set(PROGRAMME_INFO):
            new_args = set(args) - set(DEFAULT_INFO)
            results = [i + ": " + d[i] for i in DEFAULT_INFO]
            results.extend([i + ": " + d[i] for i in new_args if d[i]])
            print ("\n").join(results)


def results_to_csv(data, *args):
    "Write the results to a csv file"
    print ">> CSV file written!"
    

def get_all_programmes(user, password, action, *args):
    '''Return info on all your programmes:
    [action]: Results can be printed and/or written to 
    a csv file. Value should be 'stdout', 'csv' or 'both'.
    [*args]: (see PROGRAMME_INFO for the full list)
    - If *args is left blank the info returned is 
    set in DEFAULT_INFO.
    - Otherwise it returns DEFAULT_INFO and the other 
    parameters specified.'''
    url = URL + "programmes/"
    data = sr.get_request(user, password, url)
    #for d in data:
    if action == 'stdout':
        results_to_stdout(data, args)
    elif action == 'csv':
        results_to_csv(data, args)
    elif action == 'both':
        results_to_stdout(data, args)
        results_to_csv(data, args)
    else:
        print """The only actions available are 
        'stdout', 'csv' or 'both'."""


def get_programme_by_id(user, password, programme_id):
    url = URL + "programmes/" + programme_id
    data = sr.get_request(user, password, url)
    print data['name'], " - ", data['programme_id']


if __name__ == "__main__":
    get_all_programmes(sys.argv[1], sys.argv[2], 'both')
    # get_all_programmes(sys.argv[1], sys.argv[2], 'stdout',
    #                    'description', 'name', 'projects')
    # get_programme_by_id(sys.argv[1], sys.argv[2],
    # "d0b152a1-8a5d-4062-9163-e1adb3a2853d")
