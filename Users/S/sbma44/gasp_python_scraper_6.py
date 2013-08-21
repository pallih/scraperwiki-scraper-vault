import scraperwiki, lxml, lxml.html, time, re
gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


gasp = gasp_helper.GaspHelper("130e13701b67494f95b71f873116ed82", "K000362")



STEVE_KING_ROOT_URL = 'http://steveking.house.gov'
STEVE_KING_PRESS_RELEASE_URL = "%s/index.php?option=com_content&view=article&id=4068&Itemid=300099" % STEVE_KING_ROOT_URL

index = lxml.html.parse(STEVE_KING_PRESS_RELEASE_URL).getroot()

# grab social media
re_leave_site = re.compile(r'/htbin/leave_site\?ln_url=(?P<url>.+)')
for sm_link in index.cssselect('#connect ul li a'):
    match = re_leave_site.search(sm_link.attrib['href'])
    if match:
        sm_url = match.group('url') 
        for service_name in ('flickr', 'youtube', 'facebook', 'twitter'):
            if service_name in sm_url:
                gasp.add_social_media(service_name, sm_url)




# grab press releases
for press_release_link in index.cssselect("#idGtReportDisplay li a"):
    press_release_url = press_release_link.attrib['href']

    print "fetching %s" % press_release_url
    press_release = lxml.html.parse("http://steveking.house.gov%s" % press_release_url).getroot()
    
    title = press_release.cssselect("h2.contentheadingfull")[0].text.strip()
    date = press_release.cssselect("span.createdate")[0].text.strip()
    content = lxml.etree.tostring(press_release.cssselect("div#pagefull")[0])

    cleaned_content = ""
    forbidden_strings = ('class="articleinfo"', 'class="buttonheading"', 'class="createdate"', '###')
    for content_section in map(lambda x: x.strip(), content.split("</p>")):
        
        include_section = True
        for fs in forbidden_strings:
            if fs in content_section: 
                include_section = False

        if include_section:
            cleaned_content += "%s</p>" % content_section

    
    (title, date, cleaned_content) = map(lambda x: x.replace('&#13;','').strip(), (title, date, cleaned_content))
    
    gasp.add_press_release(title, date, cleaned_content)
    
    time.sleep(2)


gasp.finish()