'''
For a given book/author, searches the UNESCO translation database and finds what languages they have been translated into.
'''


import scraperwiki
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib import quote

BASE_URL = "http://www.unesco.org/xtrans/"

#Initial author list, for proof-of-concept:
AUTHOR_LIST = [
    'asimov, isaac',
    'drake, david',
    'weber, david',
    'haldeman, joe',
    'scalzi, john',
    'traviss, karen',
    'lowachee, karin'
]

BOOK_LIST = [
    "starship troopers",
    "ender's game"
]


def extract_languages(url):
    '''
    Extract all the languages mentioned in the page.
    '''
    
    raw_page = scraperwiki.scrape(url)

    page_soup = BeautifulSoup(raw_page)

    language_count = defaultdict(int)
    
    # Find all <span class="sn_target_lang">... and extract the language text
    lang_soup = page_soup.find_all("span", {"class": "sn_target_lang"})
    for row in lang_soup:
        lang = row.get_text().strip()
        language_count[lang] += 1
    
    # Find links to the next pages:
    next_soup = page_soup.find("td", {"class": "next"}).find('a')

    if next_soup is None: 
        return language_count
    next_link = next_soup.get('href')
    next_link = quote(next_link, "?=&,")
    print next_link
    link = BASE_URL + next_link
    new_langs = extract_languages(link)
    for lang in new_langs:
            language_count[lang] += new_langs[lang]
        
    return language_count
    
def search(title='', author=''):
    '''
    Search by title and/or author and append language counts to db.
    Author names should be in the format of LASTNAME, FIRSTNAME
    Search syntax is bsresult.aspx?a=[AUTHOR]&stxt=[TITLE]
    '''
    s_title = quote(title, ',')
    s_author = quote(author, ',')
    search_string = "bsresult.aspx?a=" + s_author  + "&stxt=" + s_title
    search_url = BASE_URL + search_string
    results = extract_languages(search_url)
    
    db_entries = []
    for lang in results:
        new_entry = {}
        new_entry['title'] = title
        new_entry['author'] = author
        new_entry['language'] = lang
        new_entry['count'] = results[lang]
        db_entries.append(new_entry)

    scraperwiki.sqlite.save(['title', 'author', 'language'], db_entries, table_name="Translations")

#MAIN CODE
#=========

for name in AUTHOR_LIST: search(author=name)
for name in BOOK_LIST: search(title=name)

'''
For a given book/author, searches the UNESCO translation database and finds what languages they have been translated into.
'''


import scraperwiki
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib import quote

BASE_URL = "http://www.unesco.org/xtrans/"

#Initial author list, for proof-of-concept:
AUTHOR_LIST = [
    'asimov, isaac',
    'drake, david',
    'weber, david',
    'haldeman, joe',
    'scalzi, john',
    'traviss, karen',
    'lowachee, karin'
]

BOOK_LIST = [
    "starship troopers",
    "ender's game"
]


def extract_languages(url):
    '''
    Extract all the languages mentioned in the page.
    '''
    
    raw_page = scraperwiki.scrape(url)

    page_soup = BeautifulSoup(raw_page)

    language_count = defaultdict(int)
    
    # Find all <span class="sn_target_lang">... and extract the language text
    lang_soup = page_soup.find_all("span", {"class": "sn_target_lang"})
    for row in lang_soup:
        lang = row.get_text().strip()
        language_count[lang] += 1
    
    # Find links to the next pages:
    next_soup = page_soup.find("td", {"class": "next"}).find('a')

    if next_soup is None: 
        return language_count
    next_link = next_soup.get('href')
    next_link = quote(next_link, "?=&,")
    print next_link
    link = BASE_URL + next_link
    new_langs = extract_languages(link)
    for lang in new_langs:
            language_count[lang] += new_langs[lang]
        
    return language_count
    
def search(title='', author=''):
    '''
    Search by title and/or author and append language counts to db.
    Author names should be in the format of LASTNAME, FIRSTNAME
    Search syntax is bsresult.aspx?a=[AUTHOR]&stxt=[TITLE]
    '''
    s_title = quote(title, ',')
    s_author = quote(author, ',')
    search_string = "bsresult.aspx?a=" + s_author  + "&stxt=" + s_title
    search_url = BASE_URL + search_string
    results = extract_languages(search_url)
    
    db_entries = []
    for lang in results:
        new_entry = {}
        new_entry['title'] = title
        new_entry['author'] = author
        new_entry['language'] = lang
        new_entry['count'] = results[lang]
        db_entries.append(new_entry)

    scraperwiki.sqlite.save(['title', 'author', 'language'], db_entries, table_name="Translations")

#MAIN CODE
#=========

for name in AUTHOR_LIST: search(author=name)
for name in BOOK_LIST: search(title=name)

