# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import json
import pprint
import requests
import sys
import urllib
from PIL import Image
from io import BytesIO
from dateutil import parser

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    from urllib import quote
    from urllib import urlencode


CLIENT_ID = "19ZPvP3ALZ_khhzj-X7LOg"
CLIENT_SECRET = "EX8iWl633lIrBbk4nc6WvkOOzSjhqhAsX3InB4tmfB4WoUe4cl9F6Azy61gNAeJH"


API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


DEFAULT_TERM = input('Please enter the name of the business that you would like to query: ')
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 1


def obtain_bearer_token(host, path):
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, location):
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(bearer_token, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    #pprint.pprint(response['hours'], indent=2)

    #For milestone 1, could potentially be used to store and print images onto a window
    imageList = []

    for i in range (0, len(response['photos'])):
        url = response['photos'][i]
        imageList.append(Image.open(requests.get(url, stream=True).raw))

    #for now just show a single image from the array
    imageList[0].show()

    print('Address: ' + response['location']['address1'])

    #show hours open
    for i in range (0, len(response['hours'][0]['open'][0])):
        print(response['hours'][0]['open'][i]['start'])

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()