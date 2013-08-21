import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
import json
import re

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
ck = cookielib.Cookie(version=0, name='13206d08-8f08-4ec0-ad95-d7868db06379', value='%7B%22parent_id%22%3A%224dAY_Kd4sVR%22%2C%22referrer%22%3A%22%22%2C%22id%22%3A%22xrOZqwtDO5d%22%2C%22wom%22%3Atrue%2C%22entry_point%22%3A%22http%3A%2F%2Fwww.att.com%2Fsimplybetter%2F%3Fsource%3DIA4r25ODB00WLDZCL%23fbid%3D4dAY_Kd4sVR%22%2C%22url_tag%22%3A%5B%22IA4r25ODB00WLDZCL%22%5D%7D', port=None, port_specified=False, domain='.att.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cj.set_cookie(ck)
br.set_cookiejar(cj)

catUrlPrefix = 'http://www.att.com/esupport/main.jsp?cv=820&ct='
catUrlSuffix = '&pv=3&br=BR'

done = [
'800297',
'800298',
'800299',
'800300',
'800301',
'800348',
'7700008',
'2800006',
'800292',
'5200008',
'800293',
'800294',
'800295',
'6500005',
'800349',
'2700018',
'800321',
'5600013',
'5000007',
'5600010',
'800312',
'800332',
'7500006',
'6500007',
'6500008',
'7600004',
'5600012',
'800322',
'9003624',
'9003625',
'9003626',
'9003627',
'9003628',
'9003629',
'9003622',
'9003623',
'4200008',
'800311',
'2700015',
'800313',
'5400004',
'800317',
'1400006',
'800314',
'800315',
'800316',
'800318',
'800319',
'5300015',
'800323',
'800324',
'4500004',
'1400005',
'800327',
'800326',
'800328',
'800329',
'800333',
'800334',
'1500011',
'800335',
'800336',
'800338',
'7600027',
'1200005',
'1200007',
'800325',
'7700005',
'7700006',
'6200004',
'7800011',
'800432',
'800490',
'9003511',
'9003512',
'800007',
'8000023',
'8200005',
'800010',
'800177',
'800178',
'800179',
'800180',
'800181',
'800182',
'800183',
'800184',
'800185',
'800186',
'800187',
'800188',
'800189',
'800190',
'800191',
'800192',
'800193',
'800194',
'800195',
'800196',
'800197',
'800198',
'800199',
'800200',
'800201',
'800202',
'800203',
'800204',
'6000004',
'7500007',
'7800010',
'2000005',
'8100004',
'7800004',
'4000005',
'9004111',
'7400012',
'4000004',
'5800004',
'9003510',
'5900005',
'9003509',
'800296',
'800291',
'2700016',
'5000006',
'6500006',
'9003621',
'9003619',
'800309',
'1200004',
'7700004',
'9004092',
'800006',
'800009',
'800008',
'800173',
'2600005',
'800340']

questionCategories = [
'800009',
'800173',
'2600005',
'800054',
'800080',
'800114',
'800160',
'800205',
'800259']

def scrapeCats():
    existingCats = scraperwiki.sqlite.execute("select category_id from swdata")
    for qid in questionCategories:
        if [qid] in existingCats['data']:
            print "skipping " + qid 
        else:
            scrapeCatBreadcrumb(catUrlPrefix + qid + catUrlSuffix, qid)


def scrapeCatBreadcrumb(url, qid):
    resp = scraperwiki.scrape(url)
    soup = BeautifulSoup(resp)
    title = soup.find('title')
    l = len(title.text)
    newTitle = title.text[9:l]
    newTitle = newTitle[0:l-47]
    print newTitle
    scrpts = soup.findAll('script', attrs= { "type" : "text/javascript" } )
    for scrpt in scrpts:
        if scrpt.text.startswith( 'var vanityurl = ' ):
            print scrpt.text[17:110]
            record = {}
            record['category_id'] = qid
            record['path'] = scrpt.text[17:114]
            record['category_name'] = newTitle
            scraperwiki.sqlite.save(unique_keys=['category_id'], data=record)


def scrapeAnswer():
    newAns = ansUrl.split("&")
    newUrl = newAns[0] + '&cv=820&pv=3#fbid=3wIKRvJW481'
    res = scraperwiki.sqlite.execute("select * from swdata where url == '" + newUrl +"'")
    if res["data"]:
        print 'Skipping (Q and A already saved)'
    else:
        print 'Answer URL: ' + newUrl
        response = br.open(newUrl)
        ansSoup = BeautifulSoup(response.read())
        ansDivs = ansSoup.findAll('div', attrs={ 'class' : 'answerContent'} )
        # print 'Answer: ' + ansDivs[1].text
        # print ansDivs[1]
        record = {}
        record['url'] = newUrl
        record['question'] = question
        last = len(ansDivs)
        if len(ansDivs) > 1:
            record['answerText'] = ansDivs[last - 1].text
            record['answerHtml'] = ansDivs[last - 1]
        scraperwiki.sqlite.save(unique_keys=['url'], data=record)

def parsePaths():
    existingCats = scraperwiki.sqlite.execute("select category_id from swdata")
    existingPaths = scraperwiki.sqlite.execute("select category_id, path from swdata")
    data = existingPaths['data']
    cats = existingCats['data']
    c = 0
    unrecorded = []
    while c < len(data):
        st = data[c][1].replace("&#039;","").split(",")
        for s in st:
            if s == '800005':
                break
            if [s] not in cats:
                if s not in unrecorded:
                    unrecorded.append(s)
                    print s
        c = c+1
    print c
    print len(unrecorded)
    print unrecorded

def updatePaths():
    existingCats = scraperwiki.sqlite.execute("select category_id from swdata")
    existingPaths = scraperwiki.sqlite.execute("select category_id, path, category_name from swdata")
    data = existingPaths['data']
    cats = existingCats['data']
    c = 0
    while c < len(data):
        st = data[c][1]
        st = st.replace("&#039;","").split(",")
        #print cats[c]
        # print st[1]
        record = {}
        record['category_id'] = st[0]
        record['path'] = data[c][1]
        record['category_name'] = data[c][2]
        record['parent_category_id'] = st[1]
        print record
        c = c+1
        scraperwiki.sqlite.save(unique_keys=['category_id'], data=record)

scrapeCats()
#parsePaths()
updatePaths()

