"""Controls the web server for the entire site with a Flask framework. Assumes
that the main app is app.py. Contains links to the rest of the site, and it
handles non-static downloads.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_file
from flask import flash

import os
import sys
sys.path.insert(0, 'static/py')

import fetch

#from flaskext.mysql import MySQL

from bs4 import BeautifulSoup

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# calls the app so it can run
if __name__ == "__main__":
    app.run()

import psycopg2

# Environmental variables
DATABASE_URL = os.environ['DATABASE_URL']
try:
    SSL_MODE = os.environ['SSL_MODE']
except KeyError:
    SSL_MODE='require' # default is requiring ssl

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM videos")
    data = cur.fetchall()
    cur.close()
    conn.close()
    print("connected to postgres!")
except:
    print("not connected to postgres!")

# setting up secret key
# TODO make this environment var
#app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.secret_key = b'\xd2\xc7\xdd\xa4\xd7\xc7\xfb\x92\x88\x15\xbbF,3\xc7\x9d'

# setting up Flask-Login manager
from flask_login import LoginManager, login_required, login_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)

# initialize login form stuff
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

# setting up Flask-Login user object
sys.path.insert(0, 'srv')
from User import User
def getUserById(id):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE Id = %s;', (id, ))
        data = cur.fetchall()
        cur.close()
        conn.close()
        
        if data:
            print("Successfully retrieved user")
            return User(data[0][1], data[0][3], DATABASE_URL, SSL_MODE) # user, pass
        else:
            print("Failed to retrieve user: no user")
            return None
    except:
        print("Failed to retrieve user: no connection")
        return None
@login_manager.user_loader
def load_user(user_id):
    return getUserById(user_id)


# make sure that each request is redirected to https
# TODO fix potential security vulnerability
@app.before_request
def before_request():
    if SSL_MODE is 'require' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    fetch.fetchHomePage()
    return render_template('history.html')

@app.route('/search')
def search():
    print("in search")
    text = request.args.get('jsdata')
    results = []
    # each comma separated group represents and AND clause
    for p in text.split(','):
        queryTerms = p.split(" ") # use later to search for specific terms like map
        phraseResults = []
        if text:
            # Assumption: there better only by one instance of 1vX. if not takes the first one
            clutchKills = -1 # -1 means no requirement
            i = text.find("1v")
            if i > -1 and len(text) - i > 2:
                clutchKills = int(text[i + 2])
                if clutchKills and 0 <= clutchKills and 5 >= clutchKills: # if there's a number after v
                    clutchKills = int(text[i + 2])
                else:
                    clutchKills = -1

            for d in data:
                if queryRequirements(text) and (text in d or text.lower() in d or d[16] == clutchKills) and [d[1], d[10], d[2]] not in phraseResults:
                    phraseResults.append([d[1], d[10], d[2]])
        for r in phraseResults:
            if r not in results:
                results.append(r)


    print("out search")

    return jsonify(results)

# this is a bad function TODO fix
def queryRequirements(q):
    if q == 'true' or q == 'false':
        return False
    return True

# basic 404 page. Hopefully isn't called all that often TODO: implement
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
@app.route('/testAPI')
def testAPI():
    return jsonify("OH")

# input rating into Ratings table upon user post request
@app.route('/updateRating/<videoId>&<userId>&<rating>', methods=['POST'])
def inputRating(videoId, userId, rating):
    # connect to db and send command
    print('input received')
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Ratings WHERE VideoId=%s AND UserId=%s;', (videoId, userId))
        # if rating exists, update it
        if cur.fetchone() != None:
            cur.execute('UPDATE Ratings SET rating=%s WHERE VideoId=%s AND UserId=%s;', (rating, videoId, userId))
        # if rating doesn't exist, insert into db
        else:
            cur.execute('INSERT INTO Ratings VALUES(DEFAULT, %s, %s, %s, DEFAULT);', (videoId, userId, rating))
        conn.commit()
        print('Sent rating', rating, 'for video', videoId, 'for user', userId, 'successfully.')
        cur.close()
        conn.close()
        return "test success"
    except:
        print('Failed to send rating', rating, 'for video', videoId, 'for user', userId)
        return "test failed"

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # authenticate(User)
        # TODO hash password from client to server
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
            cur = conn.cursor()
            cur.execute('SELECT password FROM Users WHERE Name = %s AND Password = crypt(%s, Password);', (request.form['username'], request.form['password']))
            encryptedPassword = cur.fetchall()[0][0]
            user = User(request.form['username'], encryptedPassword, DATABASE_URL, SSL_MODE)
            cur.execute('SELECT Id FROM Users WHERE Name = %s AND Password = %s;', (user.username, user.password))
            id = cur.fetchall()[0][0]
            if id:
                user.isAuthenticated = True
                user.isActive = True
                # bool returns True for any string, False for blank/None
                print('before login_user')
                login_user(user, remember = bool(request.form.get('remember_me')))
                print('past login_user')
                flash('Logged in successfully.')
                assert(user.is_authenticated)
                print("user authenticated")
            else:
                flash('Login failed.')
                print("authentication failed: invalid credentials")
                raise
            cur.close()
            conn.close()
        except:
            print("authentication failed: no connection to database - ", sys.exc_info()[0])
            flash('Login failed.')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


'''@app.route("/signup")
def testreact():
    return render_template('test-react.html') '''
'''
@app.route('/highlight/<videoId>')
def load_highlight():
    return render_template('highlight.html')'''

'''# loads About page
@app.route('/about')
def about():
    return render_template('about.html')'''

'''# loads contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')'''
