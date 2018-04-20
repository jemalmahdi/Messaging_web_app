from flask import Flask, g, jsonify, request, render_template
from flask.views import MethodView
import os
import csv
import sqlite3
import datetime
from collections import OrderedDict

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'Social.sqlite')

def init_db():
    """
    This will initialize the database
    """
    conn = get_db()

    query = '''
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS post;
        CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            first TEXT,
            last TEXT           
        );
        CREATE TABLE post (
            id INTEGER PRIMARY KEY,
            post TEXT,
            time TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id)
        );                    
    '''

    conn.cursor().executescript(query)


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database Created')


def connect_db():
    """
    Returns a sqlite connection object associated with the application's
    database file.
    """

    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row

    return conn


def get_db():
    """
    Returns a database connection. If a connection has already been created,
    the existing connection is used, otherwise it creates a new connection.
    """

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


def get_date():
    now = datetime.datetime.now()

    return now.strftime("%Y-%m-%d %H:%M")


def query_by_id(table_name, item_id):
    """
    Get a row from a table that has a primary key attribute named id.

    Returns None of there is no such row.

    :param table_name: name of the table to query
    :param item_id: id of the row
    :return: a dictionary representing the row
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'SELECT * FROM {} WHERE id = ?'.format(table_name)

    cur.execute(query, (item_id,))

    row = cur.fetchone()

    if row is not None:
        return dict(row)
    else:
        return None


def get_all_rows(table_name):
    """
    Returns all of the rows from a table as a list of dictionaries. This is
    suitable for passing to jsonify().

    :param table_name: name of the table
    :return: list of dictionaries representing the table's rows
    """

    conn = get_db()
    cur = conn.cursor()

    query = 'SELECT * FROM {}'.format(table_name)

    results = []

    for row in cur.execute(query):
        results.append(dict(row))

    return results

def insert_post(post, user_id):
    conn = get_db()
    cur = conn.cursor()

    query = '''
        INSERT INTO post(post, time, user_id) VALUES(?, ?, ?)
    '''

    cur.execute(query, (post, get_date(), user_id))
    conn.commit()

    cur.execute('SELECT * FROM post WHERE id = ?', (cur.lastrowid,))

    return dict(cur.fetchone())


def update_post(text, user_id, post_id):
    conn = get_db()
    cur = conn.cursor()

    query = '''
        UPDATE post SET text = ? AND user_id = ? WHERE id = ?
    '''

    cur.execute(query, (text, user_id, post_id))
    conn.commit()

    cur.execute('SELECT * FROM post WHERE id = ?', (post_id,))

    return dict(cur.fetchone())


def delete_item(table_name, item_id):
    """
    This function deletes items with item_id from table_name

    :param table_name: the table which has an item to delete
    :param item_id: it item which to delte
    :return: NONE
    """
    conn = get_db()
    cur = conn.cursor()

    query = 'DELETE FROM {} WHERE id = ?'.format(table_name)

    cur.execute(query, (item_id,))
    conn.commit()

    return None


class PostView(MethodView):
    def get(self, post_id):
        """
        Handle GET requests.

        Returns JSON representing all of the post if post_id is None, or a
        single post if post_id is not None.

        :param post_id: id of a post, or None for all posts
        :return: JSON response
        """
        if post_id is None:
            posts = get_all_rows('post')
            return jsonify(posts)
        else:
            posts = query_by_id('post', post_id)

            if posts is not None:
                response = jsonify(posts)
            else:
                raise RequestError(404, 'post not found')

            return response

    def post(self, user_id):
        """
        Handles a post request to insert a new city. Returns a JSON
        response representing the new post.

        The post name must be provided in the requests's form data.

        :return: a response containing the JSON representation of the post
        """
        if 'text' not in request.form:
            raise RequestError(422, 'text of post required')
        else:
            response = jsonify(insert_post(request.form['text'], user_id))
        return response

    def delete(self, post_id):
        """
        Handles a DELETE request given a certain post_id
        :return: a response containing the JSON representation of the
            old post
        """

        if post_id is None:
            raise RequestError(422, 'post id required')
        else:
            posts = query_by_id('post', post_id)

            if posts is not None:
                delete_item('post', post_id)
            else:
                raise RequestError(404, 'post not found')
        return jsonify(posts)

    def put(self, post_id):
        """
        Handles a PUT request given a certain post_id
        :return:a response containing the JSON representation of the
            new post
        """

        if post_id is None:
            raise RequestError(422, 'post id is required')
        else:
            if 'text' not in request.form:
                raise RequestError(422, 'post text is required')
            else:
                post = query_by_id('post', post_id)

                if post is not None:
                    update_post(request.form['text'],
                                  request.form['user'], post_id)
                else:
                    raise RequestError(404, 'post not found')

                post = query_by_id('post', post_id)
                return jsonify(post)

    def patch(self, post_id):
        """
        Handles the PATCH request given a certain post_id
        :return:a response containing the JSON representation of the
            old post
        """

        if post_id is None:
            raise RequestError(422, 'post id is required')
        else:
            posts = query_by_id('post', post_id)

            if posts is None:
                raise RequestError(404, 'post not found')
            else:

                new_text = posts['text']
                if 'text' in request.form:
                    new_name = request.form['text']

                new_user = posts['user_id']
                if 'user' in request.form:
                    new_user = request.form['user']

                update_post(post_id, new_text, new_user)
                posts = query_by_id('posts', post_id)
                return jsonify(posts)



# Register PostView as the handler for all the /post/ requests. For
# more info
# about what is going on here, see http://flask.pocoo.org/docs/0.12/views/
post_view = PostView.as_view('post_view')
app.add_url_rule('/post/', defaults={'post_id': None},
                 view_func=post_view, methods=['GET'])
app.add_url_rule('/post/<int:user_id>', view_func=post_view,
                 methods=['POST'])
app.add_url_rule('/post/<int:post_id>', view_func=post_view,
                 methods=['GET'])
app.add_url_rule('/post/<int:post_id>', view_func=post_view,
                 methods=['DELETE'])
app.add_url_rule('/post/<int:post_id>', view_func=post_view,
                 methods=['PUT'])
app.add_url_rule('/post/<int:post_id>', view_func=post_view,
                 methods=['PATCH'])