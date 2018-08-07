"""Grabs the appropriate elements for various pages and returns them.
"""

import glob
import os

__author__ = "Robbie Freeman"
__credits__ = ["Robbie Freeman"]
__maintainer__ = "Robbie Freeman"
__email__ = "robbie.a.freeman@gmail.com"
__status__ = "Development"

""" Grabs 3 articles, as well as their pictures, and returns them in a list
"""
def fetchHomePage():
    articles = glob.glob("*.txt")
    files.sort(key=os.path.getmtime)

""" Class that represents an article preview. Does nothing but contain the
    picture, title, subtitle, and link.
"""
class ArticlePreview:
    def __init__(self, picture, title, subtitle, link):
        self.picture = picture
        self.title = title
        self.subtitle = subtitle
        self.link = link
