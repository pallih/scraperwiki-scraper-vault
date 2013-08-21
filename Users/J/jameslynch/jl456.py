import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
ck = cookielib.Cookie(version=0, name='13206d08-8f08-4ec0-ad95-d7868db06379', value='%7B%22parent_id%22%3A%224dAY_Kd4sVR%22%2C%22referrer%22%3A%22%22%2C%22id%22%3A%22xrOZqwtDO5d%22%2C%22wom%22%3Atrue%2C%22entry_point%22%3A%22http%3A%2F%2Fwww.att.com%2Fsimplybetter%2F%3Fsource%3DIA4r25ODB00WLDZCL%23fbid%3D4dAY_Kd4sVR%22%2C%22url_tag%22%3A%5B%22IA4r25ODB00WLDZCL%22%5D%7D', port=None, port_specified=False, domain='.att.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cj.set_cookie(ck)
br.set_cookiejar(cj)

testUrlPrefix = 'http://www.att.com/esupport/main/middleColumn.jsp?ct='
testUrlSuffix = '&pv=2&rpp=300&sv=1'

existingUrls = []

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
'9003509']

spares = ['800296',
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

def scrapeQandAs():
    # resUrls = scraperwiki.sqlite.execute("select url from swdata")
    # existingUrls = resUrls["data"]
    for qid in questionCategories:
        print '================= Question Category ' + qid + ' ================='
        scrapeQuestionList(testUrlPrefix + qid + testUrlSuffix)

def scrapeQuestionList(url):
    testHtml = scraperwiki.scrape(url)
    testSoup = BeautifulSoup(testHtml)
    divs = testSoup.findAll('div', attrs={ 'class' : 'desclft'} )
    i = 0;
    for div in divs:
        # print 'Question: ' + div.input['value']
        scrapeAnswer(div.input['value'], 'http://www.att.com' + div.a['href']) 
        if i % 10 == 0:
            print 'questions complete: '
            print i
        i = i + 1;

def scrapeAnswer(question, ansUrl):
    newAns = ansUrl.split("&")
    newUrl = newAns[0] + '&cv=820&pv=3#fbid=3wIKRvJW481'
    res = scraperwiki.sqlite.execute("select * from swdata where url == '" + newUrl +"'")
    if res["data"]:
        print 'Skipping (Q and A already saved)'
    else:
        # print 'Answer URL: ' + newUrl
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
            record['isNew'] = 'true'
        scraperwiki.sqlite.save(unique_keys=['url'], data=record)

def scrapeMissingQandAs():
    missingAnswersUrls = scraperwiki.sqlite.execute("select url, question from swdata where answerText == ''")
    urls = missingAnswersUrls['data']
    c= 0
    print len(urls)
    while c < len(urls):
        print c
        scrapeAnswer(urls[c][1], urls[c][0])
        c = c+1

scrapeQandAs()
#scrapeMissingQandAs()

