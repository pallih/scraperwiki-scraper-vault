# Blank Python
import pprint
import scraperwiki           
import lxml.html           
import string 

html = scraperwiki.scrape("http://www.corriere.it/")
root = lxml.html.fromstring(html)

search_word = 'ingleterre'

for el in lxml.html.iterlinks(html):
    #print el[2]
    
    try:
        exploded = el[2].split('/')
        for part in exploded:
            if part == 'cronache' or part == 'esteri':
                #print el[2]
                try:
                    linkhtml = scraperwiki.scrape(el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('p')
                    for one_paragraph in paragraphs:
                        exploded_body_text = one_paragraph.text.split(' ');
                        for word in exploded_body_text:
                            for c in string.punctuation:
                                word= word.replace(c,"")
                            if word.lower() == search_word:
                                print el[2]
                except:
                    pass
                try:
                    linkhtml = scraperwiki.scrape('http://www.corriere.it'+el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('p')
                    for one_paragraph in paragraphs:
                        exploded_body_text = one_paragraph.text.split(' ');
                        for word in exploded_body_text:
                            for c in string.punctuation:
                                word= word.replace(c,"")                            
                            if word.lower() == search_word:
                                print 'http://www.corriere.it'+el[2]
                except:
                    pass
    except:
        pass
# Blank Python
import pprint
import scraperwiki           
import lxml.html           
import string 

html = scraperwiki.scrape("http://www.corriere.it/")
root = lxml.html.fromstring(html)

search_word = 'ingleterre'

for el in lxml.html.iterlinks(html):
    #print el[2]
    
    try:
        exploded = el[2].split('/')
        for part in exploded:
            if part == 'cronache' or part == 'esteri':
                #print el[2]
                try:
                    linkhtml = scraperwiki.scrape(el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('p')
                    for one_paragraph in paragraphs:
                        exploded_body_text = one_paragraph.text.split(' ');
                        for word in exploded_body_text:
                            for c in string.punctuation:
                                word= word.replace(c,"")
                            if word.lower() == search_word:
                                print el[2]
                except:
                    pass
                try:
                    linkhtml = scraperwiki.scrape('http://www.corriere.it'+el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('p')
                    for one_paragraph in paragraphs:
                        exploded_body_text = one_paragraph.text.split(' ');
                        for word in exploded_body_text:
                            for c in string.punctuation:
                                word= word.replace(c,"")                            
                            if word.lower() == search_word:
                                print 'http://www.corriere.it'+el[2]
                except:
                    pass
    except:
        pass
