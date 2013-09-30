import scraperwiki
import mechanize
import re
import urlparse
from scraperwiki import datastore

def Main():
    url = "http://www.plaidcymru.org/content.php?nID=564;lID=1"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    base = br.open(url)
    page = base.read()

    candidates = re.findall('(?si)<ul class="nav2">(.*?)</ul>', page)

    links = re.findall('(?si)<li>(.*?)</li>', candidates[0])
    for link in links:
        data = {}
        constituency = re.findall('(?si)<a href=".*?".*>(.*?)</a>', link)
        data["constituency"] = constituency[0]
        print "------------------------------------------------------------"
        print "CONSTITUENCTY: ", constituency[0]
        link = re.findall('(?si)<a href="(.*?)".*>.*?</a>', link)
        link = urlparse.urljoin(url, link[0])
        data["link"] = link
        page = br.follow_link(text_regex=constituency[0])
        page = page.read()
        code = re.findall('(?si)<div class="cms_content">(.*?)</div>', page)
        content = re.findall('(?si)<div class="cms_content">(.*?)</div>', page)
        name = re.findall('(?si)<center>\s*<h2><img.*?/></h2>\s*</center>\s*<h2>(.*?)</h2>', content[0])
        if name:
            data["name"] = SimplifyHTML(name[0])
            #print "NAME: ", name[0]
        else:
            name = re.findall('(?si)<h2>(.*?)</h2>', content[0])
            if name:
                data["name"] = SimplifyHTML(name[0])
                #print "NAME: ", name[0]
            else:
                name = re.findall('(?si)<p>(.*?)</p>', content[0])
                name = SimplifyHTML(name[0])
                name = re.findall('(?si)(Dr\s\w+\s\w+\s\w+).*?', name)
                if name:
                    data["name"] = SimplifyHTML(name[0])
                    print "NAME: ", name[0]
                else:
                    name = re.findall('(?si)<p>(.*?)</p>', content[0])
                    name = SimplifyHTML(name[0])
                    name = re.findall('(?si)(Llyr\s\w+\s\w+).*?', name)
                    if name:
                        data["name"] = SimplifyHTML(name[0])
                        print "NAME: ", name[0]
                    else:
                        name = re.findall('(?si)<p>(.*?)</p>', content[0])
                        name = SimplifyHTML(name[0])
                        name = re.findall('(?si)(\w+\s\w+).*?', name)
                        if name:
                            data["name"] = SimplifyHTML(name[0])
                            #print "NAME: ", name[0]
                        else:
                            name = re.findall('(?si)<p>(.*?)</p>', content[0])
                            name = re.findall('(?si)<strong>(\w+\s\w+).*?', name[1])
                            if name:
                                data["name"] = SimplifyHTML(name[0])
                                #print "NAME: ", name[0]
                            else:
                                name = re.findall('(?si)<p>(.*?)</p>',     content[0])
                                name = re.findall('(?si)(\w+\s\w+).*?', name[1])
                                if name:
                                    data["name"] = SimplifyHTML(name[0])
                                    #print "NAME: ", name[0]
                            
        photo = re.findall('(?si)<img.*?src="(.*?)".*?>', content[0])
        if photo:
            data["photo"] = urlparse.urljoin(link, photo[0])
        bio = re.findall('(?si)<p>(.*)</p>', content[0])
        if bio:
            bio = re.sub('\w+.\w+@\w+.com|Background: ', '', bio[0])
            data["bio"] = SimplifyHTML(bio)
        print "DATA: ", data
        datastore.save(unique_keys=['name', 'constituency'], data=data)

def SimplifyHTML(html):
    t = re.sub("<p>", "NEWLINE", html)
    t = re.sub("<h2>(.*)</h2>", "==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t

Main()

import scraperwiki
import mechanize
import re
import urlparse
from scraperwiki import datastore

def Main():
    url = "http://www.plaidcymru.org/content.php?nID=564;lID=1"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    base = br.open(url)
    page = base.read()

    candidates = re.findall('(?si)<ul class="nav2">(.*?)</ul>', page)

    links = re.findall('(?si)<li>(.*?)</li>', candidates[0])
    for link in links:
        data = {}
        constituency = re.findall('(?si)<a href=".*?".*>(.*?)</a>', link)
        data["constituency"] = constituency[0]
        print "------------------------------------------------------------"
        print "CONSTITUENCTY: ", constituency[0]
        link = re.findall('(?si)<a href="(.*?)".*>.*?</a>', link)
        link = urlparse.urljoin(url, link[0])
        data["link"] = link
        page = br.follow_link(text_regex=constituency[0])
        page = page.read()
        code = re.findall('(?si)<div class="cms_content">(.*?)</div>', page)
        content = re.findall('(?si)<div class="cms_content">(.*?)</div>', page)
        name = re.findall('(?si)<center>\s*<h2><img.*?/></h2>\s*</center>\s*<h2>(.*?)</h2>', content[0])
        if name:
            data["name"] = SimplifyHTML(name[0])
            #print "NAME: ", name[0]
        else:
            name = re.findall('(?si)<h2>(.*?)</h2>', content[0])
            if name:
                data["name"] = SimplifyHTML(name[0])
                #print "NAME: ", name[0]
            else:
                name = re.findall('(?si)<p>(.*?)</p>', content[0])
                name = SimplifyHTML(name[0])
                name = re.findall('(?si)(Dr\s\w+\s\w+\s\w+).*?', name)
                if name:
                    data["name"] = SimplifyHTML(name[0])
                    print "NAME: ", name[0]
                else:
                    name = re.findall('(?si)<p>(.*?)</p>', content[0])
                    name = SimplifyHTML(name[0])
                    name = re.findall('(?si)(Llyr\s\w+\s\w+).*?', name)
                    if name:
                        data["name"] = SimplifyHTML(name[0])
                        print "NAME: ", name[0]
                    else:
                        name = re.findall('(?si)<p>(.*?)</p>', content[0])
                        name = SimplifyHTML(name[0])
                        name = re.findall('(?si)(\w+\s\w+).*?', name)
                        if name:
                            data["name"] = SimplifyHTML(name[0])
                            #print "NAME: ", name[0]
                        else:
                            name = re.findall('(?si)<p>(.*?)</p>', content[0])
                            name = re.findall('(?si)<strong>(\w+\s\w+).*?', name[1])
                            if name:
                                data["name"] = SimplifyHTML(name[0])
                                #print "NAME: ", name[0]
                            else:
                                name = re.findall('(?si)<p>(.*?)</p>',     content[0])
                                name = re.findall('(?si)(\w+\s\w+).*?', name[1])
                                if name:
                                    data["name"] = SimplifyHTML(name[0])
                                    #print "NAME: ", name[0]
                            
        photo = re.findall('(?si)<img.*?src="(.*?)".*?>', content[0])
        if photo:
            data["photo"] = urlparse.urljoin(link, photo[0])
        bio = re.findall('(?si)<p>(.*)</p>', content[0])
        if bio:
            bio = re.sub('\w+.\w+@\w+.com|Background: ', '', bio[0])
            data["bio"] = SimplifyHTML(bio)
        print "DATA: ", data
        datastore.save(unique_keys=['name', 'constituency'], data=data)

def SimplifyHTML(html):
    t = re.sub("<p>", "NEWLINE", html)
    t = re.sub("<h2>(.*)</h2>", "==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t

Main()

