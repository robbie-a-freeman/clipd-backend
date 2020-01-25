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
sys.path.insert(0, 'srv')
from database import DB
try:
    db = DB(DATABASE_URL, SSL_MODE)
    print("connected to postgres!")
except:
    print("not connected to postgres! error:", sys.exc_info()[1])

# setting up email variables
from flask_mail import Mail, Message
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'robbie.a.freeman@gmail.com',
	MAIL_PASSWORD = 'rorodog811',
    MAIL_DEFAULT_SENDER = 'robbie.a.freeman@gmail.com'
	)
mail = Mail(app)

# setting up secret key
# TODO make this environment var
#app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.secret_key = b'\xd2\xc7\xdd\xa4\xd7\xc7\xfb\x92\x88\x15\xbbF,3\xc7\x9d'

# setting up Flask-Login manager
from flask_login import LoginManager, login_required, login_user, logout_user
login_manager = LoginManager()
login_manager.init_app(app)

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
#algolia.initializeClipsIndex(db)

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

# initialize login form stuff
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, validators
class LoginForm(FlaskForm):
    username    = StringField('Username')
    password    = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Submit')

# initialize sign up form stuff
class SignUpForm(FlaskForm):
    from models import Weapon
    listWeaponChoices = db.getWeaponTypes()
    # for reasons required by WTForms
    weaponChoices = list(map(lambda x:(x,x), listWeaponChoices))
    signUpUsername = StringField('Username', [validators.Length(min=4, max=25)])
    email          = StringField('Email Address', [validators.Email(), validators.Length(min=6, max=35)])
    signUpPassword = PasswordField('Password', [validators.Length(min=4, max=35)])
    weapon         = SelectField('Favorite Weapon', choices = weaponChoices)
    signUpSubmit   = SubmitField('Submit')

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
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
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contactForm = ContactForm()
    if contactForm.validate_on_submit():
        from flask import flash
        try:
            subject = "Clip'd request form: " + request.form["reason"] + " - " + request.form["name"]
            msg = Message(subject, \
            recipients=["robbie.a.freeman@gmail.com"])
            msg.body = request.form["content"] + "\n\n Sender email:" + request.form["email"]
            mail.send(msg)
            flash('Thanks for your input. We\'ll be in touch!')
            print("Message sent")
        except:
            flash('Sorry, message failed to send. Try again later!')
            print("Message failed to send, exception: ", sys.exc_info()[1])
        return redirect(url_for('index'))
    return render_template('contact.html', contactForm=contactForm)

@app.route('/maps/<mapId>')
def maps(mapId):
    mapObj = db.getMapById(mapId)
    print("name,", mapObj.name)
    return render_template('category.html', catTitle=mapObj.name, catType="maps", catInfo=mapObj.asList())
    
@app.route('/events/<eventId>')
def events(eventId):
    eventObj = db.getEventById(eventId)
    print("name,", eventObj.name)
    return render_template('category.html', catTitle=eventObj.name, catType="events", catInfo=eventObj.asList())
    
@app.route('/players/<playerId>')
def players(playerId):
    playerObj = db.getPlayerById(playerId)
    print("name,", playerObj.alias)
    return render_template('category.html', catTitle=playerObj.alias, catType="players", catInfo=playerObj.asList())
    
@app.route('/weapons/<weaponId>')
def weapons(weaponId):
    weaponObj = db.getWeaponById(weaponId)
    print("name,", weaponObj.name)
    return render_template('category.html', catTitle=weaponObj.name, catType="weapons", catInfo=weaponObj.asList())
    
@app.route('/organizers/<organizerId>')
@app.route('/organisers/<organizerId>') # lol British English
def organizers(organizerId):
    organizerObj = db.getOrganizerById(organizerId)
    print("name,", organizerObj.name)
    return render_template('category.html', catTitle=organizerObj.name, catType="organizers", catInfo=organizerObj.asList())
    
@app.route('/teams/<teamId>')
def teams(teamId):
    teamObj = db.getTeamById(teamId)
    print("name,", teamObj.alias)
    return render_template('category.html', catTitle=teamObj.alias, catType="teams", catInfo=teamObj.asList())

'''# loads About page
@app.route('/about')
def about():
    return render_template('about.html')'''

