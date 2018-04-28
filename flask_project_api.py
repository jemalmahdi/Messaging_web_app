import requests
import sys

API_BASE_URL = 'http://127.0.0.1:5000/api/users'


def main():
    """
    This program is a command line program which takes in a username of a user
    and prints off the names of all of the chats that the owner is involved in.
    """

    if len(sys.argv) != 2:
        sys.exit('Usage: {} <search string>'.format(sys.argv[0]))

    search_string = sys.argv[1]

    request_url = '{}/{}'.format(API_BASE_URL, search_string)

    response = requests.get(request_url)

    if response.status_code != 200:
        sys.exit('Error fetching dogs owned by {}'.format(sys.argv[1]))

    content = response.json()

    owner_id = content['id']

    response = requests.get('http://127.0.0.1:5000/api/chat/')

    if response.status_code != 200:
        sys.exit('Error fetching dogs')

    content = response.json()

    for repository in content:
        if repository['owner_id'] == owner_id:
            print(repository['name'])


if __name__ == '__main__':
    main()
