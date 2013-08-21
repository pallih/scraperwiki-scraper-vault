import scraperwiki

# Blank Python

import scraperwiki

# Blank Python

__author__ = 'bmihelic'

import scraperwiki
import lxml.html
import time
import types
import re
import urllib2
import datetime
import dateutil.parser
import httplib
import codecs

class web_article(object):

    def __init__(self, url):
        # Set initial url variable as url to webpage
        self.url = url
        # Set initial tree variable to parse html
        self.tree = self.parse()
        # Create raw data dictionary:
        # This dictionary is to hold database data (including the metadata file)
        # The purpose of this dictionary is primarily for ease of viewing when examining extracted data
        # Each key has a value of either a string or a list of strings
        self.raw = {}

    # Parses html at url and returns tree, called at initiation
    def parse(self):
        # grab html web page
        tries = 0
        while tries < 5:
            try:
                connect = urllib2.urlopen(self.url)
                try:
                    html = connect.read()
                except  httplib.IncompleteRead:
                    print 'Incomplete Read'
                    return None
                # create tree
                tree = lxml.html.fromstring(html)
                return tree
            except urllib2.URLError:
                tries += 1

        print 'Tried to open page at %s %d times and failed.  Giving up...' % (self.url, tries)
        return None

    # Reloads new html tree and url given new url
    def change_page(self, new_url):
        self.url = new_url
        self.tree = self.parse()

    # Setters

    # Sets url
    def set_url(self, new_url):
        self.url = new_url

    # Sets tree
    def set_tree(self, new_tree):
        self.tree = new_tree

    # Sets a given raw dictionary key and associates it with a given value
    def set_raw_value(self, raw_key, raw_value):
        if raw_value != '':
            if isinstance(raw_value, types.ListType):
                formatted_raw_value = []
                for list_entry in raw_value:
                    raw_value_formatter = string_formatter(list_entry)
                    raw_value_formatter.replace_chars("'", '')
                    list_entry = raw_value_formatter.get_string()
                    formatted_raw_value.append(list_entry)
            else:
                raw_value_formatter = string_formatter(raw_value)
                raw_value_formatter.replace_chars("'", '')
                formatted_raw_value = raw_value_formatter.get_string()

            self.raw[raw_key] = formatted_raw_value

    # Getters

    # Returns url
    def get_url(self):
        return self.url

    # Returns tree
    def get_tree(self):
        return self.tree

    # Returns raw dictionary
    def get_raw(self):
        return self.raw

    # Returns raw dictionary value associated with a given dictionary key
    def get_raw_value(self, raw_key):
        return self.raw[raw_key]

class extractor(object):

    def __init__(self, article):
        self.article = article

    def get_article(self):
        return self.article

    def set_article(self, article):
        self.article = article

    # Returns a list of values given a cssselect selector combination
    def extract_list(self, selector):
        tree = self.article.get_tree()
        # Extract information
        elements = tree.cssselect(selector)
        return elements

    # Returns the first value in a list determined by a cssselect selector combination
    def extract(self, selector):
        # Extract information
        elements = self.extract_list(selector)
        if len(elements) > 0:
            return elements[0]

    # Loops through article pages and extracts body text from each page
    def extract_body_text(self):
        article_navigator = navigator(self.article)
        body_text = []
        final_text = ''
        # Loop through pages
        while True:
            # Extract body text
            paragraphs = self.extract_list('article p')
            for paragraph in paragraphs:
                paragraph = paragraph.text_content()
                body_text.append(paragraph)
            stop = article_navigator.go_to_next_page()
            # If no more pages:
            if stop == 'stop':
                final_text = ''.join(body_text)
                break
        if final_text:
            self.article.set_raw_value('body_text', final_text)
        else:
            self.article.set_keeper(False)

# This class is for formatting strings in order to be placed in dictionaries or sent to databases
class string_formatter(object):

    def __init__(self, string):
        self.string = string

    def get_string(self):
        return self.string

    def set_string(self, new_string):
        self.string = new_string

    # Replaces chars in bad_cars with new_char
    def replace_chars(self, bad_chars, new_char):
        for char in bad_chars:
            new_string = self.string.replace(char, new_char)
        self.string = new_string

    def fix_data(self):
        self.replace_chars("''(),", '')
        self.replace_chars('&', 'and')

    # Turns string into list given splitter and deletes any list entries past given limit
    def to_list(self, splitter, limit):
        list = self.string.split(splitter, limit)
        if len(list) > limit:
            del list[limit]
        self.set_string(list)

# This class is for formatting dates and times in order to be ingested into Savanna
class date_time_formatter(object):

    def __init__(self, date_time):
        self.date_time = date_time

    def get_date_time(self):
        return self.date_time

    def set_date_time(self, new_date_time):
        self.date_time = new_date_time

    # For general formats, parses dates
    def parse_date(self):
        parsed_date = dateutil.parser.parse(self.date_time).date()
        self.date_time = str(parsed_date)

    # Converts date_time to ISO formatted date: 'YYYY-MM-DD'
    def to_iso(self, format):
        structured_date = time.strptime(self.date_time, format)
        year = int(time.strftime('%Y', structured_date))
        month = int(time.strftime('%m', structured_date))
        day = int(time.strftime('%d', structured_date))
        date = datetime.date(year, month, day)
        iso_date = date.isoformat()
        self.date_time = str(iso_date)

    # Takes datetime in ISO format and changes to savanna date_time, times must include hours, mins, and secs
    def to_savanna(self):
        if 'T' in self.date_time:
            savanna_tail = '.000Z'
        else:
            savanna_tail = 'T00:00:00.000Z'
        savanna_date = self.date_time + savanna_tail
        self.date_time = savanna_date

    # Gets current time
    def to_current(self):
        current_date_time = time.strftime('%Y-%m-%dT%H:%M:%S')
        self.date_time = current_date_time

    # Checks against yesterdays date, returns true if date matches yesterdays
    def is_yesterday(self):
        yesterday = str(datetime.date.today() - datetime.timedelta(days = 1))
        if self.date_time == yesterday:
            return True
        else:
            return False

# This class is for sending dictionary information to the scraperwiki database, given an article and the scraper name
# to be used in making database table names
class exporter(object):

    def __init__(self, article, scraper_name):
        self.article = article
        self.scraper_name = scraper_name

    def get_article(self):
        return self.article

    def get_scraper_name(self):
        return self.scraper_name

    def set_article(self, article):
        self.article = article

    def set_scraper_name(self, new_scraper_name):
        self.scraper_name = new_scraper_name

    def delete_row(self, table_name):
        scraperwiki.sqlite.execute("DELETE FROM %s_%s WHERE id = '%s'" % (self.scraper_name, table_name, self.article.get_id()))

    def check_database(self, table_name):
        article = scraperwiki.sqlite.select("* FROM %s_%s WHERE id = '%s'" % (self.scraper_name, table_name, self.article.get_id()))
        if len(article) > 0:
            return True
        else:
            return False

    # Makes new row in database with url as id
    def make_row(self, table_name):
        if self.check_database(table_name):
            self.delete_row(table_name)
        scraperwiki.sqlite.execute("INSERT INTO %s_%s (id) VALUES ('%s')" % (self.scraper_name, table_name, self.article.get_id()))
        scraperwiki.sqlite.commit()

    # Stores raw dictionary
    def export_raw(self):
        raw = self.article.get_raw()
        id = self.article.get_id()
        self.make_row('raw')
        # Loops through raw dictionary keys and stores value in new row
        # Lists are stored as strings separated by ' | '
        for raw_key in raw:
            raw_value = raw[raw_key]
            if isinstance(raw_value, types.ListType):
                raw_value = ' | '.join(raw_value)
            scraperwiki.sqlite.execute("UPDATE %s_raw SET %s = '%s' WHERE id = '%s'" % (self.scraper_name, raw_key, raw_value, id))
        scraperwiki.sqlite.commit()

    # The following methods create the required raw and entities tables:

    def create_raw_table(self):
        table_name = '%s_raw' % self.scraper_name
        scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS %s (
                                        id TEXT,
                                        published_date TEXT,
                                        author TEXT,
                                        topic_regions TEXT,
                                        publication_type TEXT,
                                        source_url TEXT,
                                        title TEXT,
                                        document_type TEXT,
                                        pdf longblob,
                                        body_text TEXT,
                                        extraction_date TEXT,
                                        publisher TEXT,
                                        distributor TEXT,
                                        keywords TEXT,
                                        metadata_file TEXT,
                                        article_image LONGBLOB,
                                        article_image_caption TEXT)""" % table_name)
        scraperwiki.sqlite.commit()

    def drop_table(self, table_name):
        scraperwiki.sqlite.execute('DROP TABLE IF EXISTS %s' % table_name)

class navigator(object):

    def __init__(self, article):
        # Current article
        self.article = article
        # Root url to be used to finish url fragments found in 'href' attributes of 'a' elements
        self.root_url = 'http://www.washingtonpost.com'
        # List of link objects on page, to be filled if needed
        self.links = []
        # List of linked_articles made from links list, to be filled if needed
        self.linked_articles = []

    # Returns current article object
    def get_article(self):
        return self.article

    # Returns links list
    def get_links(self):
        return self.links

    # Returns list of linked articles
    def get_linked_articles(self):
        return self.linked_articles

    # Changes current article
    def set_article(self, new_article):
        self.article = new_article

    # Clicks on a link in the article and assigns the resulting article given an 'a' object
    def click(self, a):
        new_url = a.attrib['href']
        if 'http://' not in new_url:
            new_url = self.root_url + new_url
        self.article.change_page(new_url)

    # Clicks on link to next page in current article if it exists, otherwise returns 'stop'
    def go_to_next_page(self):
        next_extractor = extractor(self.article)
        next_selector = 'a.next-page'
        next = next_extractor.extract(next_selector)
        if next is not None:
            self.click(next)
        else:
            return 'stop'

    # Gathers links on root page and returns a list of urls given selector to links
    def gather_links(self, link_selector):
        link_extractor = extractor(self.article)
        link_list = link_extractor.extract_list(link_selector)
        print 'found %d links:' % len(link_list)
        for link in link_list:
            print link.text
            # Remove blog articles
            if '/blogs/' not in link.attrib['href']:
                self.links.append(link)
            else:
                print 'link removed'

    # Creates articles from each link in links list and stores them in linked_articles
    def links_to_articles(self):
        i = 0
        for link in self.links:
            self.click(link)
            linked_article = web_article(self.article.get_url())
            if self.article.get_tree() is not None:
                self.linked_articles.append(linked_article)
                i += 1
        print 'got %d new articles:' % i
        for article in self.linked_articles:
            print article.get_url()

    # Gathers all links and creates articles from them
    def gather_linked_articles(self, link_selector):
        self.gather_links(link_selector)
        self.links_to_articles()

# This is the main function.  For each article on the new york times, it extracts the body text and any relevant data,
# writes a metadata file for the article and sends everything to the scraperwiki database.
def extract_all_articles():
    # Set root url
    url = 'http://www.washingtonpost.com/'
    # Make root page
    root_page = web_article(url)
    # Create navigator for getting categories on root page
    root_navigator = navigator(root_page)
    # Gather all top headlines
    root_navigator.gather_linked_articles('div[class="wp-row "] div[class="wp-column five"] li a[class="icon link-type article"]')
    # For each article
    for news_article in root_navigator.linked_articles:
        data_extractor = extractor(news_article)
        data_extractor.extract_all_data()
    root_navigator.save_keepers()
    for news_article in root_navigator.linked_articles:
        # Make a metadata writer object to write the metadata file
        meta_writer = metadata_writer(news_article)
        # Write the metadata file
        meta_writer.write_metadata_file()
        # Make news exporter object to send data to database
        news_exporter = exporter(news_article, 'washington_post_good')
        # Drop database tables
        #news_exporter.drop_tables()
        # Create database tables
        news_exporter.create_tables()
        # Export data to database
        news_exporter.export_all_data()
        # Export data to file
        #news_exporter.export_to_file()
        print news_article.get_raw_value('metadata_file')
        print news_article.get_raw_value('body_text')

extract_all_articles()