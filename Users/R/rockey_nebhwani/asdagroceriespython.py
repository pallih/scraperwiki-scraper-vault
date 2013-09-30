import os
import sqlite3
import cookielib
import urllib2
 
COOKIE_DB = "{home}/.mozilla/firefox/cookies.sqlite".format(home=os.path.expanduser('~'))
CONTENTS = "host, path, isSecure, expiry, name, value"
COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
URL = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'
 
 
def get_cookies(host):
    # based on http://www.guyrutenberg.com/2010/11/27/building-cookiejar-out-of-firefoxs-cookies-sqlite/
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    con = sqlite3.connect(COOKIE_DB)
    cur = con.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cur.execute(sql)
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)

    return cj
 
 
def get_page_with_cookies(cj):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    theurl = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'   # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
    txdata = None   # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
    #params = {}
    #txdata = urllib.urlencode(params)
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}  # fake a user agent, some websites (like google) don't like automated exploration

    req = urllib2.Request(theurl, txdata, txheaders)    # create a request object
    handle = urllib2.urlopen(req)                       # and open it to return a handle on the url

    return handle.read()
 
 
def main():
    host = 'groceries.asda.com'
    cj = get_cookies(host)
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie
    #cj.save(COOKIEFILE)                     # save the cookies (not necessary)
print get_page_with_cookies(cj)
 
 
if __name__=="__main__":
    main()import os
import sqlite3
import cookielib
import urllib2
 
COOKIE_DB = "{home}/.mozilla/firefox/cookies.sqlite".format(home=os.path.expanduser('~'))
CONTENTS = "host, path, isSecure, expiry, name, value"
COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
URL = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'
 
 
def get_cookies(host):
    # based on http://www.guyrutenberg.com/2010/11/27/building-cookiejar-out-of-firefoxs-cookies-sqlite/
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    con = sqlite3.connect(COOKIE_DB)
    cur = con.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cur.execute(sql)
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)

    return cj
 
 
def get_page_with_cookies(cj):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    theurl = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'   # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
    txdata = None   # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
    #params = {}
    #txdata = urllib.urlencode(params)
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}  # fake a user agent, some websites (like google) don't like automated exploration

    req = urllib2.Request(theurl, txdata, txheaders)    # create a request object
    handle = urllib2.urlopen(req)                       # and open it to return a handle on the url

    return handle.read()
 
 
def main():
    host = 'groceries.asda.com'
    cj = get_cookies(host)
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie
    #cj.save(COOKIEFILE)                     # save the cookies (not necessary)
print get_page_with_cookies(cj)
 
 
if __name__=="__main__":
    main()import os
import sqlite3
import cookielib
import urllib2
 
COOKIE_DB = "{home}/.mozilla/firefox/cookies.sqlite".format(home=os.path.expanduser('~'))
CONTENTS = "host, path, isSecure, expiry, name, value"
COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
URL = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'
 
 
def get_cookies(host):
    # based on http://www.guyrutenberg.com/2010/11/27/building-cookiejar-out-of-firefoxs-cookies-sqlite/
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    con = sqlite3.connect(COOKIE_DB)
    cur = con.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cur.execute(sql)
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)

    return cj
 
 
def get_page_with_cookies(cj):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    theurl = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'   # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
    txdata = None   # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
    #params = {}
    #txdata = urllib.urlencode(params)
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}  # fake a user agent, some websites (like google) don't like automated exploration

    req = urllib2.Request(theurl, txdata, txheaders)    # create a request object
    handle = urllib2.urlopen(req)                       # and open it to return a handle on the url

    return handle.read()
 
 
def main():
    host = 'groceries.asda.com'
    cj = get_cookies(host)
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie
    #cj.save(COOKIEFILE)                     # save the cookies (not necessary)
print get_page_with_cookies(cj)
 
 
if __name__=="__main__":
    main()import os
import sqlite3
import cookielib
import urllib2
 
COOKIE_DB = "{home}/.mozilla/firefox/cookies.sqlite".format(home=os.path.expanduser('~'))
CONTENTS = "host, path, isSecure, expiry, name, value"
COOKIEFILE = 'cookies.lwp'          # the path and filename that you want to use to save your cookies in
URL = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'
 
 
def get_cookies(host):
    # based on http://www.guyrutenberg.com/2010/11/27/building-cookiejar-out-of-firefoxs-cookies-sqlite/
    cj = cookielib.LWPCookieJar()       # This is a subclass of FileCookieJar that has useful load and save methods
    con = sqlite3.connect(COOKIE_DB)
    cur = con.cursor()
    sql = "SELECT {c} FROM moz_cookies WHERE host LIKE '%{h}%'".format(c=CONTENTS, h=host)
    cur.execute(sql)
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        #print c
        cj.set_cookie(c)

    return cj
 
 
def get_page_with_cookies(cj):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    theurl = 'http://groceries.asda.com/asda-estore/search/searchcontainer.jsp?trailSize=1&searchString=brandy&domainName=Products&headerVersion=v1&_requestid=15405'   # an example url that sets a cookie, try different urls here and see the cookie collection you can make !
    txdata = None   # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
    #params = {}
    #txdata = urllib.urlencode(params)
    txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}  # fake a user agent, some websites (like google) don't like automated exploration

    req = urllib2.Request(theurl, txdata, txheaders)    # create a request object
    handle = urllib2.urlopen(req)                       # and open it to return a handle on the url

    return handle.read()
 
 
def main():
    host = 'groceries.asda.com'
    cj = get_cookies(host)
    for index, cookie in enumerate(cj):
        print index, '  :  ', cookie
    #cj.save(COOKIEFILE)                     # save the cookies (not necessary)
print get_page_with_cookies(cj)
 
 
if __name__=="__main__":
    main()