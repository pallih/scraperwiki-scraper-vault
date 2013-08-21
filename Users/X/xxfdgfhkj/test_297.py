import scraperwiki
import datetime
import json
import re
import urllib2
import importlib
import sys
sys.path.append(".")

ranks = None


# name, points, nation, imgquery


def save(sport, arr, table):
    scraperwiki.sqlite.save(unique_keys=['s'], data={ 's':  sport, 'd': json.dumps(arr[:10])}, table_name=table)
    scraperwiki.sqlite.save(unique_keys=['s'], data={ 's':  sport, 'd': json.dumps(arr)}, table_name=table+"_all")

def fetch(url):
    return scraperwiki.scrape(url, None, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4')



def import_libs(f):

    def f1(*args, **kwargs):
        global ranks
        if  not ranks:
            u = urllib2.urlopen('https://raw.github.com/lcweb/ranks/master/server/ranks.py')
            localFile = open('ranks.py', 'w')
            localFile.write(u.read())
            localFile.close()
            ranks = importlib.import_module('ranks')
            f(*args, **kwargs)

    return f1    


@import_libs
def main():
    
    cats = ranks.cats()
    scraperwiki.sqlite.save(unique_keys=['cats'], data={'cats': json.dumps(cats)}, table_name="cats")

    ff = ranks.ff()

    for f in ff:
        html = fetch(f(burl=True))
        arr = f(html=html)
        save(f(bsport=True), arr, f(bcat=True))    



main()




