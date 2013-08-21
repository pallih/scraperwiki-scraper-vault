import scraperwiki
import lxml.html
import nltk, re, pprint 
import requests
import ast
import time

scraperwiki.sqlite.attach("robbie_lyrics")
url_list =  scraperwiki.sqlite.select("* from robbie_lyrics.swdata")


def ie_preprocess(document):
    """This function takes raw text and chops and then connects the process to break it down into
    sentences, then words and then complete part-of-speech tagging"""
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def scrape_lyrics (url):
    """This function scrapes a URL, ids the div#albums tag, tests to see whether the #songlyrics_h tag exists and if it does,
    then grabs the text and passes it to test-sentiment function for analysis""" 
    url = url.encode('utf8', 'replace')
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    block = root.cssselect("div#albums")
    if root.cssselect('#songlyrics_h'):
        lyrics = root.cssselect('#songlyrics_h')
        text_lyric = lyrics[0].text_content()  
        neg, pos, neutral, label = test_sentiment(text_lyric) 
        
    else:
        neg = "none available"
        pos = "none available"
        neutral = "none available"
        label = "none available"
    return neg, pos, neutral, label
 

def test_sentiment(text):
    string_for_output = text.encode('utf8', 'replace')
    payload = {'text': string_for_output}
    r = requests.post("http://text-processing.com/api/sentiment/", data=payload)
    dictionary = str(r.text)
    dictionary = ast.literal_eval(dictionary)
    neg = dictionary['probability']['neg']
    pos = dictionary['probability']['pos']
    neutral = dictionary['probability']['neutral']
    label = dictionary['label']
    return neg, pos, neutral, label
    
print url_list
for row in url_list:
    record = {}
    link_url = row['url']
    print link_url
    neg, pos, neutral, label = scrape_lyrics(link_url)
    print neg, pos, neutral, label
    record['album'] = row['album']
    record['song'] = row ['song']
    record['year'] = row ['year']
    record['url'] = row ['url']
    record['neg'] = neg
    record['pos'] = pos
    record['neutral'] = neutral
    record['label'] = label
    record['index'] = row['index']
    scraperwiki.sqlite.save(['index'], record) 


    
