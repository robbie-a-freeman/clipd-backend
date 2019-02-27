"""Controls the web server for the entire site with a Flask framework. Assumes
that the main app is app.py. Contains links to the rest of the site, and it
handles non-static downloads.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import json
from flask import abort
from flask import redirect
from flask import url_for
from flask import send_file

import os
import sys
sys.path.insert(0, 'static/py')

import fetch

from flaskext.mysql import MySQL

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# calls the app so it can run
if __name__ == "__main__":
    app.run()

# MySQL configurations - source: https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rorodog811'
app.config['MYSQL_DATABASE_DB'] = 'csgo_highlights'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute('''SELECT * FROM videos''')
data = cursor.fetchall()
print (data)

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def changelog():
    fetch.fetchHomePage()
    return render_template('history.html')

# basic 404 page. Hopefully isn't called all that often TODO: implement
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# loads About page
@app.route('/about')
def about():
    return render_template('about.html')

# loads the page with list of articles TODO implement
@app.route('/article/<query>')
def article(query):
        return render_template('articleFiles/' + query + '.html')

# loads the page with list of articles TODO get rid of
@app.route('/article')
def exArticle():
    return render_template('article.html')

# loads the page with list of articles TODO implement
@app.route('/articles')
def articles():
    return render_template('index.html')

# loads contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# loads Hall of History page
@app.route('/history')
def history():
    return render_template('history.html')

# loads Smoke Stop page
@app.route('/smokestop')
def smokestop():
    return render_template('smokestop.html')
