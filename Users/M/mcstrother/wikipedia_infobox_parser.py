import scraperwiki

import re
import sys
import urllib2
import yaml
import pprint

"""
article_title = sys.argv[1]
if len(sys.argv) > 2:
    box_title = sys.argv[2]
    # allow box title to be capitalized or not
    box_title = '[' + box_title[0].lower() + box_title[0].upper() + ']' + box_title[1:]
else:
    box_title = None # if no infobox title is provided, program returns the first one on the page
"""
article_title = "Brazil"
box_title = None


#Build a regexp to get the source artery from the artery infobox
exp = r'\{\{'                  # the opening brackets for the infobox 
exp = exp + r'\s*'           # any amount of whitespace
exp = exp + r'[Ii]nfobox +'  # the word "infobox", capitalized or not followed by at least one space
if box_title:
    exp = exp + box_title     # the infobox title, capitalized or not
    exp = exp + r'\s*\|'         # any number of spaces or returns followed by a pipe character
exp = exp + r'.*'           # a bunch of other stuff in the infobox  
exp3 = exp                  # save the regexp so far so that I can use it later
exp3 = exp3 + r'.*\}\}'          # any amount of anything, followed by the end of the infobox

exp3_obj = re.compile(exp3, re.DOTALL)

def get_infobox_from_text(article_text):
    search_result = exp3_obj.search(article_text)
    if search_result:
        result_text = search_result.group(0) # returns the entire matching sequence
    else:
        return None
    # the regex isn't perfect, so look for the closing brackets of the infobox
    count = 0
    last_ind = None
    for ind, c in enumerate(result_text):
        if c == '}':
            count = count -1
        elif c == '{':
            count = count +1
        if count == 0 and not ind == 0:
            last_ind = ind
            break
    return result_text[0:last_ind+1]

def _get_proper_title_from_response(response):
    if 'redirects' in response:
        return response['redirects'][-1]['to']
    elif 'normalized' in response:
        return response['normalized'][-1]['to']
    #else return none

def get_yaml_url(url):
    """Get a yaml file from the wikimedia api and return it already parsed
    """
    wiki_file  = urllib2.urlopen(url)
    data = wiki_file.read()
    data = yaml.load(data)
    return data

def parse_infobox_text(text):
    text = text.split('|')
    text = text[1:] #everything before the first pipe is the infobox declaration
    new_list = [text[0]]
    for item in text[1:]:
        # make sure we split only on the pipes that represent ends of the infobox entry, not the pipes used in links
        if (']]' in item) and ((not '[[' in item) or item.find(']]') < item.find('[[')):
            new_list[-1] = new_list[-1] +'|' + item
        else:
            new_list.append(item)
    new_list[-1] = new_list[-1][:-2] #trim off the closing brackets
    data_dict = {}
    for item in new_list:
        if '=' in item:
            items = item.split('=', 1)
            data_dict[items[0].strip()] = items[1].strip()
        else:
            continue
    return data_dict
    
    
def get_article(title):
    r_title = title.replace(' ', '%20')
    url = 'http://en.wikipedia.org/w/api.php?action=query&titles=' + r_title +'&prop=revisions&rvprop=content&format=yaml&rvsection=0&redirects'
    data = get_yaml_url(url)
    response = data['query']
    try:
        article_text = response['pages'].values()[0]['revisions'][0]['*']
    except KeyError as ke:
        if not 'missing' in  response['pages'].values()[0]:
            raise ke # programmer error
        else:
            return (None, None)
    proper_title = _get_proper_title_from_response(response)
    if proper_title is None:
        proper_title = title
    return (article_text, proper_title)
    
def run(article_title):
    article_text, proper_title = get_article(article_title)
    data = parse_infobox_text(get_infobox_from_text(article_text))
    return data

scraperwiki.sqlite.save(unique_keys=("Name",), data = run(article_title))

    
