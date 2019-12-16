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

import os
import sys

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# calls the app so it can run
if __name__ == "__main__":
    app.run()

# Environmental variables
DATABASE_URL = os.environ['DATABASE_URL']
try:
    SSL_MODE = os.environ['SSL_MODE']
except KeyError:
    SSL_MODE='require' # default is requiring ssl

'''# set up SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
POSTGRES_URL = str('postgresql://localhost:5432')
POSTGRES_USER = str('postgres')
POSTGRES_PW = str('rorodog')
POSTGRES_DB = str('csgo_highlights')
TEST_DB_URL = str('postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB))
app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)
from sqlalchemy_utils import database_exists, create_database, drop_database
if database_exists(TEST_DB_URL):
    print('Deleting database.')
    drop_database(TEST_DB_URL)
if not database_exists(TEST_DB_URL):
    print('Creating database.')
    create_database(TEST_DB_URL)
db.create_all()
print('db should be up') '''

sys.path.insert(0, 'srv')
from database import DB
try:
    db = DB(DATABASE_URL, SSL_MODE)
    print("connected to postgres!")
except:
    print("not connected to postgres! error:", sys.exc_info()[1])

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
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, validators
class LoginForm(FlaskForm):
    username    = StringField('Username')
    password    = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Submit')

class SignUpForm(FlaskForm):
    from models import Weapon
    listWeaponChoices = db.getWeaponTypes()
    print("weapon choices: ", listWeaponChoices)
    # for reasons required by WTForms
    weaponChoices = list(map(lambda x:(x,x), listWeaponChoices))
    signUpUsername = StringField('Username', [validators.Length(min=4, max=25)])
    email          = StringField('Email Address', [validators.Email(), validators.Length(min=6, max=35)])
    signUpPassword = PasswordField('Password', [validators.Length(min=4, max=35)])
    weapon         = SelectField('Favorite Weapon', choices = weaponChoices)
    signUpSubmit   = SubmitField('Submit')

# setting up Flask-Login user object
from models import User
@login_manager.user_loader
def load_user(user_id):
    return db.getUserById(user_id)

# make sure that each request is redirected to https
# TODO fix potential security vulnerability
@app.before_request
def before_request():
    if SSL_MODE is 'require' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# run algolia
import algolia
algolia.initializeClipsIndex(db)

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    try:
        return render_template('history.html', categories=json.dumps(db.getCategories()))
    except:
        return render_template('history.html')

@app.route('/search&<userId>')
def search(userId):
    print("in search")
    text = request.args.get('jsdata')
    results = algolia.clipSearch(text)
    print("out search")
    print(results)
    return jsonify(results)

# basic 404 page. Hopefully isn't called all that often TODO: implement
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
@app.route('/testAPI')
def testAPI():
    return jsonify("OH")

@app.route('/clips/<clipId>/avgRatings', methods=['POST'])
def avgRatings(clipId):
    try:
        return jsonify(db.getAvgClipRatings(clipId))
    except:
        print("EXCEPTION: Could not retrive average ratings for", clipId)
        return jsonify([])

@app.route('/clips/<clipId>/userRatings&<userId>', methods=['POST'])
def userRatings(clipId, userId):
    try:
        return jsonify(db.getClipUserRatings(clipId, userId))
    except:
        print("EXCEPTION: Could not retrive user ratings for clip", clipId, "and user", userId)
        return jsonify([])

@app.route('/clips/<clipId>')
def clips(clipId):
    from models import Clip
    clip = db.getClipById(clipId)
    clipJson = json.dumps(clip.asList())
    return render_template('clip.html', clipData=clipJson, clipTitle="Placeholder", categories=json.dumps(db.getCategories()))

# input rating into Ratings table upon user post request
@app.route('/updateRating/<clipId>&<userId>&<categoryId>&<rating>', methods=['POST'])
def inputRating(clipId, userId, categoryId, rating):
    # connect to db and send command
    print('input received')
    return db.updateRating(clipId, userId, categoryId, rating)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        # authenticate(User)
        db.loginUser(request.form['username'], request.form['password'], request.form.get('remember_me'))
        return redirect(url_for('index'))
    return render_template('login.html', loginForm=loginForm)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        # Sign up the user
        db.signUpUser(request.form['signUpUsername'], request.form['email'], request.form['signUpPassword'], request.form.get('weapon'))
        return redirect(url_for('login'))
    return render_template('signup.html', signUpForm=signUpForm)

# initialize contact form
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, validators
from wtforms.widgets import TextArea
class ContactForm(FlaskForm):
    reasonsForContact = [('casual', 'Just saying hi!'),\
                        ('job', 'Looking for a job'),\
                        ('partnership', 'Business partnership'),\
                        ('correction', 'Something\'s missing/incorrect')]
    name    = StringField('Name')
    email   = StringField('Email (if desired)', [validators.Email(), validators.Length(min=6, max=35)])
    reason  = SelectField('Reason for reaching out', choices = reasonsForContact)
    content = StringField('Content', widget=TextArea())
    submit  = SubmitField('Submit')

# loads contact page
@app.route('/contact')
def contact():
    contactForm = ContactForm()
    if contactForm.validate_on_submit():
        from flask import flash
        flash('Thanks for your input. We\'ll be in touch!')
        # TODO somehow send messages
        return redirect(url_for('index'))
    return render_template('contact.html', contactForm=contactForm)

'''# loads About page
@app.route('/about')
def about():
    return render_template('about.html')'''

