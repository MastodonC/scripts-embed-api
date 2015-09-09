#!/usr/bin/python
import sys
import requests
import time
import json
import send_requests as sr
from requests.auth import HTTPBasicAuth

# Embed url
URL = "https://www.getembed.com/4/"

# Add entity and device ids for properties you want to upload
# measurements to:
# Example:
# [{"entity1": ["device1.1", "device1.2"]},
#  {"entity2": ["device2.1", "device2.2"]}]
entities = [
    {"xxxxxxxxxxxxxx-xx-xxx-xxxxxx": ["aaaaabbbbbbbbaabbbbbbbbaa"]},
    {"yyyyyyyyyy-yyyy-yyyyyy-yyyyy": ["ccccccccccdddcddcdccdddcc"]}
]

# Update measurements and make sure "type" matches current sensor type
measurements = {"measurements": [
    {
        "value": "0.87",
        "timestamp": "2015-08-24T10:30:00Z",
        "type": "Pressure"
    }
]}


def get_json_data(filename):
    "Retrieve measurements from a json file."
    with open(filename, 'r') as f:
        data = json.load(f)
        return data


# To run if you want to check device info
def check_device_info(entity_id, device_id, user, pwd):
    "Check device exists and device info."
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "entities/" + entity_id + "/devices/" + device_id
    r = requests.get(url=url, auth=auth)
    print r.status_code
    print r.json()


# To run to upload measurements device per device
# NOTE: Update measurements content and make sure "type"
# matches current sensor type
def post_measurements(entity_id, device_id, measurements, user, pwd):
    "Post measurements for a device."
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "entities/" + entity_id + "/devices/" + device_id +\
        "/measurements/"
    data = json.dumps(measurements)
    try:
        r = requests.post(url=url, data=data, auth=auth)
        time.sleep(2)
        print r.status_code, r.reason
        if r.status_code == 202:
            print "Measurements uploaded for device ", device_id,\
                " in property ", entity_id
    except requests.exceptions.ConnectionError as e:
        print "Connection error. ", e
    except requests.exceptions.ConnectTimeout as e:
        print "Connection timed out. ", e


# To run to upload measurements for several devices
def upload_all_measurements(user, pwd):
    "Add measurements for multiple devices."
    for entity in entities:
        for device in entity:
            post_measurements(entity, device, user, pwd)


def check_measurements_upload(entity_id, device_id, sensor_type,
                              start_date, end_date, user, pwd):
    """Check measurements were uploaded to a specific device.
    Expect the sensor type and start/end dates as strings like '2015-09-09'."""
    url = URL + "entities/" + entity_id + "/devices/" + device_id +\
    "/measurements/" + sensor_type + "?startDate=" + start_date +\
    "%2000:00:00&endDate=" + end_date + "%2000:00:00"
    print sr.get_request(user, pwd, url)


if __name__ == "__main__":
    # post_measurements("d0a91ad4-dd99-4ad1-8b6f-ad97c54a6aae",
    #                   "b4149ec6-7264-4f5c-b62a-09d3baff7808",
    #                   sys.argv[1], sys.argv[2])

    # check_device_info("4bc58f62-1861-484c-bfda-f24fff8bc03c",
    #              "c09416f0-82b0-4f3d-b76b-a47ba84372a3",
    #              sys.argv[1], sys.argv[2])

    # Example to upload json measurements:

    # data = get_json_data("/home/eleonore/Documents/WORK_PROJECTS/
    # hecuba/tapestry/input/temp-data.json")
    # post_measurements("4bc58f62-1861-484c-bfda-f24fff8bc03c",
    #                   "c09416f0-82b0-4f3d-b76b-a47ba84372a3",
    #                   data, sys.argv[1], sys.argv[2])

    # Example to check measurements upload:

    check_measurements_upload("4bc58f62-1861-484c-bfda-f24fff8bc03c",
                              "c09416f0-82b0-4f3d-b76b-a47ba84372a3",
                              "Temperature", "2012-05-01", "2012-05-02",
                              sys.argv[1], sys.argv[2])
