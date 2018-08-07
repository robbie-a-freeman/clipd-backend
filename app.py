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

app = Flask(__name__)

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

# calls the app so it can run
if __name__ == "__main__":
    app.run()

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def changelog():
    return render_template('index.html')

# basic 404 page. Hopefully isn't called all that often TODO: implement
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# loads About page
@app.route('/about')
def about():
    return render_template('about.html')

# loads the page with list of articles TODO implement
@app.route('/article/<string>')
def article():
    return render_template('index.html')

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
