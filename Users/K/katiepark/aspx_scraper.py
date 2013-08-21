import scraperwiki
import mechanize
import re

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

urllist = ['http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=349762&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=353558&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=374394&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=393744&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=397584&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=404487&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=421070&ContributionType=Individual%20Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Semi.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=443833&ContributionType=Individual+Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Quarterly.aspx','http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=452685&ContributionType=Individual+Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Quarterly.aspx']

#for url in urllist:
url = 'http://www.elections.il.gov/CampaignDisclosure/ItemizedContrib.aspx?FiledDocID=452685&ContributionType=Individual+Contributions&Archived=True&OrderBy=LastorOnlyName-AtoZ&ItemizedContribFrom=D2Quarterly.aspx'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

for pagenum in range(99):
    html = response.read()
    #print "Page %d  page length %d" % (pagenum, len(html))
    data = {
        'cname' : re.findall('headers="ctl00.ContentPlaceHolder1.thContributedBy"><span>(.*?)</span>', html),
        'camt' : re.findall('headers="ctl00.ContentPlaceHolder1.thA1Amount"><span>(.*?)<br/?>', html)
    }
    #print cname, camt
    #print "Contribs found:", re.findall('headers="ctl00.ContentPlaceHolder1.thContributedBy"><span>(.*?)</span>', html)
    #print "Contribs found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)
    scraperwiki.sqlite.save(unique_keys=['cname','camt'], data=data)

    mnextlink = re.search("javascript:__doPostBack\('ProviderSearchResultsTable1\$NextLinkButton',''\).>Next Page", html) 
    if not mnextlink:
        break

    br.select_form(name='ctl00')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

