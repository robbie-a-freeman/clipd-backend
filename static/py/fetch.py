"""Grabs the appropriate elements for various pages and returns them.
"""

import glob
import os
from bs4 import BeautifulSoup as bs

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

""" Grabs 3 articles, as well as their pictures, and returns them in a list of
    ArticlePreview objects
"""
def fetchHomePage():
    articles = glob.glob("templates/articleFiles/*")
    articles.sort(key=os.path.getmtime, reverse=True)
    for a in articles:
        page = bs(a, 'html.parser')
        print(page.find(id="title"))

    print(articles)

""" Class that represents an article preview. Does nothing but contain the
    picture, title, subtitle, link, and name.
"""
class ArticlePreview:
    def __init__(self, picture, title, subtitle, link, name):
        self.picture = picture
        self.title = title
        self.subtitle = subtitle
        self.link = link
        self.name = name
