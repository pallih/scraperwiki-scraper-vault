import scraperwiki
#import inspect
import lxml.html 
import re

#Load the html of the All Conferences physics page
html = scraperwiki.scrape("http://www.allconferences.com/search/index/Category__parent_id:440828/showLastConference:0/") 

root = lxml.html.fromstring(html) 

eventlist = root.cssselect('div.listing')

for event in eventlist :
    
#This is a random number assigned to each conference, not using it but could use it as a unique marker instead of the name
    eventid = event.get('id')

    confname_css = event.cssselect('h2')[0]
    confname = confname_css.text_content()
    
    venueinfo_css = event.cssselect('div.venue_info')[0]

    venuelinks_css = venueinfo_css.cssselect('a')
    
    venue1 =  venuelinks_css[0].text_content()
    venue2 =  venuelinks_css[1].text_content()
    venue3 =  venuelinks_css[2].text_content()
    
    date_css = event.cssselect('div.conferenceDate')[0]
    
    datebegin = date_css.cssselect('span.begin_txt')[0].text_content()
    if datebegin.startswith('BEGINS') :
        datebegin = datebegin[9:]

    dateend = date_css.cssselect('span.end_txt')[0].text_content()
    if dateend.startswith('Ends') :
         dateend = dateend[5:]   
    
    
# Follow event link to find website url

    link = event.cssselect('h2 a')[0].get('href')
    
    try:
        html2 =  scraperwiki.scrape(link)
        root2 = lxml.html.fromstring(html2)

        webbutton = root2.cssselect('button.eventWebsite')[0]


#Not ideal, using regular expression to find the link in the button
        click = webbutton.get('onclick')

        p = r'window.open\(\'([A-Za-z0-9.:/]+)\'\)'
        url = re.findall(p,click)[0]

    except:
        #There is no page, so can't get url
        url =''


        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue1+', '+venue2+', '+venue3, 'datebegin':datebegin, 'dateend':dateend})           
    
    



import scraperwiki
#import inspect
import lxml.html 
import re

#Load the html of the All Conferences physics page
html = scraperwiki.scrape("http://www.allconferences.com/search/index/Category__parent_id:440828/showLastConference:0/") 

root = lxml.html.fromstring(html) 

eventlist = root.cssselect('div.listing')

for event in eventlist :
    
#This is a random number assigned to each conference, not using it but could use it as a unique marker instead of the name
    eventid = event.get('id')

    confname_css = event.cssselect('h2')[0]
    confname = confname_css.text_content()
    
    venueinfo_css = event.cssselect('div.venue_info')[0]

    venuelinks_css = venueinfo_css.cssselect('a')
    
    venue1 =  venuelinks_css[0].text_content()
    venue2 =  venuelinks_css[1].text_content()
    venue3 =  venuelinks_css[2].text_content()
    
    date_css = event.cssselect('div.conferenceDate')[0]
    
    datebegin = date_css.cssselect('span.begin_txt')[0].text_content()
    if datebegin.startswith('BEGINS') :
        datebegin = datebegin[9:]

    dateend = date_css.cssselect('span.end_txt')[0].text_content()
    if dateend.startswith('Ends') :
         dateend = dateend[5:]   
    
    
# Follow event link to find website url

    link = event.cssselect('h2 a')[0].get('href')
    
    try:
        html2 =  scraperwiki.scrape(link)
        root2 = lxml.html.fromstring(html2)

        webbutton = root2.cssselect('button.eventWebsite')[0]


#Not ideal, using regular expression to find the link in the button
        click = webbutton.get('onclick')

        p = r'window.open\(\'([A-Za-z0-9.:/]+)\'\)'
        url = re.findall(p,click)[0]

    except:
        #There is no page, so can't get url
        url =''


        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue1+', '+venue2+', '+venue3, 'datebegin':datebegin, 'dateend':dateend})           
    
    



