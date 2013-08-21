import scraperwiki,requests,lxml.html

# Blank Python

starturl='http://soccernet.espn.go.com/results/_/league/eng.1/barclays-premier-league' # always utd
xpath="//div[contains(concat(' ',normalize-space(@class),' '),' %s ')]" # http://pivotallabs.com/users/alex/blog/articles/427-xpath-css-class-matching

def scrapeurlw(url, saver=True):
    buildup=[]
    html=requests.get(url).content
    myteam=lxml.html.fromstring(html).get_element_by_id('my-teams-table')
    prev=myteam.cssselect('strong a')[0]
    previous=prev.attrib['href']
    try:
        assert prev.text_content().strip()=='Previous Games' # watch for termination
    except:
        previous=None
    for row in myteam.cssselect("tr td[align='center']"):
        if row.text_content().strip() == "Score":
            continue
        data={'url':row.cssselect("a")[0].attrib['href']}
        if saver:
            scraperwiki.sqlite.save(unique_keys=['url'], data=data, table_name='prem-walker')
        else:
            buildup.append(data)
    
    if saver:
        scraperwiki.sqlite.save_var('nexturl', previous)
        return previous
    else:
        return buildup


#url=starturl

# used for first scraping
#url=scraperwiki.sqlite.get_var('nexturl')
#while url != None:
#    url=scrapeurlw(url)
