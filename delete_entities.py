#!/usr/bin/python
import os, sys, csv
import time, json, requests
from requests.auth import HTTPBasicAuth

URL = "https://www.getembed.com/4/"

test_properties = ["25a1cd92-e9b2-429e-8f0b-d5b0fec0a70c", "0f8ac79a-ad97-40c3-b0b4-bb59b5e0027d",
                   "542576ff-4b81-4517-8dbd-8f0c67cfe91c", "7f6c4159-fe5b-43d8-9040-70b66d4f58a1",
                   "df0f772c-e591-4294-962e-7d22411c380a", "cf5efbc0-034e-44a3-9563-5a45dea33328"]

def list_properties(filename):
    "List ids of properties to be deleted."
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        r = [i[0] for i in reader]
        return r

def delete_properties(list_properties, user, pwd):
    print "There are %d properties to be deleted." % len(list_properties)
    for entity_id in list_properties:
        url = URL + "entities/%s" % entity_id
        auth = HTTPBasicAuth(user, pwd)
        r = requests.delete(url=url, auth=auth)
        time.sleep(3)
        if r.status_code != 204:
            print "The properties couldn't be deleted. Error ", r.status_code
        else:
            print r.status_code, " Property %s was successfully deleted!" % entity_id

if __name__ == "__main__":
    l = list_properties("to_delete.csv")
    delete_properties(l, sys.argv[1], sys.argv[2])

    #delete_properties(test_properties, sys.argv[1], sys.argv[2])

