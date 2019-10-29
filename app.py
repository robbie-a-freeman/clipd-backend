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

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# loads home
@app.route('/')
@app.route('/home')
@app.route('/index')
def changelog():
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

@app.route("/testreact")
def testreact():
    return render_template('test-react.html')

@app.route("/signup")
def testreact():
    return render_template('test-react.html')
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
