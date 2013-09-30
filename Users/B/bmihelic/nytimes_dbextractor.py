import scraperwiki

# Blank Python

import json
import urllib2
import codecs

def get_json(scraper_uri):
    scraper_json_request = urllib2.urlopen(scraper_uri)
    scraper_json = json.load(scraper_json_request)

    for item in scraper_json:
        print item
        #publisher = item.values()[0]
        #author = item.values()[2]
        #body_text = item.values()[1]
        #article_image_caption = item.values()[4]
        #article_image = item.values()[5]
        #metadata_file = item.values()[6]
        #published_date = item.values()[7]
        #pdf = item.values()[8]
        #source_url = item.values()[9]
        #title = item.values()[3]

        #filename = str(source_url)

        #output_meta = codecs.open(('%s/%s.txt.metadata' % (output_dir, remove_char(filename, '/:<>'))), 'w', 'utf-8')
        #output_meta.write(metadata_file)
        #output_meta.close()

        #output_text = codecs.open(('%s/%s.txt' % (output_dir, remove_char(filename, '/:<>'))), 'w', 'utf-8')
        #output_text.write("Classification: UNCLASSIFIED" + "\r\n" + "Caveats: NONE" + "\r\n\r\n")
        #output_text.write("TITLE:" + title + "\r\n")

        #output_text.write(body_text)
        #output_text.close()

def remove_char(value, deletechars):
    for c in deletechars:
        if not value == None:
            value = value.replace(c, '')
    return value;


if __name__ == "__main__":
    output_dir = "/Users/hstrauss/Desktop/allafrica"
    scraper_uri = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=nytimes&query=select%20*%20from%20%60nytimes_raw%60"
    get_json(scraper_uri)
import scraperwiki

# Blank Python

import json
import urllib2
import codecs

def get_json(scraper_uri):
    scraper_json_request = urllib2.urlopen(scraper_uri)
    scraper_json = json.load(scraper_json_request)

    for item in scraper_json:
        print item
        #publisher = item.values()[0]
        #author = item.values()[2]
        #body_text = item.values()[1]
        #article_image_caption = item.values()[4]
        #article_image = item.values()[5]
        #metadata_file = item.values()[6]
        #published_date = item.values()[7]
        #pdf = item.values()[8]
        #source_url = item.values()[9]
        #title = item.values()[3]

        #filename = str(source_url)

        #output_meta = codecs.open(('%s/%s.txt.metadata' % (output_dir, remove_char(filename, '/:<>'))), 'w', 'utf-8')
        #output_meta.write(metadata_file)
        #output_meta.close()

        #output_text = codecs.open(('%s/%s.txt' % (output_dir, remove_char(filename, '/:<>'))), 'w', 'utf-8')
        #output_text.write("Classification: UNCLASSIFIED" + "\r\n" + "Caveats: NONE" + "\r\n\r\n")
        #output_text.write("TITLE:" + title + "\r\n")

        #output_text.write(body_text)
        #output_text.close()

def remove_char(value, deletechars):
    for c in deletechars:
        if not value == None:
            value = value.replace(c, '')
    return value;


if __name__ == "__main__":
    output_dir = "/Users/hstrauss/Desktop/allafrica"
    scraper_uri = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=nytimes&query=select%20*%20from%20%60nytimes_raw%60"
    get_json(scraper_uri)
