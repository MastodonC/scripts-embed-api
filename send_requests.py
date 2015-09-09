#!/usr/bin/python
import sys
# import json
import urlparse
import requests
from requests.auth import HTTPBasicAuth

HOSTNAMES = {"www.getembed.com", "localhost"}


def validate_hostname(url):
    """Check the hostname is part of authorised 
    hostnames defined in HOSTNAMES"""
    if urlparse.urlparse(url=url).hostname not in HOSTNAMES:
        raise requests.exceptions.InvalidURL(url)


def work_locally(url):
    """Print a warning message to tell you whether
    you're working on a local Embed instance or
    on the production server."""
    if urlparse.urlparse(url=url).hostname == "localhost":
        print ">> Ok, you're working on your local Embed instance."
    elif urlparse.urlparse(url=url).hostname == "www.getembed.com":
        print ">> Careful, you're sending requests to Embed production server."


def get_request(user, password, url):
    """Generate a generic http get request,
    handle errors and return the json data."""
    ## Two verifications to be changed to decorators.
    work_locally(url)
    validate_hostname(url)

    auth = HTTPBasicAuth(user, password)
    try:
        r = requests.get(url=url, auth=auth)
        if r.status_code == requests.codes.ok:
            print ">> The http request was accepted! =)"
            return r.json()
        else:
            print ">> Something went wrong! :-/"
            r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        print ">> Connection error: ", e.message
    except requests.exceptions.ConnectTimeout as e:
        print ">> Connection timed out: ", e.message
    except requests.exceptions.HTTPError as e:
        print ">> HTTP error: ", e.message
    except requests.exceptions.RequestException as e:
        print ">> Request exception: ", e.message
        sys.exit()


if __name__ == "__main__":
    # validate_hostname("http://google.com/images/")
    work_locally("http://www.getembed.com/app")
