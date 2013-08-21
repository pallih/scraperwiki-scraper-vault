import mechanize 
import urllib2
import scraperwiki
import lxml.html
import string
import re
import HTMLParser


from htmlentitydefs import name2codepoint
def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint), 
            lambda m: unichr(name2codepoint[m.group(1)]), s)

h = HTMLParser.HTMLParser()

loginUrl = "http://agorapublix.com/forum3/index.php?action=login"
loginFormName = "frmLogin"
loginUserField = "user"
loginUser = ""
loginPasswordField = "passwrd"
loginPassword = ""

tableUrlformat = "http://agorapublix.com/forum3/index.php?action=mlist;sort=realName;start="
pagestart = 0
pagestep = 100
page = 0
pagemax = 999999

br = mechanize.Browser()
response = br.open(loginUrl)
br.select_form(name=loginFormName)

br[loginUserField] = loginUser
br[loginPasswordField] = loginPassword 

response = br.submit()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(br._ua_handlers["_cookies"].cookiejar))

uniquekey = 0

while page < pagemax :
    pagestart = pagestep * page
    page = page + 1
    
    url = tableUrlformat + str(pagestart)
    print "page " + str(page) + " " + url
    s = opener.open(url)
    html = lxml.html.fromstring(s.read())
    bodyarea = html.cssselect("td#bodyarea")[0] 

    if page == 1 :
        sel = lxml.html.tostring(bodyarea)
        membersNb = int( re.search('([0-9]+)\s*total des membres', sel).group(1) )
        pagemax =  int(membersNb/pagestep) + 1
        print "membersNb=" + str(membersNb) + " " + "pagemax=" + str(pagemax)

    i = 0
    for tr in bodyarea.cssselect("tr"):
        i = i + 1
        if i > 4 :
            tds = tr.cssselect("td")
            if len(tds) > 1 :
                uniquekey = uniquekey + 1
                data = {
                    'N': uniquekey,
                    # 'Etat' : lxml.html.tostring(tds[0]),
                    'Identifiant' :  h.unescape(htmlentitydecode(re.search('>([^<]+)</a>',lxml.html.tostring(tds[1])).group(1))),
                    #'Courriel' : lxml.html.tostring(tds[2]),
                    #'SiteWeb' : lxml.html.tostring(tds[3]),
                    #'ICQ' : lxml.html.tostring(tds[4]),
                    #'AOLIM' : lxml.html.tostring(tds[5]),
                    #'YahooIM' : lxml.html.tostring(tds[6]),
                    #'MSNIM' : lxml.html.tostring(tds[7]),
                    'Rang' : h.unescape(htmlentitydecode(re.search('>([^<]+)</td>',lxml.html.tostring(tds[8])).group(1))),
                    'Inscritle' : h.unescape(re.search('>([^<]+)</td>',lxml.html.tostring(tds[9])).group(1)),
                    'Messages' : h.unescape(re.search('>([^<]+)</td>',lxml.html.tostring(tds[10])).group(1).replace('.',''))
                }
                scraperwiki.sqlite.save(unique_keys=['N'], data=data)
