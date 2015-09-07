#!/usr/bin/python
import sys
import time
import csv
import requests
from requests.auth import HTTPBasicAuth

URL = "https://www.getembed.com/4/"


# Note: this function will hit a limit.
# It won't retrieve more than 50 entities/project
def get_project_info(project_id, entity_code, user, pwd):
    """Retrieve property, devices and sensor ids for
    a property code."""
    AUTH = HTTPBasicAuth(user, pwd)
    url = URL + 'projects/%s/entities/' % project_id
    r = requests.get(url=url, auth=AUTH)
    time.sleep(3)
    if r.status_code != 200:
        print "Error ", r.status_code
    if r.status_code == 200:
        print r.json()
        try:
            print len(r.json()["entities"]), "entities"  # if 50 <- limit!
            for i in r.json()["entities"]:

                if i["property_code"] == entity_code:
                    print "Property %s: %s"\
                        % (i["property_code"], i["entity_id"])
                    url2 = URL + 'en#tities/%s/devices/'\
                        % i["entity_id"]
                    r2 = requests.get(url=url2, auth=AUTH)
                    time.sleep(2)
                    if r2.status_code != 200:
                        print "Error ", r2.status_code
                    else:
                        for d in r2.json():
                            print "Device ", d["description"]
                            for s in d["readings"]:
                                print "Device id: ", s["device_id"]
                                print "Sensor id: ", s["sensor_id"]
        except:
            print "No properties for this project or else ..."
            pass


def get_entity_info(entity_id, user, pwd):
    "Get devices and sensors for a property given its id."
    AUTH = HTTPBasicAuth(user, pwd)
    url = URL + 'entities/%s/devices/' % entity_id
    r = requests.get(url=url, auth=AUTH)
    time.sleep(3)
    if r.status_code != 200:
        print "Error ", r.status_code
    else:
        for d in r.json():
            print "Device: ", d["description"]
            for s in d["readings"]:
                print "Device id: ", s["device_id"]
                print "Sensor id: ", s["sensor_id"]


# Note: this uses custom url and will not reach a limit
# in the search results
def find_entities_by_code(project_id, property_codes, outfile, user, pwd):
    """Retrieves info for properties given their property codes.
    Writes this info into a csv file."""
    AUTH = HTTPBasicAuth(user, pwd)
    with open(outfile, 'a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Entity code", "Entity id", # "Property data",
                         "Device code", "Device id", "Sensor id",
                         "Device2 code", "Device2 id", "Sensor2 id",
                         "Profile id", "Profile data"])
        for code in property_codes:
            url = URL + "entities/?q=project_id%3A" + project_id +\
                "%20AND%20property_code%3A" + code +\
                """&page=0&size=10&sort_key=programme_name.
                lower_case_sort&sort_order=asc"""
            r = requests.get(url=url, auth=AUTH)
            time.sleep(2)
            if r.status_code != 200:
                print "Error ", r.status_code
            else:
                for ent in r.json()["entities"]:
                    row = []
                    # Get property info:
                    print "Property ", ent["entity_id"]
                    row.extend([ent["property_code"], ent["entity_id"]])
                    # Get property data:
                    # row.append(ent["property_data"])
                    if len(ent["devices"]) == 0:
                        row.extend(["", "", ""])
                    if len(ent["devices"]) > 0:
                        for dev in ent["devices"]:
                            print "Device: ", dev["device_id"]
                            row.extend([dev["description"], dev["device_id"]])
                            for sen in dev["readings"]:
                                print "Sensor: ", sen["sensor_id"]
                                row.append(sen["sensor_id"])
                    # Get profile data:
                    url2 = URL + "entities/" + ent["entity_id"] + "/profiles/"
                    r2 = requests.get(url=url2, auth=AUTH)
                    time.sleep(2)
                    if r2.status_code != 200:
                        if r2.status_code == 404:
                            row.extend(["", ""])
                        print "Profile data - Error ", r2.status_code
                    else:
                        row.extend(["", "", ""])
                        for pro in r2.json():
                            row.extend([pro["profile_id"],
                                        pro["profile_data"]])
                    writer.writerow(row)


if __name__ == "__main__":

    cds = ['3144', '3148', '3171']
    #get_project_info("xxxxxx", "A009", sys.argv[1], sys.argv[2])

    # get_entity_info("4f4261dd-af09-408b-b443-1a22f3e9a7e3",
    # sys.argv[1], sys.argv[2])

    find_entities_by_code("c06c9bf8-d67c-4ab9-aa0f-75bbaf58b033", 
	cds, 
	"/home/eleonore/Documents/WORK_PROJECTS/hecuba/tapestry/report_stns.csv",
    	sys.argv[1], sys.argv[2])
