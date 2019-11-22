"""Controls the web server for the entire site with a Flask framework. Assumes
that the main app is app.py. Contains links to the rest of the site, and it
handles non-static downloads.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import json
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
        data = cur.fetchone()
        cur.close()
        conn.close()
        if data:
            print("Successfully retrieved user")
            return User(data[0], data[1], data[3], DATABASE_URL, SSL_MODE) # user, pass
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


# TODO move to database.py
def getCategories():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM RatingCategories')
        categories = cur.fetchall()
        cur.close()
        conn.close()
        print('Successfully retrieved rating categories')
        return categories
    except:
        print('Failed to retrieve rating categories')
        return None

# TODO move to database.py
def getCode(vid):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT Code FROM Videos WHERE Id = %s', vid)
        code = cur.fetchall()
        cur.close()
        conn.close()
        print('Successfully retrieved video', vid, 'code')
        return code
    except:
        print('Failed to retrieve video', vid, 'code')
        return None
# TODO move to database.py
def getVideoUserRatings(vid, uid):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Ratings WHERE VideoId=%s AND UserId=%s;', (vid, uid))
        u = cur.fetchall()
        print(u)
        ur = []
        for j in u:
            # append rating categoryid and rating number
            print('j:', j)
            ur.append(str(j[3]))
            ur.append(str(j[4]))
        print('Fetched ratings for video', vid, 'for user', uid, 'successfully.')
        cur.close()
        conn.close()
        return ur
    except:
        print('Failed to fetch ratings for video', vid, 'for user', uid, 'because', sys.exc_info()[1])
        return []
# TODO move to database.py
def getAvgVideoRatings(vid):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM RatingAvgs WHERE VideoId=%s;', (vid,))
        r = cur.fetchall()
        print(r)
        ar = []
        for j in r:
            # append rating categoryid and rating number
            print('j:', j)
            ar.append(str(j[2]))
            ar.append(str(j[4]))
        print('Received average ratings for video', vid, 'successfully.')
        cur.close()
        conn.close()
        return ar
    except:
        print('Failed to receive average ratings for video', vid, 'because', sys.exc_info()[1])
        return []

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    fetch.fetchHomePage()
    try:
        return render_template('history.html', categories=json.dumps(getCategories()))
    except:
        return render_template('history.html')

# TODO make secure
@app.route('/search&<userId>')
def search(userId):
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
                if queryRequirements(text) and (text in d or text.lower() in d or d[4] == clutchKills) and [d[1], d[4], d[2]] not in phraseResults:
                    # get user's past reviews for selected videos
                    ur = getVideoUserRatings(d[0], userId)
                    phraseResults.append([d[0], d[1], d[4], d[2], ur])
        for r in phraseResults:
            if r not in results:
                results.append(r)


    print("out search")
    print(results)
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

@app.route('/videos/<videoId>/avgRatings', methods=['POST'])
def avgRatings(videoId):
    try:
        return jsonify(getAvgVideoRatings(videoId))
    except:
        print("EXCEPTION")
        return jsonify([])

@app.route('/videos/<videoId>/userRatings&<userId>', methods=['POST'])
def userRatings(videoId, userId):
    try:
        return jsonify(getVideoUserRatings(videoId, userId))
    except:
        return jsonify([])

@app.route('/videos/<videoId>')
def videos(videoId):
    return render_template('video.html', videoId=videoId, videoTitle="Placeholder", videoCode=getCode(videoId), categories=json.dumps(getCategories()))

# input rating into Ratings table upon user post request
@app.route('/updateRating/<videoId>&<userId>&<categoryId>&<rating>', methods=['POST'])
def inputRating(videoId, userId, categoryId, rating):
    # connect to db and send command
    print('input received')
    rating = float(rating)
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode=SSL_MODE)
        cur = conn.cursor()
        cur.execute('SELECT Total, Average FROM RatingAvgs WHERE VideoId=%s AND RatingCategoryId=%s;', (videoId, categoryId))
        result = cur.fetchone()
        cur.execute('SELECT * FROM Ratings WHERE VideoId=%s AND UserId=%s AND RatingCategoryId=%s;', (videoId, userId, categoryId))
        oldRatingRow = cur.fetchone()
        print("oldRatingRow:", oldRatingRow)
        # if rating exists, remove old rating and insert new
        if oldRatingRow != None: # assumption: a rating exists, the rating average exists too
            print("result: ", result[0])
            if result[0] > 1:
                revertedRating = (result[0] * result[1] - oldRatingRow[4]) / (result[0] - 1)
                newRating = (revertedRating * (result[0] - 1) + rating) / result[0]
            else: # if there's only one rating to begin with
                newRating = rating
            cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE VideoId=%s AND RatingCategoryId=%s;', (newRating, result[0], videoId, categoryId))
            cur.execute('UPDATE Ratings SET rating=%s WHERE VideoId=%s AND UserId=%s AND RatingCategoryId=%s;', (rating, videoId, userId, categoryId))
        # if rating doesn't exist, insert into db
        else:
            if result != None:
                newTotal = result[0] + 1
                newAvg = (newTotal * result[1] + float(rating)) / (newTotal + 1)
                cur.execute('UPDATE RatingAvgs SET Average=%s, Total=%s WHERE VideoId=%s AND RatingCategoryId=%s;', (newAvg, newTotal, videoId, categoryId))
            else:
                cur.execute('INSERT INTO RatingAvgs VALUES(DEFAULT, %s, %s, %s, %s);', (videoId, categoryId, 1, rating))
            cur.execute('INSERT INTO Ratings VALUES(DEFAULT, %s, %s, %s, %s, DEFAULT);', (videoId, userId, categoryId, rating))
        conn.commit()
        print('Sent rating', rating, 'for video', videoId, 'for user', userId, 'of type', categoryId, 'successfully.')
        cur.close()
        conn.close()
        return "test success"
    except:
        print('Failed to send rating', rating, 'for video', videoId, 'for user', userId, 'of type', categoryId, 'because', sys.exc_info()[0:2])
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
            cur.execute('SELECT Id FROM Users WHERE Name = %s AND Password = %s;', (request.form['username'], encryptedPassword))
            id = cur.fetchall()[0][0]
            if id:
                # bool returns True for any string, False for blank/None
                user = User(id, request.form['username'], encryptedPassword, DATABASE_URL, SSL_MODE)
                print("user inited")
                login_user(user, remember = bool(request.form.get('remember_me')))
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
