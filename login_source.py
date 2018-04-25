"""
flask-login.readthedocs.io

To run the flask app:
$ <activate virtual environment>
$ pip install flask
$ pip install WTForms
$ pip install tabulate
$ pip install flask_login
$ pip install passlib
$ export FLASK_APP=login_source
$ flask run

Investigated ways to implement a login system with flask, with Jemal Jemal. We
 went through the docs for flask-login and WTForms and decided that these were
 the tools we will use. Following this, we watched two youtube videos:
 1) https://www.youtube.com/watch?v=2dEM-s3mRLE
 2) https://www.youtube.com/watch?v=zRwy8gtgJ1A
 The first was not to helpful. The second is just what we need, and we plan on
 meeting tomorrow to use it to help us implement the login.


24th April afternoon
Spoke with Isaac, Morgan and Jemal discussing the studtures of the tables and
divying up work. Set a timeline for when certain work is due by.

24th April evening
Pair-prgramming with Jemal to set up the Registeration. Used WTFform tutorials,
and bootstrap examples. Also relied on code snippets from
http://flask.pocoo.org/snippets/98/

25th April morning
Wrapped up the the login code. A user can now register and then log into our
website. There are validation checks in both the login and registeration page.
The password is encrypted. Upon Loging in, the user is moved to a dashboard
where all the active chats that the user is in are displayed.

"""

from Social_Media import *
from flask import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user

from passlib.hash import sha256_crypt # a hash algorithm that encrypts password
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'Social.sqlite')
app.config["SECRET_KEY"] = 'thisissecret'


# init DB if no db present (FOR NOW WE ARE JUST INITING, NEED TO DO THE CHECK OTHER TIMES)


# flask-login
login_manager = LoginManager()  # allows Flask-Login
login_manager.init_app(app)  # Once app obj created, configures it for login
login_manager.login_view = "login"


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
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)


# Index
@app.route('/')
def index():
    return render_template('HomePage.html')


# Register Form Class
class RegisterForm(Form):
    """
    This connects the html registeration form fields corresponding to the
    rendered HTML page's fields. The validators set requirements on the form
    fields.

    Inherits from Form. See http://flask.pocoo.org/snippets/135/
    """
    name = StringField('Name',
                       [validators.Length(min=1, max=50)])
    username = StringField('Username',
                           [validators.Length(min=4, max=25)])
    email = StringField('Email',
                        [validators.Length(min=6, max=50)])
    password = PasswordField('Password',
                             [validators.DataRequired(),
                              validators.EqualTo('confirm',
                                                 message='Incorrect Password')
                              ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # check if there is a post request and if the data inputted to form
        # is in the correct format (if it has been validated)
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        conn = get_db()
        cur = conn.cursor()

        # Execute query
        cur.execute("INSERT INTO user(name, email, username, password) "
                    "VALUES(?, ?, ?, ?)", (name, email, username, password))

        # Commit to DB
        conn.commit()

        # Flash a message to the HTML cause we just registered babbyyyyyy
        flash('Congratulations! You have sold your soul to WooMessages! Next '
              'time, read terms and conditions. Proceed to Login.', 'success')

        # now that registered, send to login site
        return redirect(url_for('login'))
    return render_template('RegisterationPage.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_entered = request.form['password']

        # Create cursor
        conn = get_db()
        cur = conn.cursor()

        # Get user by username
        cur.execute('SELECT * FROM user WHERE username = ?', (username,))
        data = cur.fetchall()
        num_rows = len(data)

        print(username)
        print(num_rows)

        # if the returned number of rows > 1 then user found
        if num_rows == 1:
            # Get stored hash
            userdata = data[0]
            password_real = userdata['password']

            # Compare Password entered to password saved in DB
            if sha256_crypt.verify(password_entered, password_real):
                # yay! The passwords match
                session['logged_in'] = True
                session['username'] = username
                welcome_text = "Welcome back, " + str(userdata['name'])

                flash(welcome_text, 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid password'
                flash("Invalid password", 'danger')
                return render_template('Login.html', error=error)

        else:
            error = 'Username not found'
            flash("WHO IS U??? Username not found", 'danger')
            return render_template('login.html', error=error)

    return render_template('Login.html')

# Check if user logged in
def is_logged_in(f):
    """
    Code adapted from http://flask.pocoo.org/snippets/98/

    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Logged out!', 'success')
    return redirect(url_for('login'))



# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    """

    :param e:
    :return:
    """
    return Response('<p>Login failed!</p>')


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    """


    :return:
    """
    # Create cursor
    # conn = get_db()
    # cur = conn.cursor()
    #
    # # Get user's active chats
    # cur.execute('SELECT chat.name FROM user, chat WHERE user.id = chat.user_id AND username = ?', (username,))
    # data = cur.fetchall()
    # num_rows = len(data)
    #
    # # Get list of active messages from chat rel [FETCHALL]
    # data = cur.fetchall()
    # num_rows = len(data)

    data = None
    num_rows = 0

    if num_rows > 0:
        return render_template('dashboard.html', active_chats=data)
    else:
        msg = 'No active chats'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()


if __name__ == "__main__":
    app.secret_key='WooMessagesKeepsSecrets'
    app.run(debug=True)