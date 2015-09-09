#!/usr/bin/python
import sys
import time
import csv
import requests
from requests.auth import HTTPBasicAuth

# Replace with a list of property codes
CODES = ['A001', 'A002', 'A003', 'A004', 'A005']

# Nested lists to make it easy to write to a csv file
LIST_CODES = [[i] for i in CODES]

URL = "https://www.getembed.com/4/"

# Replace with your project id
PROJECT_ID = "xxxxx-xxxxx-xxxx-xxx-xx"


def write_report(filename, user, pwd):
    """Retrieve info about properties in a project
    and with specific property codes.
    Write the results to a csv file."""
    with open(filename, 'w') as f:

        report_writer = csv.writer(f, delimiter=',', quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(['property code', 'property ID',
                                'device description', 'device ID',
                                'sensor ID'])

        auth = HTTPBasicAuth(user, pwd)
        for i in range(len(CODES)):
            print "Looking up info for property %s ..." % CODES[i]
            url1 = URL + 'entities/?q=project_id3A' + PROJECT_ID +\
                '%20AND%20property_code%3A' + CODES[i]
            r1 = requests.get(url=url1, auth=auth)
            time.sleep(2)
            if r1.status_code == 200:
                entities = r1.json()['entities']
                if len(entities) > 1:
                    print "WHAT!?! There are %d properties named %s"\
                        % (len(entities), CODES[i])
                else:
                    results1 = r1.json()['entities'][0]
                    LIST_CODES[i].append(results1['entity_id'] or '')
                    devices = results1['devices']
                    for device in devices:
                        for sensor in device['readings']:
                            if device['description'] == CODES[i]:
                                LIST_CODES[i].append(device['description'])
                                LIST_CODES[i].append(sensor['sensor_id'])
                                LIST_CODES[i].append(sensor['device_id'])
            report_writer.writerow(LIST_CODES[i])
        print "report written"


if __name__ == '__main__':
    # print LIST_CODES[:10]
    write_report('properties_report.csv', sys.argv[1], sys.argv[2])
