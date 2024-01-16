# Copyright (c) 2020 EUMETSAT <br>
# License: MIT

import requests
import json
import os


# ---------------------------------------------------------------------------

def generate_token(apis_endpoint="https://api.eumetsat.int", \
                   consumer_key=None, consumer_secret=None, \
                   credentials_file=None, token_url=None):
    '''
    Function to generate an access token for interacting with EUMETSAT Data
    Service APIs

    Args:
        apis_endpoint (str):    The endpoint URL of the API
        consumer_key (str):     The consumer key as a string
        consumer_secret (str):  The consumer secret as a string.
        credentials_file (str): An optional json format credentials file
        token_url (str):        The token URL (if different from default)

    Returns:
        An access token (if pass) or None (if fail).
    '''

    # build the token URL:
    if not token_url:
        token_url = apis_endpoint + "/token"

    # check the credentials.
    if not credentials_file and not consumer_key:
        print('No consumer key or credentials file given. Quitting...')
        return None

    if credentials_file:
        with open(credentials_file) as f:
            data = json.load(f)
            consumer_key = data['consumer_key']
            consumer_secret = data['consumer_secret']

    response = requests.post(
        token_url,
        auth=requests.auth.HTTPBasicAuth(consumer_key, consumer_secret),
        data={'grant_type': 'client_credentials'},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert_response(response)
    return response.json()['access_token']


# ---------------------------------------------------------------------------

def assert_response(response, success_code=200):
    '''
    Function to check API key generation response. Will return an error
    if the key retrieval was not successful.

    Args:
        response (obj):      The authentication response.
        success_code (int):  The expected sucess code (200).

    Returns:
        Nothing if success, error message if fail.
    '''

    assert response.status_code == success_code, \
        "API Request Failed: {}\n{}".format(response.status_code, \
                                            response.content)


# ---------------------------------------------------------------------------

def import_credentials(filename):
    '''
    Function to read <CONSUMER_KEY> and <CONSUMER_SECRET> from a JSON format
    file.

    Args:
        fiename (str):      The credentials filename

    Returns:
        Nothing if success, error message if fail.
    '''

    try:
        with open(filename, 'r') as json_file:
            credentials = json.load(json_file)
    except:
        print('File does not exist or is not in the correct format')
        return

    print('Successfully retrieved credentials....')
    return credentials
# ---------------------------------------------------------------------------