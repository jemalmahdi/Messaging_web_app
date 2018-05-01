"""
WooMessages
CS 232
Final Project
AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN THOMPSON


This program lets the user interact with the Free Music Database's API, to
present data about the albums, artists and tracks in the database. This will
soon be expanded to include commands to add information to the database and
modify information to the database.

Normal use:
$ python3 query_WooMessage.py show api/message
time                chat_id    user_id    id  message
----------------  ---------  ---------  ----  --------------------------------
04/25/2018 21:49          1          1     1  Boy I like school
04/26/2018 21:49          1          2     2  I like donkeys
04/27/2018 21:49          1          3     3  nah. i think school sucks
04/28/2018 21:49          1          4     4  nah boy school is cool
04/29/2018 21:49          1          5     5  i don't think we should do drugs

...

$ python3 query_WooMessage.py show api/chat
title                    time                id
-----------------------  ----------------  ----
School is good           04/25/2018 21:49     1
I hate life              02/4/2018 21:49      2
Yoyoyoy                  02/10/2018 21:49     3
crack is defintely wack  02/17/2018 21:49     4
...

$ python3 query_WooMessage.py show api/user
email                    id  username    name    password
---------------------  ----  ----------  ------  -----------------------------
Avajpai18@wooster.edu     2  AviVajpeyi  Avi     $5$rounds=535000$d..rqlB6QA
tomboss@gmail.com         3  TomBoss     Boss    $5$rounds=535000$titTV1yN2U
...

"""
import json
import requests
import sys
import tabulate

# Base URL for the API. All API requests begin with this URL.
API_BASE_URL = 'http://127.0.0.1:5000/'
SUCCESSFUL_RESPONSE = 200
BAD_RESPONSE = 404


def dump_json_data(data, filename):
    """
    Helper function to convert a list of dictionaries into JSONs which are then
    saved in a textfile.

    :param data: list of dictionaries to save as a JSON
    :param filename: the filename where the data is saved
    :return: None
    """
    # data must be a python dictionary
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def read_json_data_from_file(filename):
    """
    Helper function to read JSON data from a textfile.

    :param filename: the txtfile containing the JSON data.
    :return: the JSON data
    """
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def show_commands():
    """
    Deals with the 'show' commands that requests GETs from the API.
    :return:
    """
    # Build up the URL for search

    table_name = sys.argv[2]
    request_url = '{}{}/'.format(API_BASE_URL, table_name)

    # Use the requests module to fetch the URL as JSON
    response = requests.get(request_url)
    status_code = response.status_code

    if status_code == SUCCESSFUL_RESPONSE:
        # Convert the JSON content of response to a Python list
        content = response.json()

        # Getting keys from 1st entry
        keys = list()
        for key in content[0].keys():
            keys.append(key)

        data = [x.values() for x in content]
        print(tabulate.tabulate(data, keys))

    else:
        print('Error: the url {} does not exist'.format(request_url))
        sys.exit(1)


def insert_commands():
    print("INSERT")


def update_commands():
    print("PUT/PATCH")


def main():

    # there must be commands
    if len(sys.argv) < 2:
        sys.exit('Usage:\n$ python3 query_WooMessage.py <command> <table>\n'
                 'Current commands availible: show\n'
                 'Current tables: api/chat, api/user, api/message')

    command = sys.argv[1]

    if command == "show":
        show_commands()
    # elif command == "add":
    #     insert_commands()
    else:
        print("Error: Invalid command")


if __name__ == '__main__':
    main()
