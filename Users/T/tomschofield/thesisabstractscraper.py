# Blank Python
import pprint
import scraperwiki           
import lxml.html           
import string 
#range is 50-78



urlcounter=59

while urlcounter<79:
    urlcounter +=1
    try:
        url = "https://theses.ncl.ac.uk/dspace/handle/10443/"+str(urlcounter)+"/browse-title"
        print urlcounter,url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        for el in lxml.html.iterlinks(html):
            counter = 0
            exploded = el[2].split('/')
    
            try:
                #print exploded[2]
                if exploded[2]=='handle':
                    #print "https://theses.ncl.ac.uk"+el[2]
                    linkhtml = scraperwiki.scrape("https://theses.ncl.ac.uk"+el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('td')
                    for element in paragraphs:
                        #exploded_body_text = element.text.split(' ');
                        try:
                            exploded_body_text = element.text.split(' ');
                            #if exploded_body_text[0].strip(' ') == 'Abstract:':
                            if counter > 0 :
                                #print "Got one ",element.text
                                scraperwiki.sqlite.save(unique_keys=["a"], data={"a":"§"+element.text+"§"})
                                counter = 0
                            if "Abstract:" in element.text :   
                                counter += 1
                        except:
                            pass
            except:
                pass
    except:
                pass # Blank Python
import pprint
import scraperwiki           
import lxml.html           
import string 
#range is 50-78



urlcounter=59

while urlcounter<79:
    urlcounter +=1
    try:
        url = "https://theses.ncl.ac.uk/dspace/handle/10443/"+str(urlcounter)+"/browse-title"
        print urlcounter,url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        for el in lxml.html.iterlinks(html):
            counter = 0
            exploded = el[2].split('/')
    
            try:
                #print exploded[2]
                if exploded[2]=='handle':
                    #print "https://theses.ncl.ac.uk"+el[2]
                    linkhtml = scraperwiki.scrape("https://theses.ncl.ac.uk"+el[2])
                    root = lxml.html.fromstring(linkhtml)
                    paragraphs = root.cssselect('td')
                    for element in paragraphs:
                        #exploded_body_text = element.text.split(' ');
                        try:
                            exploded_body_text = element.text.split(' ');
                            #if exploded_body_text[0].strip(' ') == 'Abstract:':
                            if counter > 0 :
                                #print "Got one ",element.text
                                scraperwiki.sqlite.save(unique_keys=["a"], data={"a":"§"+element.text+"§"})
                                counter = 0
                            if "Abstract:" in element.text :   
                                counter += 1
                        except:
                            pass
            except:
                pass
    except:
                pass 