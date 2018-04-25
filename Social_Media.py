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
    add_view_rules(message_view, '/message/')

create_views_with_rules()

# Register MessageView as the handler for all the /message/ requests. For
# more info
# about what is going on here, see http://flask.pocoo.org/docs/0.12/views/
# message_view = MessageView.as_view('message_view')
# app.add_url_rule('/message/',
#                  defaults={'message_id': None},
#                  view_func=message_view,
#                  methods=['GET'])
#
# app.add_url_rule('/message/<int:user_id>',
#                  view_func=message_view,
#                  methods=['message'])
#
# app.add_url_rule('/message/<int:message_id>',
#                  view_func=message_view,
#                  methods=['GET'])
#
# app.add_url_rule('/message/<int:message_id>',
#                  view_func=message_view,
#                  methods=['DELETE'])
#
# app.add_url_rule('/message/<int:message_id>',
#                  view_func=message_view,
#                  methods=['PUT'])
#
# app.add_url_rule('/message/<int:message_id>',
#                  view_func=message_view,
#                  methods=['PATCH'])
