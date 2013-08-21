import scraperwiki
import mechanize
import re



url = 'http://agenda.co.brazos.tx.us'
br = mechanize.Browser()
br.addheaders = [('User-agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')]
response = br.open(url)



for pagenum in range(10):               #re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)
    
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    print "Clinicians found:", re.findall("MeetingView.aspx\?MeetingID.*?(a)</a>", html)

    mnextlink = re.search("javascript:__doPostBack('SearchAgendasMeetings$radGridMeetings$ctl00$ctl03$ctl01$ctl07", html)
    if not mnextlink:
        break

    br.select_form(name='ctl00') 
    br.form.set_all_readonly(False) 
    br['__EVENTTARGET'] = 'SearchAgendasMeetings$radGridMeetings$ctl00$ctl03$ctl01$ctl07'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()
#Need to set event target to something. ^Obviously doesn't work.
