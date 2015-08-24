#!/usr/bin/python
import sys, requests, time, json
from requests.auth import HTTPBasicAuth

## Info on this script refer to a testing instance on getembed.com

## Embed url
URL = "https://www.getembed.com/4/"

## Add entity and device ids for properties you want to upload measurements to:
## Example:
## [{"entity1": ["device1.1", "device1.2"]}, {"entity2": ["device2.1", "device2.2"]}]
entities = [
    {"ded6b5f1-ce79-4912-b6be-f8f9af7ce93b": ["ded6b5f1-ce79-4912-b6be-f8f9af7ce93b"]},
    {"e5ffee9f-8ab9-4346-b012-78aea2ed9a73": ["1473d94f-bf97-4321-80b9-be84dedca6de"]}
]

measurements = {"measurements": [
    {
        "value": "0.87",
        "timestamp": "2014-05-11T10:30:00Z",
        "type": "water meter",
    }
]}

## To run if you want to check device info
def check_device(entity_id, device_id, user, pwd):
    "Check device exists and device info."
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "entities/" + entity_id + "/devices/" + device_id
    r = requests.get(url=url, auth=auth)
    print r.status_code
    print r.json()

## To run to upload measurements device per device
# NOTE: Update measurements content and make sure "type" matches current sensor type
def post_measurements(entity_id, device_id, user, pwd):
    "Post measurements for a device."
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "entities/" + entity_id + "/devices/" + device_id + "/measurements/"
    data = json.dumps(measurements)
    try:
        r = requests.post(url=url, data=data, auth=auth)
        time.sleep(2)
        print r.status_code, r.reason
        if r.status_code == 202:
            print "Measurements uploaded for device ", device_id, " in property ", entity_id
    except ConnectionError as e:
        print "Connection error. ", e
    except ConnectTimeout as e:
        print "Connection timed out. ", e

## To run to upload measurements to several devices
def upload_all_measurements(user, pwd):
    "Add measurements for multiple devices."
    for entity in entities:
        for device in entity:
            post_measurements(entity, device, user, pwd)


if __name__ == "__main__":
    post_measurements("45f93880-df89-4565-acd1-6a1d6c22792c", "d434ec0e-210f-4937-9873-6c42eddd3936", sys.argv[1], sys.argv[2])

    # check_device("45f93880-df89-4565-acd1-6a1d6c22792c", "d434ec0e-210f-4937-9873-6c42eddd3936", sys.argv[1], sys.argv[2])
                
