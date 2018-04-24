"""

flask-login.readthedocs.io

$ pip install flask_login


Investigated ways to implement a login system with flask, with Jemal Jemal. We
 went through the docs for flask-login and WTForms and decided that these were
 the tools we will use. Following this, we watched two youtube videos:
 1) https://www.youtube.com/watch?v=2dEM-s3mRLE
 2) https://www.youtube.com/watch?v=zRwy8gtgJ1A
 The first was not to helpful. The second is just what we need, and we plan on
 meeting tomorrow to use it to help us implement the login.



"""

__author__ = 'Vajpeyi_Jemal'

import os
from flask import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user


app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'Social.sqlite')
app.config["SECRET_KEY"] = 'thisissecret'
# init DB

# flask-login
login_manager = LoginManager() # allows Flask-Login
login_manager.init_app(app) # Once app obj created this configures it for login
login_manager.login_view = "login" # asdasda

# silly user model
class User(UserMixin):
    """
    Inherits from UserMixin that implments:

    1) is_authenticated(self): Checks if user is authenticated (has provided
    valid credentials).

    2) is_active(self):

    3) is_anonymous(self):

    4) get_id(self):
    return

    """

    def __init__(self, id):
        """
        Constructor for user object.
        """
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        """
        Overloading print function for User Objects.
        """
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


@login_manager.user_loader
def load_user(user_id):
    """
    Reloads the USER obj specified by USER ID, stored during one login session.

    :param userid: unicode ID of user
    :return: corresponding user object
    """
    return User.get(user_id)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)


# Index
@app.route('/')
def index():
    return render_template('HomePage.html')


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    """

    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    """

    :return:
    """
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    """

    :param e:
    :return:
    """
    return Response('<p>Login failed</p>')


if __name__ == "__main__":
    app.run()