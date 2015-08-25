#!/usr/bin/python
import os, sys, csv
import time, json, requests
from requests.auth import HTTPBasicAuth

PROJECTS = [u'xxxxxxxx', u'zzzzzz', u'yyyyyyy', u'vvvvvvvv'] ## Replace w/ project ids

ENTITIES = [u'xxxxxxxx', u'zzzzzz', u'yyyyyyy', u'vvvvvvvv'] ## Replace w/ entity ids


URL = "https://www.getembed.com/4/"

PROG_ID = "XYJNGGFDDEE" ## Replace w/ programme id

## Note: this request will hit a limit of 50 responses.
def list_all_projects(user, pwd):
    "Lists all projects in a programme"
    project_ids = []
    auth = HTTPBasicAuth(user, pwd)
    url = URL + "programmes/" + PROG_ID + "/projects"
    r = requests.get(url=url, auth=auth)
    time.sleep(2)
    if r.status_code == 200:
        list_projects = r.json()
        print "There are %d projects." % len(list_projects)
        for project in list_projects:
            print project['project_id']
            project_ids.append(project['project_id'])
    return project_ids

## Note: this request will hit a limit of 50 responses.
def list_all_entities(user, pwd):
    "Lists all entities in a project"
    entity_ids = []
    auth = HTTPBasicAuth(user, pwd)
    for proj_id in PROJECTS:
        url = URL + "projects/" + proj_id + "/entities"
        r = requests.get(url=url, auth=auth)
        time.sleep(2)
        if r.status_code == 200:
            list_entities = r.json()['entities']
            for entity in list_entities:
                entity_ids.append(entity['entity_id'])
    return entity_ids

## Note: this request will hit a limit of 50 responses.
def get_profiles(user, pwd, filename):
    "Get properties profiles and write into csv file."
    auth1 = HTTPBasicAuth(user, pwd)
    
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Property ID', 'Profile ID', 'Event type', 'Timestamp'])
        
        for entity in ENTITIES:
            print "ENTITY: ", entity
            url1 = URL + "entities/" + entity + "/profiles"
            r = requests.get(url=url1, auth=auth1)
            time.sleep(2)
            print r.status_code
            if r.status_code == 200:
                list_profiles = r.json()
                print "There are %d profiles." % len(list_profiles)
                if len(list_profiles) > 2:
                    for profile in list_profiles:
                        profile_id = profile['profile_id']
                        profile_name = profile['profile_data'].get('event_type', '')
                        profile_date = profile['timestamp']
                        csv_writer.writerow([entity, profile_id, profile_name, profile_date])
                

if __name__ == "__main__":
    ##get_profiles(sys.argv[1], sys.argv[2])

    ##print list_all_projects(sys.argv[1], sys.argv[2])

    ##print list_all_entities(sys.argv[1], sys.argv[2])

    get_profiles(sys.argv[1], sys.argv[2], "entity_profiles.csv")
    print "CSV written!"

    #print ENTITIES.index('2cd308755ae52fd27adacd75c4eb7b71de2e0a7d')

    

