# FB Directory Scraper
# Mencius, 2013-02-26


"""


"""

import scraperwiki

import lxml.html
from urlparse import urlparse
import re
import pickle
import json

class Crawler():
    
    def __init__(self):
        self.css_dir = "div li.fbDirectoryBoxColumnItem a"
        self.css_fbpage = "table.mam tbody tr td div div div div a"
        self.visited = set()
        self.dir_pages = set()
        self.fb_pages = list()
        self.depth_max = 3
        self.depth = 0
        try:
            self.last_visited = self.get_lastdir()
            print (self.last_visited)
        except:
            self.last_visited = list()
            print("No last save")
    
    def get_lastdir(self):
        try:
            return(pickle.loads(scraperwiki.sqlite.get_var('last_visited')))
            
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)

    def filter_page(self, url):
        #filter1: returns FBpage's unique name, otherwise return false
        parse_url = urlparse(url)
        p = re.compile('/pages/')
        directory = p.findall(parse_url.path)
        if (len(directory) > 0):
            return False
        else:
            return re.sub('[./]', '', parse_url.path)

        #define filters here. 
        #ex) only return true if the fb_page has X likes. 
    
    def get_pagedata(self, fbID):
        graph_page = "http://graph.facebook.com/"+fbID
        print("checking out " + graph_page)
        purge = scraperwiki.scrape(graph_page)
        return json.loads(purge)
        

    def is_directory(self, url):
        parse_url = urlparse(url)
        p = re.compile('/directory/')
        directory = p.findall(parse_url.path)
        directory
        if (len(directory) > 0):
            return True
        else:
            return False

    def scrape_page(self, url):
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        return root

    def find_dirs(self, root):
        return root.cssselect(self.css_dir)

    def find_pages(self, root):
        return root.cssselect(self.css_fbpage)


    def depth_first(self, url):
        print("Looking at: "+ url)
        #if (url not in self.last_visited): 
        print("url not found")
        root = self.scrape_page(url)
        found_dirs = self.find_dirs(root)
        print(found_dirs)
        #if it's a directory of more directories, keep crawling

        if (found_dirs):      
            for link in found_dirs:
                if link not in self.visited:
                    new_url = link.attrib['href']
                    self.depth_first(new_url)
                
        else:
        #otherwise, find the pages the directory lists, and add them
        #to the db
     
            print("did not find dirs")   
            found_pages = self.find_pages(root)
            
            for link in found_pages:
                found_page = link.attrib['href']
                pageID = self.filter_page(found_page)
                if (pageID != False):
                    #self.fb_pages.append(found_page)
                    data = {'id': pageID,
                            'url': found_page}
                    #data.update(self.get_pagedata(pageID))
                    scraperwiki.sqlite.save(unique_keys=['id', 'url'], data=data)
            
            #store 
        self.visited.add(url)
        scraperwiki.sqlite.save_var('last_visited', pickle.dumps(self.visited))
        

    def crawl(self, url):
        self.depth_first(url)

c = Crawler()
url = "http://www.facebook.com/directory/pages/A"
c.crawl(url)

