import scraperwiki
import urllib2
import json
import lxml.etree as etree
import re
import uuid


data = {}

def line_extractor(root):
    for page in root:
        for text in page:
            text_line = ''
            if text.text:
                text_line = text.text
                
            else:
                text_line = ''
                for i in text:
                    text_line = text_line + i.text
            yield text_line

def mp_text_block(root):            
    block_start = False
    text_block = ''
    key = ''
    text_start = False
    mp = ''
    data = {}
    for line in line_extractor(root):
        if not block_start:
            if re.search(r'PR\-\d{4}',line):
                #print 'block start'
                key = line[line.index('P'):]
                block_start = True
        else:
            if re.search(r'\w+\s*\[ (\w+\s*)+ \]',line):
                #print 'mp start'
                mp = line

            elif re.match(r'^"',line):
                #print 'text start'
                text_start = True
                text_block = text_block + line

            elif text_start:
                if re.search('"\s$',line):
                    #print 'cleaning up'
                    text_start = False
                    block_start = False
                    text_block = text_block + line
                    data = {'key':key,'mp':mp,'text':text_block,'key':str(uuid.uuid1())}
                    scraperwiki.sqlite.save(unique_keys=['key'],data=data)
                    text_block = ''
                    mp = ''
                    #print data
                elif re.search('^\s+$',line):
                    pass
                elif re.search('^AUM',line):
                    pass
                elif re.search('^\($',line):
                    pass
                else:
                    #print 'text adding'
                    text_block = text_block + line
                

            else:
                if re.match('\B',line):
                    pass
                else:
                    print 'problem ',line, len(line), text_start,block_start

def main():
    link_src = \
    '''https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=malaysian_parliament_hansard_url&query=select%20*%20from%20swdata%20limit%2010'''
    links = urllib2.urlopen(link_src)
    links_data = json.load(links)
    pdf_url = links_data[2]['url'].replace(' ','%20')
    print pdf_url
    pdf_data = urllib2.urlopen(pdf_url).read()
    xml_data = scraperwiki.pdftoxml(pdf_data)
    xml_data = xml_data.replace('<b>','').replace('</b>','')
    print xml_data
    root = etree.fromstring(xml_data)
    # mp_text_block(root)
    #for i in line_extractor(root):
    #    if re.search(r'PR\-\d{4}',i):
    #        print i
    #    if re.search(r'"\s$',i):
    #         print i
    #    if re.search(r'^AUM',i):
    #        pass
    #    elif re.search(r'^\s$',i):
    #        pass
    #    elif re.match(r'^\d+$',i):
    #        pass
    #    else:
    #        print i

main()
    