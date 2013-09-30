# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
# Needs parsing of list of countries per treaty and any signing statements

# Call to action: Which treaties has your nation not signed that you think it should sign?

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, datetime


def Main():
    url = "http://treaties.un.org/pages/ParticipationStatus.aspx"
    root = lxml.html.parse(url).getroot()
    print lxml.etree.tostring(root)

    # <tr><td>9</td><td><a href="sss">CHAPTER IX</a></td><td><span>Health</span></td></tr>
    for node in root.cssselect('table#ctl00_ContentPlaceHolder1_dgChapterList tr'):
        assert (node[1][0].tag, node[2][0].tag) == ('a', 'span'), lxml.etree.tostring(node)
        lurl, ltext, chaptitle = node[1][0].get('href'), node[1][0].text, node[2][0].text
        rurl = urlparse.urljoin(url, lurl)

        #<tr><td>10.</td><td><a href="V">Africa. &#160;&#160;Paris, 14 October 1994</a></td>
        #<td>27</td><td>10</td><td></td><td>XXVII</td><td></td><td>527</td>
        #<td>United Nations in Africa</td><td>XXVII-10</td></tr>        
        sroot = lxml.html.parse(rurl).getroot()
        for snode in sroot.cssselect('table#ctl00_ContentPlaceHolder1_dgSubChapterList tr'):
            assert (snode[1][0].tag, snode[8].tag, snode[9].tag) == ('a', 'td', 'td'), lxml.etree.tostring(snode)
            turl, ttext, title, cid = snode[1][0].get('href'), snode[1][0].text, snode[8].text, snode[9].text
            tturl = urlparse.urljoin(rurl, turl)

            data = { "title":title, "chapnum":cid, "url":tturl, "chapter":chaptitle }

            mcitydate = re.search("\xa0\xa0\s*(.*?),\s*(\d+)\s+(\w+)\s+(\d+)$", ttext)
            if mcitydate:
                data["city"] = mcitydate.group(1)
                data["date"] = datetime.date(int(mcitydate.group(4)), months.index(mcitydate.group(3))+1, int(mcitydate.group(2)))
            
            scraperwiki.datastore.save(unique_keys=["chapnum"], data=data)
    
    
# Delete functions below when you are done hacking them
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
Main()
