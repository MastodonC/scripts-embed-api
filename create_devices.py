#!/usr/bin/python
import sys
import csv
import time
import json
import requests
from requests.auth import HTTPBasicAuth

# Note: leave empty if reading property codes from a csv file
CODES = []  # properties codes will be appended to this list after
# running the function get_entities_names
PROJECT_ID = "xxxxx-xxxxx-xxxx-xxx-xx"  # Replace with your project id
URL = "https://www.getembed.com/4/"


def get_entities_names(csv_file):
    "Get the entities names from a csv header"
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        h = next(reader)
        i = h[1].split(',')[1:]
        CODES.extend(i)


# Note: this function will hit a limit.
# It won't retrieve more than 50 entities/project
def existing_entities(project_id, user, pwd):
    "Check whether entities already exists"
    # Get all entities for a project
    AUTH = HTTPBasicAuth(user, pwd)
    url = URL + 'projects/%s/entities' % project_id
    r = requests.get(url=url, auth=AUTH)
    time.sleep(2)
    entities_info = {}
    print r.status_code
    if r.status_code == 200:
        entities = r.json()["entities"]
        if len(entities) > 0:
            # For each entity build a dict {'code': 'id'}
            for e in entities:
                entities_info[e["property_code"]] = e["entity_id"]
        else:
            print "no properties for project " + project_id
    else:
        print "ERROR: " + r.text
    return entities_info


def existing_devices(entity_id, name, user, pwd):
    "Check whether a device already exists"
    # Get all devices for a property
    AUTH = HTTPBasicAuth(user, pwd)
    url = URL + 'entities/%s/devices/' % entity_id
    r = requests.get(url=url, auth=AUTH)
    time.sleep(2)
    if r.status_code == 200 and len(r.json()) > 0:
        for i in range(len(r.json())):
            desc = r.json()[i]["description"]
            if desc == name:
                print "There's already a device named :", name
                return True
            else:
                print "There's no device named :", name
                return False
    elif r.status_code == 200 and len(r.json()) == 0:
        print "no devices for property " + name

    else:
        "HTTP error ", r.status_code


def create_entities_devices(csv_file, project_id, codes, user, pw):
    "Create new entities, devices and write a report"
    # Check if entities in Embed are on the list
    print "Looking for pre-existing entities..."
    entities = existing_entities(project_id, user, pw)
    print "pre existing entities: ", entities

    # Lists to append new data and used to write the report:
    row_codes, row_ent, row_dev, row_sen = ["Code names"], ["Entity ids"], ["Device ids"],\
                                           ["Sensors ids"]
    AUTH = HTTPBasicAuth(user, pw)
    for name in codes:
        if name in entities.keys():
            # Check if there's already a device
            if existing_devices(entities[name], name, user, pw):
                pass
            else:
                # if a proprety but no device, then add one:
                row_codes.append(name)
                print "* Adding a device for property " + name + "..."
                url = URL + 'entities/%s/devices/' % entities[name]
                data = {"readings":
                        [{"unit": "L",
                          "period": "PULSE",
                          "type": "waterConsumption",
                          "alias": "WaterMeter"}],
                        "description": name, "entity_id": entities[name]}
                DATA = json.dumps(data)
                r = requests.post(url=url, data=DATA, auth=AUTH)
                row_ent.append(entities[name])
                time.sleep(2)
                if r.status_code == 201:
                    print "Device created for " + name + "!"
                    device_id = str(r.json()["location"]).split("/")[5]
                    row_dev.append(device_id)
                    url4 = URL + 'entities/%s/devices/%s'\
                        % (entities[name], device_id)
                    r4 = requests.get(url=url4, auth=AUTH)
                    time.sleep(2)
                    if r4.status_code == 200:
                        sensor_id = r4.json()["readings"][0]["sensor_id"]
                        row_sen.append(sensor_id)
                        print "sensor id added!"
                    else:
                        print "No sensor_id added, error: ", r4.status_code
                        row_sen.append("")
                else:
                    row_dev.append("")
                    print "Achtung! No device created for " + name +\
                        "! -> error: ", r.status_code

        else:
            # if not, create an entity
            print "** Creating a new property " + name + "..."
            url2 = URL + 'entities/'
            data2 = {"project_id": PROJECT_ID, "property_code": name}
            DATA2 = json.dumps(data2)
            r2 = requests.post(url=url2, data=DATA2, auth=AUTH)
            time.sleep(2)
            if r2.status_code == 201:
                row_codes.append(name)
                # add a device
                print "Adding a device for " + name + "..."
                path = r2.json()["headers"]["Location"]
                ent_id = path.split('/')[3]
                row_ent.append(ent_id)
                url3 = URL + 'entities/%s/devices/' % ent_id
                data3 = {"readings":
                         [{"unit": "L",
                           "period": "PULSE",
                           "type": "water meter"}],
                         "description": name, "entity_id": ent_id}
                DATA3 = json.dumps(data3)
                r3 = requests.post(url=url3, data=DATA3, auth=AUTH)
                time.sleep(2)
                if r3.status_code == 201:
                    print "Device created for " + name + "!"
                    device_id = str(r3.json()["location"]).split("/")[5]
                    row_dev.append(device_id)
                    url5 = URL + 'entities/%s/devices/%s' % (ent_id, device_id)
                    r5 = requests.get(url=url5, auth=AUTH)
                    time.sleep(2)
                    if r5.status_code == 200:
                        sensor_id = r5.json()["readings"][0]["sensor_id"]
                        row_sen.append(sensor_id)
                        print "sensor id added!"
                    else:
                        print "No sensor_id added, error: ", r5.status_code
                else:
                    print "Achtung! No device created for " + name + "!"

    with open(csv_file, 'w') as f:
        embed_writer = csv.writer(f, delimiter=',', quotechar='|',
                                  quoting=csv.QUOTE_MINIMAL)
        embed_writer.writerow(row_codes)
        embed_writer.writerow(row_ent)
        embed_writer.writerow(row_dev)
        embed_writer.writerow(row_sen)


# Note: this function will hit a limit.
# It won't retrieve more than 50 entities/project
def write_report(text_file, project_id, user, pwd):
    "Get properties ids, devices ids, sensors ids"
    # Expecting ONE device and ONE sensor per property here
    with open(text_file, 'w') as f:
        AUTH = HTTPBasicAuth(user, pwd)
        url = URL + 'projects/%s/entities/' % project_id
        r = requests.get(url=url, auth=AUTH)
        time.sleep(2)
        if r.status_code == 200:
            entities = r.json()["entities"]
            if len(entities) > 0:
                # For each entity write entity id, device_id, sensor_id
                for e in entities:
                    f.write("Property: " + e["property_code"] +
                            "\t id: " + e["entity_id"] + "\n")
                    url2 = URL + 'entities/%s/devices/' % e["entity_id"]
                    r2 = requests.get(url=url2, auth=AUTH)
                    time.sleep(2)
                    if r2.status_code == 200:
                        for d in r2.json():
                            f.write("\t > Device " + d["description"] + "\n")
                            for r in d["readings"]:
                                f.write("\t > Device id: "
                                        + r["device_id"] + "\n")
                                f.write("\t > Sensor id: "
                                        + r["sensor_id"] + "\n")
                    else:
                        print "Error ", r2.status_code
        else:
            print "Error ", r.status_code


if __name__ == "__main__":
    # Get the properties/devices names from the csv:
    get_entities_names(sys.argv[1])
    print CODES

    # Try the existing_devices function:
    # print existing_devices("c5a07ae6-ed19-4107-b4e7-8a7ad515435d",
    # u'A005', sys.argv[1], sys.argv[2])

    # Upload properties/devices and write the report in //:
    # create_entities_devices(PROJECT_ID, CODES, sys.argv[2], sys.argv[3])

    # Write report after upload
    # write_report(PROJECT_ID, sys.argv[1], sys.argv[2])
