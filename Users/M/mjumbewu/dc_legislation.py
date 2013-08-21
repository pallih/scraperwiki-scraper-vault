import mechanize
import scraperwiki
from lxml.html import fromstring, tostring
from urllib2 import urlopen

def scrape_legislation_list(list_html):
    # Make a useful structure from that HTML.
    legislation_list = fromstring(list_html)
    
    # Find all the rows.
    rows = legislation_list.cssselect('#DataGrid tr')
    
    links = []
    for row in rows:
        # If it's a header row, skip it.
        if 'class' in row.attrib and row.attrib['class'] == 'DataGridHeader':
            continue
    
        # If it's the "pager" row (at the bottom), skip it.
        if 'class' in row.attrib and row.attrib['class'] == 'DataGridPager':
            continue
    
        # Otherwise, add the link in the row to the list of links.
        #anchor = row.cssselect('a')[0]
        #links.append(anchor.attrib['href'])
        idno = row.cssselect('td')[0].text
        links.append('http://dcclims1.dccouncil.us/lims/legislation.aspx?LegNo=%s' % idno)
    
    for legislation_url in links:
        legislation_html = urlopen(legislation_url).read()
        legislation_data = fromstring(legislation_html)
    
        record = {
            'url': legislation_url,
            'title' : legislation_data.cssselect('#LegislationTitle')[0].text,
            'idno' : legislation_data.cssselect('#LegislationNo')[0].text,
            'actnogi' : legislation_data.cssselect('#ActNoGI')[0].text,
            'lawno' : legislation_data.cssselect('#LawNo')[0].text,
            'dateexpirationgi' : legislation_data.cssselect('#DateExpirationGI')[0].text,
            'dateenactmentgi' : legislation_data.cssselect('#DateEnactmentGI')[0].text,
            'dateeffectivegi' : legislation_data.cssselect('#DateEffectiveGI')[0].text,
        
            # TODO: Links are in #DocumentRepeater_ctl00_DocumentPanel
        
            'introducers' : legislation_data.cssselect('#IntroducedBy')[0].text,
            'cosponsors' : legislation_data.cssselect('#CoSponsoredBy')[0].text,
        }
    
        scraperwiki.sqlite.save(unique_keys=["idno"], data=record)

def scrape_and_look_for_next_link(current_page, list_html):
    print list_html
    #scrape_legislation_list(list_html)
    legislation_list = fromstring(list_html)
    
    print 'page ', current_page
    next_page = 'Page$%s' % (current_page + 1)
    next_link = legislation_list.cssselect('''a[href="javascript:__doPostBack('DataGrid','%s')"]''' % next_page)
    print 'looking for', '''a[href="javascript:__doPostBack('DataGrid','%s')"]''' % next_page
    if next_link:
        # find the page's form
        br.select_form(name='AdminForm')
        br.form.set_all_readonly(False)
        # set the relevant ASP.NET fields, as required in the page's onSubmit function
        # Your .aspx page may not have these
        # Luckily we can ignore the __VIEWSTATE variable: mechanize handles this for us.
        br['__EVENTTARGET'] = 'DataGrid'
        br['__EVENTARGUMENT'] = next_page
#        br['__EVENTVALIDATION'] = legislation_list.cssselect('#__EVENTVALIDATION')[0].attrib['value']
#        br['__VIEWSTATE'] = legislation_list.cssselect('#__VIEWSTATE')[0].attrib['value']
#        br['__PREVIOUSPAGE'] = legislation_list.cssselect('#__PREVIOUSPAGE')[0].attrib['value']
#        br['SelectedIndexNo'] = '0'
#        br['intLegID'] = '0'
#        br['PageHeader$SiteSearchOption'] = ['CouncilMembers']
#        br['PageHeader$SiteSearchText'] = 'Address Search'
#        br['Period'] = ['19']

        br.submit()
        new_list_html = br.response().read()
        scrape_and_look_for_next_link(current_page + 1, new_list_html)

# Download the HTML from the council legislation list.  We use the print listing because
# it allows us to get all the legislation without paging through lists.
list_url = 'http://dcclims1.dccouncil.us/lims/print/list.aspx?FullPage=True&Period=19'

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(list_url)

list_html = br.response().read()
scrape_legislation_list(list_html)
