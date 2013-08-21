__author__ = 'bmihelic'

import scraperwiki
import lxml.html
import time
import types
import re
import urllib2
import datetime
import dateutil.parser
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
        # Create entities dictionary: 
        # This dictionary is to hold entity types paired with dictionaries of paired entity text and entity probability information
        self.entities = {}
        # Create empty metadata dictionary:
        # This dictionary holds information that will be written to the metadata file
        # Each key has a value of a dictionary of facetvalues and the facetkey's MultiValued setting (if applicable)
        # Each facetvalue value is either a string or a list of strings
        # Each multivalue is either 'true' or 'false'
        self.metadata = {}
        # Create empty id: This will be used to identify article entries in database
        self.id = ''
        # Create variable to indicate whether article is a keeper
        self.keeper = True

    # Parses html at url and returns tree, called at initiation
    def parse(self):
        # grab html web page
        print self.url
        try:
            html = urllib2.urlopen(self.url).read()
        except urllib2.URLError:
            try:
                html = urllib2.urlopen(self.url).read()
            except urllib2.URLError:
                try:
                    html = urllib2.urlopen(self.url).read()
                except urllib2.URLError:
                    print 'Tried to open page 3 times and failed.  Giving up...'
                    html = ''
        # create tree
        print html
        tree = lxml.html.fromstring(html)
        return tree

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

    # Sets id
    def set_id(self, new_id):
        self.id = new_id

    # Sets keeper variable
    def set_keeper(self, boolean):
        self.keeper = boolean

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

    # Sets a metadata facetkey and associates it with a dictionary containing its given facetvalue and (if provided) its given multivalue
    def set_metadata_value(self, facetkey, facetvalue, multivalue):
        if facetvalue:
            if isinstance(facetvalue, types.ListType):
                formatted_facetvalue = []
                for list_entry in facetvalue:
                    facetvalue_formatter = string_formatter(list_entry)
                    facetvalue_formatter.fix_data()
                    list_entry = facetvalue_formatter.get_string()
                    formatted_facetvalue.append(list_entry)
            else:
                facetvalue_formatter = string_formatter(facetvalue)
                facetvalue_formatter.fix_data()
                formatted_facetvalue = facetvalue_formatter.get_string()
            self.metadata[facetkey] = {}
            self.set_facetvalue(facetkey, formatted_facetvalue)
            if multivalue:
                self.set_multivalue(facetkey, multivalue)

    # Sets a facetkey in metadata dictionary and associates it with an empty dictionary
    def set_facetkey(self, facetkey):
        self.metadata[facetkey] = {}

    # Sets a given facetvalue in the dictionary associated with a given facetkey
    def set_facetvalue(self, facetkey, facetvalue):
        self.metadata[facetkey]['facetvalue'] = facetvalue

    # Sets a given multivalue in the dictionary associated with a given facetkey
    def set_multivalue(self, facetkey, multivalue):
        self.metadata[facetkey]['multi'] = multivalue

    # Sets a given entity text and associates it with a given entity probability in the dictionary associated with a given entity type
    def set_entity_text(self, entity_type, entity_text, entity_probability):
        if entity_type not in self.get_entities():
            self.set_entity_type(entity_type)
        self.entities[entity_type][entity_text] = entity_probability

    # Sets an entity type in entities dictionary and associates it with an empty dictionary
    def set_entity_type(self, entity_type):
        self.entities[entity_type] = {}

    # Getters

    # Returns url
    def get_url(self):
        return self.url

    # Returns id
    def get_id(self):
        return self.id

    # Returns tree
    def get_tree(self):
        return self.tree

    # Returns keeper variable
    def get_keeper(self):
        return self.keeper

    # Returns raw dictionary
    def get_raw(self):
        return self.raw

    # Returns raw dictionary value associated with a given dictionary key
    def get_raw_value(self, raw_key):
        return self.raw[raw_key]

    # Returns metadata dictionary
    def get_metadata(self):
        return self.metadata

    # Returns the metadata facetvalue given the metadata facetkey
    def get_facetvalue(self, facetkey):
        return self.metadata[facetkey]['facetvalue']

    # Returns the metadata multivalue given the metadata facetkey
    def get_multivalue(self, facetkey):
        return self.metadata[facetkey]['multi']

    # Returns entities dictionary
    def get_entities(self):
        return self.entities

    # Returns all entity_texts associated with a given entity type
    def get_entity_texts(self, entity_type):
        return self.entities[entity_type]

    # Returns the entity probability associated with a given entity_type and text
    def get_entity_probability(self, entity_type, entity_text):
        return self.entities[entity_type][entity_text]

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

    # Extracts all raw data and metadata except for published date
    def extract_all_data(self):
        self.extract_published_date()
        if self.article.get_keeper():
            self.extract_body_text()
            if self.article.get_keeper():
                self.extract_authors()
                self.extract_topic_regions()
                self.extract_publication_type()
                self.extract_id()
                self.extract_title()
                self.extract_document_type()
                #self.extract_pdf()
                self.extract_extraction_date_time()
                self.extract_publisher()
                self.extract_distributor()
                self.extract_producer_category()
                self.extract_keywords()
                self.extract_all_entities()
            else:
                return
        else:
            return

    # Extracts a metadata value given its attribute (as in a cssselector), only returns value if value is found
    def extract_metadata(self, attribute):
        selector = 'head meta[%s]' % attribute
        facet_element = self.extract(selector)
        if facet_element is not None:
            facetvalue = facet_element.attrib['content']
            if facetvalue is not None:
                return facetvalue

    # Sets current article url as article id
    def extract_id(self):
        url = self.article.get_url()
        self.article.set_id(url)

    # Extracts current article url and stores it in metadata dictionary
    def extract_source_url(self):
        self.article.set_metadata_value('source-url', self.article.get_url(), 'true')

    # Data collecting methods: 
    # The following methods extract relevant information from the source code of an article and store them in
    # the raw dict, the metadata dict, the entities dict or some combination of these
    # Note: if method name is plural, value stored will be a list.  List values will have a maximum length of 10
    # If no value is found, dictionary key will not be entered in dictionary

    def extract_published_date(self):
        published_date = self.extract_metadata('name="dat"')
        if not published_date:
            published_date = self.extract_metadata('name="pdate"')
        if published_date:
            date_formatter = date_time_formatter(published_date)
            try:
                date_formatter.parse_date()
            except ValueError:
                try:
                    date_formatter.to_iso('%B %d, %Y')
                except ValueError:
                    try:
                        date_formatter.to_iso('%B %d %Y')
                    except ValueError:
                        try:
                            date_formatter.to_iso('%Y%m%d')
                        except ValueError:
                            return
            if date_formatter.is_yesterday():
                date_formatter.to_savanna()
                formatted_published_date = date_formatter.get_date_time()
                self.article.set_metadata_value('published-date', formatted_published_date, '')
                self.article.set_raw_value('published_date', formatted_published_date)
            else:
                self.article.set_keeper(False)
        else:
            self.article.set_keeper(False)

    def extract_authors(self):
        authors = self.extract_metadata('name="author"')
        if authors:
            author_formatter = string_formatter(authors)
            author_formatter.to_list(';', 10)
            author_list = author_formatter.get_string()
            self.article.set_metadata_value('author', author_list, 'true')
            self.article.set_raw_value('author', author_list)

    def extract_topic_regions(self):
        regions = self.extract_metadata('name="geo"')
        if regions:
            region_formatter = string_formatter(regions)
            region_formatter.to_list(';', 10)
            region_list = region_formatter.get_string()
            self.article.set_metadata_value('topic-regions', region_list, 'true')
            self.article.set_raw_value('topic_regions', region_list)

    def extract_keywords(self):
        keywords = self.extract_metadata('name="keywords"')
        if keywords:
            keyword_formatter = string_formatter(keywords)
            keyword_formatter.to_list(',', 10)
            keyword_list = keyword_formatter.get_string()
            self.article.set_metadata_value('keywords', keyword_list, 'true')
            self.article.set_raw_value('keywords', keyword_list)

    def extract_publication_type(self):
        publication_type = self.extract_metadata('property="og:type"')
        self.article.set_metadata_value('publication-type', publication_type, 'true')
        self.article.set_raw_value('publication_type', publication_type)

    def extract_title(self):
        title = self.extract('head title').text
        title = title.replace(' - NYTimes.com', '')
        self.article.set_metadata_value('document-subject', title, 'false')
        self.article.set_raw_value('title', title)

    # Loops through article pages and extracts body text from each page
    def extract_body_text(self):
        article_navigator = navigator(self.article)
        body_text = []
        final_text = ''
        # Loop through pages
        while True:
            # Extract body text
            paragraphs = self.extract_list('p[itemprop="articleBody"]')
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

    # These metadata values are constant:
    def extract_publisher(self):
        self.article.set_metadata_value('producer', 'The New York Times', 'false')

    def extract_distributor(self):
        self.article.set_metadata_value('distributor', 'The New York Times', 'false')

    def extract_producer_category(self):
        self.article.set_metadata_value('producer-category', 'Media', 'false')

    def extract_document_type(self):
        self.article.set_metadata_value('document-type', 'txt', 'false')

    # Gets current date_time in Savanna format
    def extract_extraction_date_time(self):
        current_date_time_formatter = date_time_formatter('')
        current_date_time_formatter.to_current()
        current_date_time_formatter.to_savanna()
        extraction_date_time = current_date_time_formatter.get_date_time()
        self.article.set_raw_value('extraction_date', extraction_date_time)
        self.article.set_metadata_value('extraction-date', extraction_date_time, 'true')

    # The following methods are for extracting entities:

    # Extracts all content using the content analyzer
    def extract_all_entities(self):
        try:
            self.article.get_raw_value('body_text')
        except KeyError:
            return
        content_article = self.run_content_analyzer()
        self.extract_categories(content_article)
        self.extract_entities(content_article, 'people', '/person')
        self.extract_entities(content_article, 'organizations', '/organization')
        self.extract_entities(content_article, 'places', '/place')

    # Passes body text to content analyzer and returns article containing content tree
    def run_content_analyzer(self):
        body_text = self.article.get_raw_value('body_text')
        # Clean up body text for passing into Yahoo Content Analyzer
        body_text = re.sub("[^A-Za-z]", " ", body_text)[:2000]
        body_text = body_text.replace(" ","%20")
        # Use REST service to get entities
        yahoo_rest_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%22' + body_text + '%22&diagnostics=true'
        content_article = web_article(yahoo_rest_url)
        return content_article

    # Extracts categories from tree of given content_article
    def extract_categories(self, content_article):
        category_extractor = extractor(content_article)
        categories = category_extractor.extract_list('results yctcategory')
        for category in categories:
            entity_probability = category.attrib['score']
            category_text = category.text
            category_formatter = string_formatter(category_text)
            category_formatter.fix_data()
            formatted_category_text = category_formatter.get_string()
            self.article.set_entity_text('category', formatted_category_text, entity_probability)

    def extract_entities(self, content_article, entity_type, entity_type_text):
        entity_extractor = extractor(content_article)
        entity_text_elements = entity_extractor.extract_list("results entity:contains('%s') text" % entity_type_text)
        for entity_text_element in entity_text_elements:
            entity_probability = entity_text_element.getparent().attrib['score']
            entity_text = entity_text_element.text
            entity_formatter = string_formatter(entity_text)
            entity_formatter.fix_data()
            formatted_entity_text = entity_formatter.get_string()
            self.article.set_entity_text(entity_type, formatted_entity_text, entity_probability)

# This class is for writing the metadata file from the metadata and entities dictionaries
class metadata_writer(object):

    def __init__(self, article):
        self.set_article(article)

    def get_article(self):
        return self.article

    def set_article(self, article):
        self.article = article

    # Writes metadata file and stores it in the raw dictionary
    def write_metadata_file(self):
        file = ''

        # Writes beginning of metadata file
        file = '%s<doc           xmlns="http://thetus.com/savanna/doc"\r\n' % file
        file = '%sxmlns:proc="http://thetus.com/savanna/doc/processing"\r\n' % file
        file = '%sxmlns:thetus="http://thetus.com"\r\n' % file
        file = '%sxmlns:ent="http://thetus.com/savanna/doc/entities"     xmlns:sec="http://thetus.com/savanna/doc/security"\r\n' % file
        file = '%sxmlns:facet="http://thetus.com/savanna/doc/facet"\r\n' % file
        file = '%sxmlns:source="http://thetus.com/savanna/doc/source" >\r\n' % file
        file = '%s    <sec:sec>\r\n' % file
        file = '%s        <sec:ownerProducer>Thetus Corporation</sec:ownerProducer>\r\n' % file
        file = '%s        <sec:classification>UNCLASSIFIED</sec:classification>\r\n' % file
        file = '%s    </sec:sec>\r\n' % file
        file = '%s    <meta>\r\n' % file

        # Published date has unique metadata code without multiValued setting:
        file = '%s        <published-date>%s</published-date>\r\n' % (file, self.article.get_facetvalue('published-date'))

        # Loops through metadata keys and write relevant metadata code
        for facetkey in self.article.get_metadata():
            facetvalues = self.article.get_facetvalue(facetkey)

            # Skips published date key
            if facetkey == 'published-date':
                continue

            # Otherwise sets multiValued to its value in the metadata dictionary and writes the facetkey
            else:
                multivalue = self.article.get_multivalue(facetkey)
                file = '%s        <facet:facet dataType="text" multiValued="%s">\r\n' % (file, multivalue)
                file = '%s                    <facet:facetkey>%s</facet:facetkey>\r\n' % (file, facetkey)

            # If dictionary entry is a list, writes a facetvalue line for each list entry
            if isinstance(facetvalues, types.ListType):
                for facetvalue in facetvalues:
                    file = '%s                    <facet:facetvalue>%s</facet:facetvalue>\r\n' % (file, facetvalue)

            # Otherwise just writes one line for facetvalue
            else:
                facetvalue = facetvalues
                file = '%s                    <facet:facetvalue>%s</facet:facetvalue>\r\n' % (file, facetvalue)

        # Similarly, loops through entities dictionary and writes the facetkeys from the entity types 
        # (multiValued is always true)
        for entity_type in self.article.get_entities():
            file = '%s        <facet:facet dataType="text" multiValued="true">\r\n' % file
            file = '%s                    <facet:facetkey>%s</facet:facetkey>\r\n' % (file, entity_type)

            entity_texts = self.article.get_entity_texts(entity_type)
            # For each entity text associated with the entity type, writes a facetvalue line
            for entity_text in entity_texts:
                file = '%s                    <facet:facetvalue>%s</facet:facetvalue>\r\n' % (file, entity_text)

        # Writes end of metadata file
        file = '%s    </meta>\r\n' % file
        file = '%s    <proc:proc>\r\n' % file
        file = '%s        <proc:schema version="8"/>\r\n' % file
        file = '%s    </proc:proc>\r\n' % file
        file = '%s</doc>' % file

        # Finally, stores file in raw data
        self.article.set_raw_value('metadata_file', file)

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

    # Stores entities dictionary
    def export_entities(self):
        entities = self.article.get_entities()
        id = self.article.get_id()
        self.make_row('entities')
        # Loops through entities dictionary keys and stores values in new row
        # Values are stored under the column name of the entity_type with the format 'entity_text , entity_probability'
        # For entity types with multiple entity_texts, text/probability pairs are separated by ' | '
        for entity_type in entities:
            entity_list = []
            for entity_text in self.article.get_entity_texts(entity_type):
                entity_probability = self.article.get_entity_probability(entity_type, entity_text)
                entity_list_value = '%s , %s' % (entity_text, entity_probability)
                entity_list.append(entity_list_value)
            entity_string = ' | '.join(entity_list)
            scraperwiki.sqlite.execute("UPDATE %s_entities SET %s = '%s' WHERE id = '%s'" % (self.scraper_name, entity_type, entity_string, id))
        scraperwiki.sqlite.commit()

    # Exports raw and entities dictionaries
    def export_all_data(self):
        try:
            self.export_raw()
            self.export_entities()
        except scraperwiki.sqlite.SqliteError, e:
            print str(e)
            print self.article.get_raw()

    # The following methods create the required raw and entities tables:

    def create_raw_table(self):
        table_name = '%s_raw' % (self.scraper_name)
        #scraperwiki.sqlite.execute('DROP TABLE IF EXISTS %s' % table_name)
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


    def create_entities_table(self):
        table_name = '%s_entities' % (self.scraper_name)
        #scraperwiki.sqlite.execute('DROP TABLE IF EXISTS %s' % table_name)
        scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS %s (
                                        id TEXT,
                                        category INT,
                                        people TEXT,
                                        places TEXT,
                                        organizations TEXT)""" % table_name)
        scraperwiki.sqlite.commit()

    def create_tables(self):
        self.create_entities_table()
        self.create_raw_table()

    def export_to_file(self):
        output_dir = "C:\\Users\\bmihelic\\Desktop\\nytimes"
        metadata_file = self.article.get_raw_value('metadata_file')
        filename_formatter = string_formatter(self.article.get_url())
        filename_formatter.replace_chars('?/:<>', '')
        filename = filename_formatter.get_string()
        title = self.article.get_raw_value('title')
        body_text = self.article.get_raw_value('body_text')

        output_meta = codecs.open('%s\\%s.txt.metadata' % (output_dir, filename), 'w', 'utf-8')
        output_meta.write(metadata_file)
        output_meta.close()

        output_text = codecs.open('%s\\%s.txt' % (output_dir, filename), 'w', 'utf-8')
        output_text.write("Classification: UNCLASSIFIED\r\nCaveats: NONE\r\n\r\n")
        output_text.write("TITLE: %s\r\n" % title)

        output_text.write(body_text)
        output_text.close()

class navigator(object):

    def __init__(self, article):
        # Current article
        self.article = article
        # Root url to be used to finish url fragments found in 'href' attributes of 'a' elements
        self.root_url = 'http://www.nytimes.com'
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
        return linked_articles

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
        next_selector = 'div.articleBody a.next'
        next = next_extractor.extract(next_selector)
        if next is not None:
            self.click(next)
        else:
            return 'stop'

    # Skips initial ad found at www.nytimes.com
    def skip_ad(self):
        ad_extractor = extractor(self.article)
        title = ad_extractor.extract('title').text
        if title == 'NY Times Advertisement':
            img = self.article.extract('a[href] img[name="skip"]')
            a_link = img.getparent()
            self.click(a_link)

    # Gathers links on root page and returns a list of urls given selector to links
    def gather_links(self, link_selector):
        link_extractor = extractor(self.article)
        links = link_extractor.extract_list(link_selector)
        for link in links:
            self.links.append(link)

    # Creates articles from each link in links list and stores them in linked_articles
    def links_to_articles(self):
        for link in self.links:
            print link
            self.click(link)
            linked_article = web_article(self.article.get_url())
            self.linked_articles.append(linked_article)

    # Gathers all links and creates articles from them
    def gather_linked_articles(self, link_selector):
        self.gather_links(link_selector)
        self.links_to_articles()
        for article in self.linked_articles:
            print article.url
        print self.linked_articles
        print 'found %d articles' % len(self.linked_articles)

    # Check to see whether articles are current removes article if date does not match yesterday's date
    def save_keepers(self):
        articles_to_save = []
        for article in self.linked_articles:
            print 'article url: %s' % article.get_url()
            if article.get_keeper():
                print 'published date: %s' % article.get_raw_value('published_date')
                articles_to_save.append(article)
                print 'article saved'
            else:
                print 'article removed'
        print '%d articles left' % len(articles_to_save)
        self.linked_articles = articles_to_save

# This is the main function.  For each article on the new york times, it extracts the body text and any relevant data,
# writes a metadata file for the article and sends everything to the scraperwiki database.
def extract_all_articles():
    # Set root url
    url = 'http://www.nytimes.com'
    # Make root page
    root_page = web_article(url)
    # Create navigator for getting categories on root page
    root_navigator = navigator(root_page)
    # Skip ad if need be...
    root_navigator.skip_ad()
    # Gather all category pages at the given cssselector
    root_navigator.gather_linked_articles('h6.moduleHeaderLg a')
    # For each category page:
    for category_page in root_navigator.linked_articles:
        # Make a new navigator for the category page
        category_navigator = navigator(category_page)
        # Gather all article pages at the given cssselector
        category_navigator.gather_linked_articles('body div.aColumn h3 > a')
        for news_article in category_navigator.linked_articles:
            data_extractor = extractor(news_article)
            data_extractor.extract_all_data()
        category_navigator.save_keepers()
        for news_article in category_navigator.linked_articles:
            # Make a metadata writer object to write the metadata file
            meta_writer = metadata_writer(news_article)
            # Write the metadata file
            meta_writer.write_metadata_file()
            # Make news exporter object to send data to database
            news_exporter = exporter(news_article, 'nytimes')
            # Create database tables
            news_exporter.create_tables()
            # Export data to database
            news_exporter.export_all_data()
            # Export data to file
            #news_exporter.export_to_file()
            print news_article.get_raw_value('metadata_file')

extract_all_articles()