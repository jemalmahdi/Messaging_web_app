"""
WooMessages
CS 232
Final Project


AVI VAJPEYI, JEMAL JEMAL, ISAAC WEISS, MORGAN FREEMAN

This Flask app allows a user to interact with a music artist database in a
RESTful fashion. Resources can be posted, updated, deleted or queired for.


To run the flask app:
$ <activate virtual environment>
$ pip install flask
$ pip install WTForms
$ pip install tabulate
$ pip install flask_login
$ pip install passlib
$ export FLASK_APP=app_main.py
$ flask run

*******************************************************************************
A general description of the WooMessage API is as follows.

There are three types of resources: Artists, Albums, Tracks

--ARTISTS
An artist resource is an individual musical artist.

    Attributes:
    id int -- The unique number to represent this resource.
    name string -- The name of the artist.
    age int -- The age of the artist.


GET /artist

Description:
Get a list of all artists

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/artists/
[
  {
        "id": 1,
        "name": Bob,
        "age": 80,
  },
  {
        "id": 1,
        "name": Bobbie,
        "age": 8,
  }
]

GET /artists/:id

Description:
Get a single artist by ID

Parameters:
id - the ID of the dog

Example usage:
$ curl -X GET http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


POST /artist

Description:
Add a new artist and get the added artist in response


Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


PUT /artist

Description:
Update ALL attributes of an artist and
get the updated artist in response

Parameters:
id - the id of the artist


Example usage:
$ curl -X PUT -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}


PATCH /artist

Description:
Update one or more attributes of an artist and
get the updated artist in response

Parameters:
id - the id of the artist

Example usage:
$ curl -X PATCH -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbieee,
    "age": 8,
}


DELETE /artist

Description:
Delete an artist and get the deleted artist in response

Parameters:
id - the id of the artist

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/artists/1
{
    "id": 1,
    "name": Bobbie,
    "age": 8,
}

*******************************************************************************
--Albums
An album resource is an individual musical album.

    Attributes:
    id int -- The unique number to represent this resource.
    name string -- The name of the album.
    artist_id int -- The id of the artist who created the album.


GET /album

Description:
Get a list of all albums

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/albums/
[
  {
        "id": 1,
        "name": Bob,
        "artist_id": 80,
  },
  {
        "id": 1,
        "name": Bobbie,
        "artist_id": 8,
  }
]

GET /albums/:id

Description:
Get a single album by ID

Parameters:
id - the ID of the album

Example usage:
$ curl -X GET http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


POST /album

Description:
Add a new album and get the added album in response

Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


PUT /album

Description:
Update ALL attributes of an album and
get the updated album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X POST -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}

PATCH /album

Description:
Update one or more attributes of an album and
get the updated album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X PATCH -d "name"="Elvis" -d "age="131" http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}


DELETE /album

Description:
Delete an album and get the deleted album in response

Parameters:
id - the id of the album

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/albums/1
{
    "id": 1,
    "name": Bobbie,
    "artist_id": 8,
}

*******************************************************************************
--Track
A track resource is an individual musical track.

    Attributes:
    album_id int -- The id of the album the track is from
    duration int -- The duration of the track in seconds
    id int -- The unique number to represent this resource.
    name string -- The name of the track.


GET /tracks/

Description:
Get a list of all tracks

Parameters:
None

Example usage:
$ curl -X GET http://127.0.0.1:5000/tracks/
[
  {
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
  },
  {
    "album_id": 2,
    "duration": 120,
    "id": 2,
    "name": "All My Life"
  }
]

GET /tracks/:id

Description:
Get a single track by ID

Parameters:
id - the ID of the track

Example usage:
$ curl -X GET http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}


POST /tracks/

Description:
Add a new track and get the added track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X POST -d "album_id"="23" -d "duration"="23" -d "name"="Blah"
http://127.0.0.1:5000/tracks/1
{
    "album_id": 23,
    "duration": 23,
    "id": 1,
    "name": "Blah"
}


PUT /tracks/

Description:
Update ALL attributes of an track (other than ID) and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X PUT -d "album_id"="23" -d "duration"="23" -d "name"="Blah"
http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}



PATCH -d album_id="1" -d duration="155" \
http://127.0.0.1:5000/track/1

Description:
Update one or more attributes of an track and
get the updated track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X PATCH -d "duration"="23" http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 23,
    "id": 1,
    "name": "Ace of Spades"
}



DELETE /tracks/:id

Description:
Delete an track and get the deleted track in response

Parameters:
id - the id of the track

Example usage:
$ curl -X DELETE http://127.0.0.1:5000/tracks/1
{
    "album_id": 1,
    "duration": 156,
    "id": 1,
    "name": "Ace of Spades"
}



*******************************************************************************
"""
from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
import csv
import sqlite3
from collections import OrderedDict
from custom_views import *
from database import *

from flask import Flask, g, jsonify, request, \
    render_template, redirect, url_for
import os
import click



app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'WooMessages.sqlite')


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database Created')


@app.cli.command('initdb_with_csv')
@click.argument('filename')
def convert_csv_to_sqlite_command(filename):
    convert_csv_to_sqlite(filename)
    print('Inserted' + filename+'data into music.sqlite')


@app.route('/')
def home_page():
    """
    Serves as a home page
    """
    return render_template('HomePage.html')


def add_view_rules(view, view_url):
    """
    Adds rules to a custom MethodView. Preconditions are that the custom
    MethodView has the RESTful API implmented.

    :param view: the custom MethodView
    :param view_url: the URL that the view is routed to.
    :return:
    """

    app.add_url_rule(view_url,
                     defaults={'id': None},
                     view_func=view,
                     methods=['GET'])
    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['GET'])

    app.add_url_rule('/artist/',
                     view_func=view,
                     methods=['POST'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['DELETE'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['PUT'])

    app.add_url_rule(view_url+'<int:id>',
                     view_func=view,
                     methods=['PATCH'])

def create_views_with_rules():
    """
    Helper function to add rules to the custom views written for the API of
    the Free Music Database.

    :return: None
    """
    message_view = MessageView.as_view('message_view')
    add_view_rules(message_view, 'api/message/')

    user_view = UserView.as_view('user_view')
    add_view_rules(user_view, 'api/user/')

    chat_view = ChatView.as_view('chat_view')
    add_view_rules(chat_view, 'api/chat/')

    chatrel_view = ChatRelView.as_view('chatrel_view')
    add_view_rules(chatrel_view, 'api/chatrel/')


