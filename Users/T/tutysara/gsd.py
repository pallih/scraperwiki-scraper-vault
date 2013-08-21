import scraperwiki
import urlparse
import lxml.html
import datetime

now = datetime.datetime.now()
date=now.strftime("%Y-%m-%d %H:%M")

print 'hw'
parent='http://www.glassdoor.com'
def get_url(url):
    return scraperwiki.scrape(url)

def gsd_seed_urls(start=1,last=2):
    links=[]
    for i in range(start,last):
        html=None
        try:
            html=get_url('http://www.glassdoor.com/site-directory/company-reviews-'+str(i)+'.htm')
        except Exception, err:
            continue
        root = lxml.html.fromstring(html)
        links=links+ [a.attrib['href'] for a in root.cssselect("div[class='link'] a") if a.attrib['href'].find('/Reviews') >=0]
        #for link in links:
        #   print link.attrib['href'], ":", link.text
    return links



def get_data(url):   
    html=get_url(url)  
    root = lxml.html.fromstring(html)
    dds=root.cssselect("dl[class='ratingValueChart cf'] dd")
    data={}
    if len(dds)>=5 :
        #print "Very Satisfied ", dds[0].text_content()
        data["Very Satisfied"]=dds[0].text_content()
        #print "Satisfied ", dds[1].text_content()
        data["Satisfied"]=dds[1].text_content()
        #print "Neutral ", dds[2].text_content()
        data["Neutral"]=dds[2].text_content()
        #print "Dissatisfied ", dds[3].text_content()
        data["Dissatisfied"]=dds[3].text_content()
        #print "Very Dissatisfied ", dds[4].text_content()
        data["Very Dissatisfied"]=dds[4].text_content()
    rstars=root.cssselect("p span[class='gdRatingStars'] span")
    if len(rstars) >=5:
        #print "Career Opportunities",get_star_val( rstars[0].attrib['style'])
        data["Career Opportunities"]=get_star_val( rstars[0].attrib['style'])
        #print "Compensation & Benefits",get_star_val(rstars[1].attrib['style'])
        data["Compensation and Benefits"]=get_star_val( rstars[1].attrib['style'])
        #print "Work/Life Balance", get_star_val(rstars[2].attrib['style'])
        data["Work Life Balance"]=get_star_val( rstars[2].attrib['style'])
        #print "Senior Leadership", get_star_val(rstars[3].attrib['style'])
        data["Senior Leadership"]=get_star_val( rstars[3].attrib['style'])
        #print "Culture &Values", get_star_val(rstars[4].attrib['style'])
        data["Culture and Values"]=get_star_val( rstars[4].attrib['style'])
    title_e=root.cssselect("title")
    if title_e:
        title=title_e[0].text_content()
        company= title[:title.find("Reviews")]
        #print company
        data["company"]=company

    website_e=root.cssselect("div[class='employerSubheaderData'] span[class='website'] span[class='value']")
    if len(website_e) >0:
        website=website_e[0].text_content()
        #print website
        data["website"]=website
    hq_e=root.cssselect("div[class='employerSubheaderData'] span[class='hq'] span[class='value']")
    if len(hq_e) >0:
        hq=hq_e[0].text_content()
        #print hq   
        data["hq"]=hq
    industry_e=root.cssselect("div[class='value primaryIndustry'] a")
    if len(industry_e) > 0:
        industry=industry_e[0].text_content()
        #print industry
        data["industry"]=industry
    revenue_e=root.cssselect("span[class='revenue']")
    if len(revenue_e) >0 :
        revenue=revenue_e[0].text_content()
        #print revenue
        data["revenue"]=revenue
    noemp_e=root.cssselect("span[class='numEmployees']")
    if len(noemp_e) >0 :
        noemp=noemp_e[0].text_content()
        data["noemp"]=noemp
    data["date"]=date
    data["url"]=url
    #print data
    return data
    
    
   
def get_star_val(s):
    #print s, s.find(':'), s.find('px')
    return s[s.find(':')+1:s.find('px')]

#get_data('http://www.glassdoor.com/Reviews/7city-Learning-Reviews-E284671.htm')
#get_star_val('width:48.0px')


for page_num in range(1,270,4):
    for link in gsd_seed_urls(page_num,page_num+4):
        url= parent+link
        print "trying url - ", url    
        data=None
        try:
            data=get_data(url)
        except Exception, err:
            print "got exception", err
            continue
        print "got data ", data
        scraperwiki.sqlite.save(unique_keys=['url', 'date'], data=data)
