#!/usr/bin/python
import sys
import time
import csv
import requests
from requests.auth import HTTPBasicAuth

URL = "https://www.getembed.com/4/"

# Replace w/ entity ids
ENTITIES = [u'xxxxxxxx', u'zzzzzz', u'yyyyyyy', u'vvvvvvvv']


def list_properties(filename):
    "List ids of properties to be deleted."
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
        r = [i[0] for i in reader]
        return r


def delete_properties(list_properties, user, pwd):
    print "There are %d properties to be deleted."\
        % len(list_properties)
    for entity_id in list_properties:
        url = URL + "entities/%s" % entity_id
        auth = HTTPBasicAuth(user, pwd)
        r = requests.delete(url=url, auth=auth)
        time.sleep(3)
        if r.status_code != 204:
            print "The properties couldn't be deleted. Error ",\
                r.status_code
        else:
            print r.status_code, " Property %s was successfully deleted!"\
                % entity_id


if __name__ == "__main__":
    l = list_properties("to_delete.csv")
    delete_properties(l, sys.argv[1], sys.argv[2])

    # delete_properties(ENTITIES, sys.argv[1], sys.argv[2])
