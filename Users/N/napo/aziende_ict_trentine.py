#TODO
# extract the information for each single company
# => other form where submit the data  by using the code with the formula 'DGAziende$' + code + '$LBTRagioneSociale'

#thanks to
#http://blog.scraperwiki.com/2011/11/09/how-to-get-along-with-an-asp-webpage/
#https://scraperwiki.com/docs/contrib/python_asp_cheat_sheet/
import mechanize
import lxml.html
import scraperwiki
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open("http://www.icttrentino.it/frontend/ricerca_aziendale.aspx/")
br.select_form("form1")
br.set_all_readonly(False)
br["__EVENTTARGET"] = "LBTutte"
br["__EVENTARGUMENT"] = ""
response = br.submit()
html = response.read()
doc = lxml.html.fromstring(html)

def detailscompany(code):
    print code
    browser = mechanize.Browser()
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    browser.open("http://www.icttrentino.it/frontend/ricerca_aziendale.aspx/ricerca_aziendale.aspx")
    browser.select_form("form1")
    browser.set_all_readonly(False)
    browser["__EVENTTARGET"] = code
    browser["__EVENTARGUMENT"] = ""
    answer = browser.submit()
    page = answer.read()
    info = lxml.html.fromstring(html)
    tables = info.cssselect("table")
    for t in tables:
        print t.text_content()

i = 0
k = 0
tot = 0
data = {}
for tds in doc.cssselect("table#DGAziende tr td"):
    if (k > 5):
        if ( i >= 0):
            if (i == 0):
                name = tds.getchildren()[0].text_content()
                code = tds.getchildren()[0].attrib['href']
                code = code.replace("javascript:__doPostBack('","")
                code = code.replace("','')","")
                detailscompany(code)
                code = code.replace('DGAziende$','')
                code = code.replace('$LBTRagioneSociale','')
                
            if (i == 1):
                place = tds.text_content()
                #place = unicode(place, "utf-8")
            if (i == 2):
                address = tds.text_content()
                #address = unicode(place, "utf-8")
            if (i == 3):
                phone = tds.text_content()
            if (i == 4):
                email = tds.text_content()
            if (i == 5):
                lastupdate = tds.text_content()
            i = i +1
            if (i > 5):
                i = 0
                tot = tot +1
                data = { 'id' : tot,
                         'code' : code,
                         'name' : name,
                         'place' : place,
                         'address': address,
                         'phone' : phone,
                         'email': email,
                         'lastupdate': lastupdate}   
                scraperwiki.sqlite.save(unique_keys=['code'], data=data)
    if tot == 1:
        break
    k= k +1


