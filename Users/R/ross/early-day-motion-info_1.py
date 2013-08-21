import scraperwiki
from lxml import etree
import time
from StringIO import StringIO
import string

scraperwiki.sqlite.attach("early-day-motions")

links = scraperwiki.sqlite.select("* from `early-day-motions`.swdata")

sources = scraperwiki.sqlite.select("distinct(source) from swdata ")
source_list = [s["source"] for s in sources]
#print source_list

for link in links:
    #print link
    url = link["url"]
    if url in source_list:
        print "Have already got %s" % url
        continue

    xml = scraperwiki.scrape(url).replace(chr(0), '')
    xml = string.replace(xml, "</xml>", "")
    #print xml

    try:
        parser = etree.XMLParser(huge_tree=True)
        root = etree.parse(StringIO(xml), parser)
    except Exception as e:
        print e
        continue

    motions = root.xpath('/session/motion')
    for motion in motions:
        id = motion.xpath('./id')[0].text
        number = motion.xpath('./number')[0].text
        session = motion.xpath('./session')[0].text
        title = motion.xpath('./title')[0].text
        text = motion.xpath('./text')[0].text
        proposer = motion.xpath('./proposer')[0].text
        proposer_obj_dont_save = motion.xpath('./proposer')[0]
        proposer = proposer_obj_dont_save.text
        proposer_id = proposer_obj_dont_save.get('id')
        signature_count = int(motion.xpath('./signature_count')[0].text)

        data = {"id":id, "number":number, "session":session, "title":title, "text":text, "proposer":proposer, "proposer_id":proposer_id, "signature_count":signature_count, "source":url}
        scraperwiki.sqlite.save(['id', 'number', 'session'], data)

import scraperwiki
from lxml import etree
import time
from StringIO import StringIO
import string

scraperwiki.sqlite.attach("early-day-motions")

links = scraperwiki.sqlite.select("* from `early-day-motions`.swdata")

sources = scraperwiki.sqlite.select("distinct(source) from swdata ")
source_list = [s["source"] for s in sources]
#print source_list

for link in links:
    #print link
    url = link["url"]
    if url in source_list:
        print "Have already got %s" % url
        continue

    xml = scraperwiki.scrape(url).replace(chr(0), '')
    xml = string.replace(xml, "</xml>", "")
    #print xml

    try:
        parser = etree.XMLParser(huge_tree=True)
        root = etree.parse(StringIO(xml), parser)
    except Exception as e:
        print e
        continue

    motions = root.xpath('/session/motion')
    for motion in motions:
        id = motion.xpath('./id')[0].text
        number = motion.xpath('./number')[0].text
        session = motion.xpath('./session')[0].text
        title = motion.xpath('./title')[0].text
        text = motion.xpath('./text')[0].text
        proposer = motion.xpath('./proposer')[0].text
        proposer_obj_dont_save = motion.xpath('./proposer')[0]
        proposer = proposer_obj_dont_save.text
        proposer_id = proposer_obj_dont_save.get('id')
        signature_count = int(motion.xpath('./signature_count')[0].text)

        data = {"id":id, "number":number, "session":session, "title":title, "text":text, "proposer":proposer, "proposer_id":proposer_id, "signature_count":signature_count, "source":url}
        scraperwiki.sqlite.save(['id', 'number', 'session'], data)

