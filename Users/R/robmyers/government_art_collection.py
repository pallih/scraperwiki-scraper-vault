# Copyright 2011 Rob Myers <rob@robmyers.org>
# Licence: GPL3 or later (at your option)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#TODO: Check for http errors and raise exception if found. Utility function...


################################################################################
# Imports
################################################################################

import scraperwiki
import lxml.html
import pickle
import re
import urllib


################################################################################
# Constants
################################################################################


SERVER = "http://www.gac.culture.gov.uk"

# The letters of the alphabet...
LETTERS = list('abcdefghijklmnopqrstuvwxyz')

# The number of pages to process each time in order to avoid a CPU timeout
PAGES_TO_PROCESS_EACH_TIME = 10


################################################################################
# Artists
################################################################################



class ShouldContinueLater (Exception):
    """Have we processed enough items for now? Avoid a CPU timout..."""
    pass


def fetch_artwork_root(obj):
    """Get the lxml html object for this artwork id"""
    url = "%s/work.aspx?obj=%s" % (SERVER, obj)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root


def artwork_details(root):
    """Get the artwork's details from the parsed html root"""
    trs = root.cssselect("div#detailsArtWork table tr")
    properties = {}
    for tr in trs:
        tds = tr.cssselect('td')
        # Table is of the format <tr><td>KEY</td><td>VALUE</td></tr>
        # And may feature empty cells
        # Get the first cell as the key, lowercasing it and
        # replacing spaces with underscores to make good column names
        key = re.sub(" ", "_", tds[0].text_content().lower())
        if key:
            properties[key] = tds[1].text
    print properties
    return properties


def remove_trailing_comma(tag):
    """Remove any trailing comma from the tag"""
    if tag[-1] == ',':
        tag = tag[:-1]
    return tag


def clean_tags(subjects):
    """Clean subject tags of extranious punctuation, etc."""
    # We get Nones, so remove these
    subjects = [subject for subject in subjects if subject != None]
    # Strip leading/trailing whitespace
    subjects = [subject.strip() for subject in subjects]
    # And remove any resulting empty strings
    subjects = [subject for subject in subjects if subject != ""]
    # Remove trailing commas from items in list
    subjects = [remove_trailing_comma(subject) for subject in subjects if subject != ""]
    return subjects


def tags_in_div_lis(root, divId):
    """Get subject or sitter lists from div/ul/li/a texts."""
    # "lis" is the multiple of "li", not a misspelling of "list" :-)
    subjectLinks = root.cssselect("div#%s ul li a" % divId)
    subjects = clean_tags([link.text for link in subjectLinks])
    return subjects


def artwork_places(root, gac):
    """Get the places tagged in the artwork"""
    tags = tags_in_div_lis(root, "contentWorkPlaces")
    return [{'gac_number':gac, 'place':tag} for tag in tags]


def artwork_subjects(root, gac):
    """Get the subjects tagged in the artwork"""
    tags = tags_in_div_lis(root, "containerWorkSubject")
    return [{'gac_number':gac, 'subject':tag} for tag in tags]


def artwork_sitters(root, gac):
    """Get the sitters tagged in the artwork"""
    tags = tags_in_div_lis(root, "contentWorkSitters")
    return [{'gac_number':gac, 'sitter':tag} for tag in tags]


def store_artwork_details_for_ids(objs):
    """Write the details for artworks in the objs list to the datastore"""
    # Batch these so we can insert them into the datastore more efficiently
    artworks = []
    places = []
    subjects = []
    sitters = []
    for obj in objs:
        # Occasional bad status lines. Handle them.
        try:
            root = fetch_artwork_root(obj)
        except Exception, e:
            print "Exception for artwork %s: %s" % (obj, e)
            continue
        artwork = artwork_details(root)
        gac = artwork.get('gac_number', None)
        artwork["obj"] = obj
        # Occasional bad links, indicated by empty artwork dict. Handle them.
        if gac:
            artworks.append(artwork)
            places += artwork_places(root, gac)
            subjects += artwork_subjects(root, gac)
            sitters += artwork_sitters(root, gac)
        else:
            print "Artwork with no GAC Number! %s - %s" % (obj, artwork)
    scraperwiki.sqlite.save(["gac_number", "obj"], artworks, table_name="artwork", verbose=2)
    scraperwiki.sqlite.save(None, places, table_name="place", verbose=2)
    scraperwiki.sqlite.save(None, subjects, table_name="subject", verbose=2)
    scraperwiki.sqlite.save(None, sitters, table_name="sitter", verbose=2)

#store_artwork_details_for_ids(['31635'])
# print scraperwiki.sqlite.execute("select * from artwork where gac_number=15508")


def artist_pages_count_for_range(range_string):
    """Get the number of pages for the letter range. Pages start at 1."""
    url = "%s/artists_list.aspx?sb=ArtistName&sl=%s" % (SERVER, range_string)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    pageCountDiv = root.cssselect("div#pageOfPages")[0]
    pageCount = re.search(r"Page [0-9]+ of ([0-9]+)", pageCountDiv.text).group(1)
    return int(pageCount)

# print artist_pages_count_for_range('AA%20-%20AL')


def artwork_ids_for_range_page(range_string, page):
    """Get the object ids for the artworks on page in letter range. Pages start at 1."""
    url = "%s/artists_list.aspx?sb=ArtistName&sl=%s&pg=%s" % (SERVER, range_string, page)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    works = root.cssselect("div.eliteSearchBox a")
    hrefs = [work.get('href') for work in works]
    objs = [re.match(r"/work\.aspx\?obj=([0-9]+)$", href).group(1) for href in hrefs]
    return objs

# print artwork_ids_for_range_page('AA%20-%20AL', 2)


def artist_ranges_for_letter(letter):
    """Get the ranges (e.g. aaa%20-%20aal, aal%20-%20aaz) for artists whose names begin with letter"""
    url = "%s/artists_list.aspx?&l=%s&sb=ArtistName" % (SERVER, letter)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    select = root.cssselect("select#makerRanges")[0]
    ranges = [urllib.quote(node.text) for node in select.getchildren()]
    return ranges
  
 # artist_ranges_for_letter('a')


def get_page_count(range_string):
    """The total count of pages in the letter range to process
       Get from the datastore, or reset for first run"""
    page_count = scraperwiki.sqlite.get_var('letter_range_page_count')
    if page_count == None:
        page_count = page_count = artist_pages_count_for_range(range_string)
        scraperwiki.sqlite.save_var('letter_range_page_count', page_count)
    return page_count


def get_page_index():
    """Get the index of the page in the range we are actually processing"""
    page_index = scraperwiki.sqlite.get_var('letter_range_page_index')
    if page_index == None:
         page_index = 1
         scraperwiki.sqlite.save_var('letter_range_page_index', page_index)
    return page_index


def clear_page_ranges_and_count():
    """Clear page count and page index for next letter range"""
    scraperwiki.sqlite.save_var('letter_range_page_count', None)
    scraperwiki.sqlite.save_var('letter_range_page_index', None)


def store_artworks_for_letter_range_pages(range_string, pages_processed_count):
    """Step through the pages in the letter range, storing the artworks"""
    print "Storing artists for letter range: %s" % range_string
    page_count = get_page_count(range_string)
    page_index = get_page_index()
    # Process each page
    print "Pages: %d Starting at: %d" % (page_count, page_index)
    while page_index <= page_count:
        print "Storing artists for page %i of letter range %s" % (page_index, range_string)
        objs = artwork_ids_for_range_page(range_string, page_index)
        store_artwork_details_for_ids(objs)
        page_index = page_index + 1
        scraperwiki.sqlite.save_var('letter_range_page_index', page_index)
        pages_processed_count = pages_processed_count + 1
        if pages_processed_count >= PAGES_TO_PROCESS_EACH_TIME:
            raise ShouldContinueLater()
    clear_page_ranges_and_count()
    return pages_processed_count

def get_ranges_for_letter(letter):
    """Get the letter ranges from the datastore or the network"""
    ranges_pickled = scraperwiki.sqlite.get_var('letter_ranges')
    if ranges_pickled == None:
        ranges = artist_ranges_for_letter(letter)
        scraperwiki.sqlite.save_var('letter_ranges', pickle.dumps(ranges))
    else:
        ranges = pickle.loads(ranges_pickled)
    return ranges


def get_range_index():
    """Get the current index in the list of ranges, or set to 0 for first run"""
    range_index = scraperwiki.sqlite.get_var('letter_range_index')
    if range_index == None:
        range_index = 0
        scraperwiki.sqlite.save_var('letter_range_index', range_index)
    return range_index


def reset_letter_ranges_and_index():
    """Reset the letter ranges ready for the next letter"""
    scraperwiki.sqlite.save_var('letter_ranges', None)
    scraperwiki.sqlite.save_var('letter_range_index', 0)


def store_artworks_for_artists_beginning(letter):
    """For each letter range for the letter, store the artworks from each page"""
    print "Storing artists for letter: %s" % letter
    ranges = get_ranges_for_letter(letter)
    range_index = get_range_index()
    pages_processed_count = 0
    # Process each letter range
    while range_index != len(ranges):
        pages_processed_count = store_artworks_for_letter_range_pages(ranges[range_index], pages_processed_count)
        range_index = range_index + 1
        scraperwiki.sqlite.save_var('letter_range_index', range_index)
    reset_letter_ranges_and_index()
    return pages_processed_count

#store_artworks_for_artists_beginning('a')


#scraperwiki.sqlite.save_var('current_letter_index', 0)  # to reset
def get_current_letter_index():
    """Get the current letter index from the datastore, or create it"""
    current_letter_index =scraperwiki.sqlite.get_var('current_letter_index')
    if current_letter_index == None:
        # First run, so initialize the value
        current_letter_index = 0
        scraperwiki.sqlite.save_var('current_letter_index', current_letter_index)
    return current_letter_index


def reset_current_letter_index():
    """Reset the current letter index ready for the next run"""
    scraperwiki.sqlite.save_var('current_letter_index', None)


def artists_toplevel():
    """The entry point for storing artworks for artists"""
    print "Storing artworks for artists."
    current_letter_index = get_current_letter_index()
    # Just run this once. If we want to rebuild, clear the var
    if current_letter_index != len(LETTERS):
        try:
            store_artworks_for_artists_beginning(LETTERS[current_letter_index])
            current_letter_index = current_letter_index + 1
            scraperwiki.sqlite.save_var('current_letter_index', current_letter_index)
        except ShouldContinueLater, e:
            print "Processed enough for now, continuing later to avoid timeout."


################################################################################
# Main run lifecycle
################################################################################

# Go!

artists_toplevel()

