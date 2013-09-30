import scraperwiki

# Blank Python

'''
Created on 23.03.2013

@author: Thomas
'''

class HnFeedItem(object):
    
    '''
    classdocs
    '''

    def __init__(self):
        
        '''
        Constructor
        '''
        
        self.set_link_to_comments("");
        self.set_link_to_post("")
        self.set_title("")
        self.set_time_stamp("")
    
    def set_link_to_post(self, link):
        
        self._link_to_post = link
        
    def get_link_to_post(self):
        
        return self._link_to_post
    
    def set_link_to_comments(self, link):
        
        self._link_to_comments = link
        
    def get_link_to_comments(self):
        
        return self._link_to_comments
    
    def set_title(self, title):
        
        self._title = title
        
    def get_title(self):
        
        return self._title
    
    def set_time_stamp(self, time_stamp):
        
        self._time_stamp = time_stamp
        
    def get_time_stamp(self):
        
        return self._time_stamp
    
    def get_as_dict(self):
        
        item_as_dict = { 
              "time" : self._time_stamp, 
              "title" : self._title, 
              "post" : self._link_to_post,
              "comments" : self._link_to_comments
              }

        return item_as_dict
    
    def __str__(self):
        
        return "time:" + str(self._time_stamp) + ", " + "title: " + str(self._title) + ", " +  "link_to_post: " + str(self._link_to_post) + ", " +  "link_to_comments: " + str(self._link_to_comments)

    def __eq__(self, other):
            
        if(type(other) != type(self)):
            return False;
        
        if(other._link_to_post == self._link_to_post):
            return True;
        
        return False;

'''
Created on 23.03.2013

@author: Thomas
'''

import feedparser
import os.path
import csv
import time 
import scraperwiki

class HnScraper(object):
    
    '''
    Usage
        1 - make a new instance
        2 - if an old history file exists, it will be read in
        3 - read feed
        4 - copy items from feed to list (only new items will be copied)
        5 - save to CSV-file
        6 - repeat a little bit later ;) 
    '''
    
    def __init__(self, history_file_name = "hn_rss_history.csv"):
        
        '''
        Constructor
        '''
        
        self._rss_urL = "https://news.ycombinator.com/rss"
        self._items = []
        
        # read about the history so you never forget where you came from
        if(os.path.isfile(history_file_name)):
            self.read_in_history(history_file_name)
            
    def read_in_history(self, history_file_name = "hn_rss_history.csv"):
        
        copied_items = 0
        
        with open(history_file_name, 'rb') as csvfile:
            
            csv_reader = csv.reader(csvfile, delimiter=';')
            
            for row in csv_reader:
                
                tmp = HnFeedItem()
                tmp.set_time_stamp(row[0])
                tmp.set_title(row[1])
                tmp.set_link_to_post(row[2])
                tmp.set_link_to_comments(row[3])

                if(not (tmp in self._items)):
                    self._items.append(tmp)
                    copied_items += 1
                    
            return copied_items
                    
    def copy_items_from_feed(self):
        
        copied_items = 0
        
        for item in self._feed[ "items" ]:
            
            title = item[ "title" ]
            link_to_post = item[ "link" ]
            link_to_comments = item[ "comments" ]
            
            tmp = HnFeedItem()
            tmp.set_time_stamp(time.time())
            tmp.set_title(title)
            tmp.set_link_to_post(link_to_post)
            tmp.set_link_to_comments(link_to_comments)
            
            if(not (tmp in self._items)):
                self._items.append(tmp)
                copied_items += 1
                
        return copied_items

    def read_feed(self):
        
        self._feed = feedparser.parse( self._rss_urL )
        
    def is_feed_well_formed(self):

        if self._feed[ "bozo" ] == 1:
            return False
        return True
    
    def get_feed_url(self):
        
        return self._rss_urL
    
    def get_number_of_items(self):
        
        return len(self._items)
    
    def get_number_of_items_in_feed(self):
        
        return len(self._feed[ "items" ])
    
    def get_feed_name(self):
        
        return self._feed[ "channel" ][ "title" ] 
    
    def print_items(self):
        
        for item in self._items:
            print item
            
    def print_items_in_feed(self):
        
        for item in self._feed[ "items" ]:
            print item
     
    def get_items(self):

        return self._items
    
    def write_items_to_csv(self, history_file_name = "hn_rss_history.csv"):
            
        history_file = open(history_file_name, "w") 
        
        for item in self.get_items(): 
            history_file.write(str(item.get_time_stamp()) + ";" + item.get_title() + ";" + item.get_link_to_post() + ";" + item.get_link_to_comments() + ";\n") 
        
        history_file.close()
    
    def copy_items_from_feed_directly_to_scraper_wiki(self):
        
        copied_items = 0
        
        for item in self._feed[ "items" ]:
            
            title = item[ "title" ]
            link_to_post = item[ "link" ]
            link_to_comments = item[ "comments" ]
            
            tmp = HnFeedItem()
            tmp.set_time_stamp(time.time())
            tmp.set_title(title)
            tmp.set_link_to_post(link_to_post)
            tmp.set_link_to_comments(link_to_comments)
 
            contains = False

            try:
                contains = len(scraperwiki.sqlite.execute("select post from hn where post = '" + tmp.get_link_to_post() + "'")[ "data" ]) != 0
            except:
                print "on the first run, the table might not exist"

            if(not contains):
                copied_items += 1
                print "save new data"
                scraperwiki.sqlite.save(unique_keys=["post"], data = tmp.get_as_dict(), table_name = "hn")
                
        return copied_items

scraper = HnScraper()

start = time.time()

# (start + 120) > time.time()
while(True):
    scraper.read_feed()
    scraper.copy_items_from_feed_directly_to_scraper_wiki()
    time.sleep(120)import scraperwiki

# Blank Python

'''
Created on 23.03.2013

@author: Thomas
'''

class HnFeedItem(object):
    
    '''
    classdocs
    '''

    def __init__(self):
        
        '''
        Constructor
        '''
        
        self.set_link_to_comments("");
        self.set_link_to_post("")
        self.set_title("")
        self.set_time_stamp("")
    
    def set_link_to_post(self, link):
        
        self._link_to_post = link
        
    def get_link_to_post(self):
        
        return self._link_to_post
    
    def set_link_to_comments(self, link):
        
        self._link_to_comments = link
        
    def get_link_to_comments(self):
        
        return self._link_to_comments
    
    def set_title(self, title):
        
        self._title = title
        
    def get_title(self):
        
        return self._title
    
    def set_time_stamp(self, time_stamp):
        
        self._time_stamp = time_stamp
        
    def get_time_stamp(self):
        
        return self._time_stamp
    
    def get_as_dict(self):
        
        item_as_dict = { 
              "time" : self._time_stamp, 
              "title" : self._title, 
              "post" : self._link_to_post,
              "comments" : self._link_to_comments
              }

        return item_as_dict
    
    def __str__(self):
        
        return "time:" + str(self._time_stamp) + ", " + "title: " + str(self._title) + ", " +  "link_to_post: " + str(self._link_to_post) + ", " +  "link_to_comments: " + str(self._link_to_comments)

    def __eq__(self, other):
            
        if(type(other) != type(self)):
            return False;
        
        if(other._link_to_post == self._link_to_post):
            return True;
        
        return False;

'''
Created on 23.03.2013

@author: Thomas
'''

import feedparser
import os.path
import csv
import time 
import scraperwiki

class HnScraper(object):
    
    '''
    Usage
        1 - make a new instance
        2 - if an old history file exists, it will be read in
        3 - read feed
        4 - copy items from feed to list (only new items will be copied)
        5 - save to CSV-file
        6 - repeat a little bit later ;) 
    '''
    
    def __init__(self, history_file_name = "hn_rss_history.csv"):
        
        '''
        Constructor
        '''
        
        self._rss_urL = "https://news.ycombinator.com/rss"
        self._items = []
        
        # read about the history so you never forget where you came from
        if(os.path.isfile(history_file_name)):
            self.read_in_history(history_file_name)
            
    def read_in_history(self, history_file_name = "hn_rss_history.csv"):
        
        copied_items = 0
        
        with open(history_file_name, 'rb') as csvfile:
            
            csv_reader = csv.reader(csvfile, delimiter=';')
            
            for row in csv_reader:
                
                tmp = HnFeedItem()
                tmp.set_time_stamp(row[0])
                tmp.set_title(row[1])
                tmp.set_link_to_post(row[2])
                tmp.set_link_to_comments(row[3])

                if(not (tmp in self._items)):
                    self._items.append(tmp)
                    copied_items += 1
                    
            return copied_items
                    
    def copy_items_from_feed(self):
        
        copied_items = 0
        
        for item in self._feed[ "items" ]:
            
            title = item[ "title" ]
            link_to_post = item[ "link" ]
            link_to_comments = item[ "comments" ]
            
            tmp = HnFeedItem()
            tmp.set_time_stamp(time.time())
            tmp.set_title(title)
            tmp.set_link_to_post(link_to_post)
            tmp.set_link_to_comments(link_to_comments)
            
            if(not (tmp in self._items)):
                self._items.append(tmp)
                copied_items += 1
                
        return copied_items

    def read_feed(self):
        
        self._feed = feedparser.parse( self._rss_urL )
        
    def is_feed_well_formed(self):

        if self._feed[ "bozo" ] == 1:
            return False
        return True
    
    def get_feed_url(self):
        
        return self._rss_urL
    
    def get_number_of_items(self):
        
        return len(self._items)
    
    def get_number_of_items_in_feed(self):
        
        return len(self._feed[ "items" ])
    
    def get_feed_name(self):
        
        return self._feed[ "channel" ][ "title" ] 
    
    def print_items(self):
        
        for item in self._items:
            print item
            
    def print_items_in_feed(self):
        
        for item in self._feed[ "items" ]:
            print item
     
    def get_items(self):

        return self._items
    
    def write_items_to_csv(self, history_file_name = "hn_rss_history.csv"):
            
        history_file = open(history_file_name, "w") 
        
        for item in self.get_items(): 
            history_file.write(str(item.get_time_stamp()) + ";" + item.get_title() + ";" + item.get_link_to_post() + ";" + item.get_link_to_comments() + ";\n") 
        
        history_file.close()
    
    def copy_items_from_feed_directly_to_scraper_wiki(self):
        
        copied_items = 0
        
        for item in self._feed[ "items" ]:
            
            title = item[ "title" ]
            link_to_post = item[ "link" ]
            link_to_comments = item[ "comments" ]
            
            tmp = HnFeedItem()
            tmp.set_time_stamp(time.time())
            tmp.set_title(title)
            tmp.set_link_to_post(link_to_post)
            tmp.set_link_to_comments(link_to_comments)
 
            contains = False

            try:
                contains = len(scraperwiki.sqlite.execute("select post from hn where post = '" + tmp.get_link_to_post() + "'")[ "data" ]) != 0
            except:
                print "on the first run, the table might not exist"

            if(not contains):
                copied_items += 1
                print "save new data"
                scraperwiki.sqlite.save(unique_keys=["post"], data = tmp.get_as_dict(), table_name = "hn")
                
        return copied_items

scraper = HnScraper()

start = time.time()

# (start + 120) > time.time()
while(True):
    scraper.read_feed()
    scraper.copy_items_from_feed_directly_to_scraper_wiki()
    time.sleep(120)