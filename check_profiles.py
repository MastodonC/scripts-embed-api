#!/usr/bin/python
import os
import sys
import csv
import time
import json
import requests
import pandas as pd
from datadiff import diff
import embed_profiles as profiles
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


def profiles_to_csv(user, pwd, entities, filename):
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


def get_info_from_csv(csv_path, column):
    df = pd.read_csv(csv_path)
    list_info = df[column].values.tolist()
    set_no_dupl = set(list_info)
    return list(set_no_dupl)


def get_profiles_diffs(user, password, entities):
    for entity_id in entities:
        print "Entity: ", entity_id
        return diff_profiles(user, password, entity_id)


def diff_profiles(user, password, entity_id):
    print "Property: ", entity_id
    profiles_dict = profiles.get_all_profiles(user, password,
                                        entity_id, 'return')
    for k, v in profiles_dict.items():
        print k
        print v[0].keys()[0], " VS ", v[1].keys()[0]
        print diff(v[0].values()[0], v[1].values()[0])


if __name__ == "__main__":
    # profiles_to_csv(sys.argv[1], sys.argv[2],
    #              ["d52942fd-bda2-4ecc-98b6-5b6a948f907a",
    #               "28e0563d-5515-4534-a5cc-db973ea66179"],
    #              "profiles_test.csv")

    # print list_all_projects(sys.argv[1], sys.argv[2], sys.argv[3])

    # print list_all_entities(sys.argv[1], sys.argv[2], projects)

    # data = read_json_data("../embed_bpe_duplicates.json")
    # entities = data['entities']
    # profiles_to_csv(sys.argv[1], sys.argv[2], entities,
    #              "../duplicate_profiles.csv")

    # Working on diffs between duplicated profiles:
    # entities = get_info_from_csv(sys.argv[1], "Property ID")
    # get_profiles_diffs(sys.argv[2], sys.argv[3], entities[:5])
    
    # Example w/ 3 profiles per type:
    # diff_profiles(sys.argv[1], sys.argv[2],
    #               "df8d259dce700d4ca07e854a86d45b4c00250b90")

    # Example w/ 2 profiles per type:
    diff_profiles(sys.argv[1], sys.argv[2],
                  "5c230d38-7713-4a0b-abcc-db77661396c1")
