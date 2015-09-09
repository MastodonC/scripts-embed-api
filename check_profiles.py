#!/usr/bin/python
import os
import sys
import csv
import time
import json
import requests
from requests.auth import HTTPBasicAuth

URL = "https://www.getembed.com/4/"


def list_all_projects(user, pwd, programme_id):
    """Return a list of all project ids in a
    programme."""
    project_ids = []
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "programmes/" + programme_id + "/projects"
    r = requests.get(url=url, auth=auth)
    time.sleep(2)
    if r.status_code == 200:
        list_projects = r.json()
        print "There are %d projects." % len(list_projects)
        for project in list_projects:
            print project['project_id']
            project_ids.append(project['project_id'])
    return project_ids


def list_all_entities(user, pwd, projects):
    """Returns a list of all the entity ids
    for a list of project ids."""
    entity_ids = []
    auth = HTTPBasicAuth(user, pwd)
    for proj_id in projects:
        url = URL + "projects/" + proj_id + "/entities"
        r = requests.get(url=url, auth=auth)
        time.sleep(2)
        if r.status_code == 200:
            list_entities = r.json()['entities']
            for entity in list_entities:
                entity_ids.append(entity['entity_id'])
    return entity_ids


def read_json_data(filename):
    """Get duplicate profiles projects and
    properties ids stored in a json file."""
    with open(filename, 'r') as f:
        data = json.load(f)
        return data


def get_profiles(user, pwd, entities, filename):
    """Returns a csv file containing profile info
    for a list of entity ids provided."""
    auth = HTTPBasicAuth(user, pwd)

    with open(filename, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Property ID', 'Profile ID',
                             'Event type', 'Timestamp'])

        for entity in entities:
            print "ENTITY: ", entity
            url = URL + "entities/" + entity + "/profiles/"
            print url
            r = requests.get(url=url, auth=auth)
            time.sleep(2)
            print r.status_code, r.reason
            if r.status_code == 200:
                list_profiles = r.json()
                print "There are %d profiles." % len(list_profiles)
                if len(list_profiles) > 2:
                    for profile in list_profiles:
                        profile_id = profile['profile_id']
                        profile_name = profile['profile_data'].get(
                            'event_type', '')
                        profile_date = profile['timestamp']
                        csv_writer.writerow([entity, profile_id,
                                             profile_name, profile_date])


if __name__ == "__main__":
    get_profiles(sys.argv[1], sys.argv[2],
                 ["d52942fd-bda2-4ecc-98b6-5b6a948f907a",
                  "28e0563d-5515-4534-a5cc-db973ea66179"],
                 "profiles_test.csv")

    # print list_all_projects(sys.argv[1], sys.argv[2], sys.argv[3])

    # print list_all_entities(sys.argv[1], sys.argv[2], projects)

    # data = read_json_data("../embed_bpe_duplicates.json")
    # projects = data['projects']
    # entities = data['entities']
    # get_profiles(sys.argv[1], sys.argv[2], projects, entities,
    #              "../duplicate_profiles.csv")
