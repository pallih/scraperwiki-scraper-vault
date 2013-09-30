"""
We'll scrape http://popcorn.oneindia.in/ to get a list of movies, actors, and their association.

"""

import scraperwiki
import lxml.html

def get_movies(letter):
    html = scraperwiki.scrape('http://popcorn.oneindia.in/browse/' + letter + '/2/browse-movies.html')
    root = lxml.html.fromstring(html)
    for el in root.cssselect("td a"): 
        if el.attrib['href'].startswith('/title/'):
            yield el.attrib['href']


def main():
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        get_movies(letter)
    get_movies('0-9')


for movie in get_movies('A'):
    print movie

# I will complete this with the Gramener team on the 9th or 10th of May, 2012
"""
We'll scrape http://popcorn.oneindia.in/ to get a list of movies, actors, and their association.

"""

import scraperwiki
import lxml.html

def get_movies(letter):
    html = scraperwiki.scrape('http://popcorn.oneindia.in/browse/' + letter + '/2/browse-movies.html')
    root = lxml.html.fromstring(html)
    for el in root.cssselect("td a"): 
        if el.attrib['href'].startswith('/title/'):
            yield el.attrib['href']


def main():
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        get_movies(letter)
    get_movies('0-9')


for movie in get_movies('A'):
    print movie

# I will complete this with the Gramener team on the 9th or 10th of May, 2012
