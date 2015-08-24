#!/usr/bin/python
import sys, requests, time
from requests.auth import HTTPBasicAuth

## Embed url
URL = "https://www.getembed.com/4/"

## Add entity and device ids for properties you want to upload measurements to:
## Example:
## [{"entity1": ["device1.1", "device1.2"]}, {"entity2": ["device2.1", "device2.2"]}]
entities = [
    {"": []},
    {"": []}
]

def post_measurements(entity_id, device_id, user, pwd):
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "entities/" + entity_id + "/devices/" + device_id + "/measurements/"
    measurements = {}
    data = json.dumps(measurements)
    r = requests.post(url=url, data=data, auth=auth)
    time.sleep(2)
    if r.status_code == 201:
        print "Measurements uploaded for device ", device_id, " in property ", entity_id
    else:
        print "Error ", r.status_code, " while uploading measurements to device ", device_id

def upload_all_measurements(user, pwd):
    for entity in entities:
        for device in entity:
            post_measurements(entity, device, user, pwd)


if __name__ == "__main__":
    post_measurements(sys.argv[1], sys.argv[2])
                
