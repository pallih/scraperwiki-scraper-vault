import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

urllist = ['']

#for url in urllist:
url = 'http://www.elections.il.gov/CampaignDisclosure/ItemizedExpend.aspx?FiledDocID=463066&ExpenditureType=Expenditures&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedExpendFrom=D2Quarterly.aspx'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(99):
    html = response.read()
    
    recipients = re.findall('headers="ctl00_ContentPlaceHolder1_thCreditor"><span>(.*?)</span>', html)
    amounts    = re.findall('headers="ctl00_ContentPlaceHolder1_thAmount"><span>(.*?)<br/?>', html)
    dates      = re.findall('headers="ctl00_ContentPlaceHolder1_thAmount"><span>\$(?:[0-9]+,)*[0-9]+\.[0-9][0-9]<br/?>(.*?)</span>', html)
    purposes   = re.findall('headers="ctl00_ContentPlaceHolder1_thPurpose"><span>(.*?)</span>', html)
    
    data = [{'recipient': recipients[i], 'amount': amounts[i],
             'date': dates[i], 'purpose': purposes[i]} for i in range(len(recipients))]

#    print data
    scraperwiki.sqlite.save(unique_keys=['recipient','amount','date','purpose'], data=data)

    mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
    if not mnextlink:
        break

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

urllist = ['']

#for url in urllist:
url = 'http://www.elections.il.gov/CampaignDisclosure/ItemizedExpend.aspx?FiledDocID=463066&ExpenditureType=Expenditures&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedExpendFrom=D2Quarterly.aspx'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(99):
    html = response.read()
    
    recipients = re.findall('headers="ctl00_ContentPlaceHolder1_thCreditor"><span>(.*?)</span>', html)
    amounts    = re.findall('headers="ctl00_ContentPlaceHolder1_thAmount"><span>(.*?)<br/?>', html)
    dates      = re.findall('headers="ctl00_ContentPlaceHolder1_thAmount"><span>\$(?:[0-9]+,)*[0-9]+\.[0-9][0-9]<br/?>(.*?)</span>', html)
    purposes   = re.findall('headers="ctl00_ContentPlaceHolder1_thPurpose"><span>(.*?)</span>', html)
    
    data = [{'recipient': recipients[i], 'amount': amounts[i],
             'date': dates[i], 'purpose': purposes[i]} for i in range(len(recipients))]

#    print data
    scraperwiki.sqlite.save(unique_keys=['recipient','amount','date','purpose'], data=data)

    mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
    if not mnextlink:
        break

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

