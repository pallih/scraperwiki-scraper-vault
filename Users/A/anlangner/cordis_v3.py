import scraperwiki
import scrapemark
import feedparser
import csv
import re
import urllib2,sys
import requests
import lxml.html
from BeautifulSoup import BeautifulSoup, NavigableString






# extract project page links from the result page "url"
def extract_links(url):
    atom_feed = feedparser.parse(url)
    link_list = []    


    for entry in atom_feed.entries:
        print entry.title #+ " - " + entry.link
        print entry.link

#        experiment with data structure
        data = {
            'TITLE' : entry.title,
            'LINK' : entry.link
        }
        print data
        #scraperwiki.sqlite.save(unique_keys=['TITLE'], data=data)

        link_list.append(entry.link)
        #csvwriter.writerow([entry.title] + [entry.link])
    return link_list

# open details page for "object" and parse the results
def parse_object(object):
    html = urllib2.urlopen(object).read()
    soup = BeautifulSoup(html)
    project_id = soup.find('input', attrs={'name':"REF"}).get('value')
    print "Project-ID: " + str(project_id)

    detail_url = "http://cordis.europa.eu/newsearch/getDoc?doctype=PROJ&xslt-template=projects/xsl/projectdet_en.xslt&rcn=" + str(project_id)
    print "***" + detail_url

    details = requests.get(detail_url)
    detail_page = details.content

    content = BeautifulSoup(detail_page, convertEntities="html", smartQuotesTo="html", fromEncoding="utf-8")

    # extract content
    data_info = content.find(attrs={'class':'projdates'})
    data_coordinator = content.find(attrs={'class': 'projcoord'})
    data_details = content.find(attrs={'class': 'projdet'})
    data_participants = content.find(attrs={'class': 'participants'})
    data_footer = content.find(attrs={'id': 'recinfo'})
    # data_tech = content.find(attrs={'class': 'tech'})
    
    # trying to find project description: display all content
    print ">>> " str(content)

    data_info = lxml.html.fromstring(str(data_info))
    data_info = data_info.text_content()

    data_coordinator = lxml.html.fromstring(str(data_coordinator))
    data_coordinator = data_coordinator.text_content()

    data_details = lxml.html.fromstring(str(data_details))
    data_details = data_details.text_content()

    data_participants = lxml.html.fromstring(str(data_participants))
    data_participants = data_participants.text_content()

    data_footer = lxml.html.fromstring(str(data_footer))
    data_footer = data_footer.text_content()



# REGEXP for fields
# Start date in YYYY-MM-DD: (?<=From\s).{1,}(?=\sto)
# End date in YYYY-MM-DD: (?<=to\s).{1,}(?=\s\|)
# Coordinator: (?<=Coordinator\s).{1,}(?=\s\(\+\))
# Coordinator contact: (?<=Administrative contact:\s).{1,}(?!\n)
# Project title in caps: (?<=\|\s).{1,}(?=\swebsite)
# Cost in EUR: (?<=EUR\s)\d{1,2}(\s\d{3}){1,2}
# EU Contribution: (?<=EU contribution: EUR\s)\d{1,2}(\s\d{3}){1,2}(?!Programme)
# Programme acronym: (?<=Programme acronym:\s)(\w{1,}.){2}
# Contract type: (?<=Contract type:\s).{1,}
# Subprogramme type: (?<=Subprogramme area:\s).{1,}(?=Contract)
# Participants: (?<=\n).{1,}?\n.{1,}?(?=\s\n)
# Participant contact: (?<=Administrative contact:\s).{1,}\n.{1,}(?=Email)
# Record number: (?<=Record number:\s)\d{1,}(?=\s\/)


    field_regexp = {
        'Title' : '(?<=\|\s).{1,}(?=\swebsite)',
        'Start date' : '(?<=From\s).{1,}(?=\sto)',
        'End date' : '(?<=to\s).{1,}(?=\s\|)',
        'Coordinator' : '(?<=Coordinator\n\n).{1,}(?=\n)',
        'Coordinator contact' : '(?<=Administrative contact:\s).{1,}\n.{1,}(?!Email)',
        'Project cost' : '(?<=EUR\s)\d{1,2}(\s\d{3}){1,2}',
        'EU contribution' : '(?<=EU contribution: EUR\s)\d{1,2}(\s\d{3}){1,2}(?!Programme)',
        'Programme' : '(?<=Programme acronym:\s\n)(\w{1,}.){2}',
        'Subprogramme' : '(?<=Subprogramme area:\s\n).{1,}(?=\n)',
        'Contract' : '(?<=Contract type:\s\n).{1,}',
        'Participants' : '(?<=\n).{1,}?\n.{1,}?(?=\s\n)',
        'Participant contact' : '(?<=Administrative contact:\s).{1,}\n.{1,}(?=Email)',
        'Record number' : '(?<=Record number:\s)\d{1,}(?=\s\/)'
    }




# WAAAAH, das hier ist unsagbar hässlich!
    project_title = re.search(field_regexp['Title'], data_info)
    project_title = project_title.group()


    project_start = re.search(field_regexp['Start date'], data_info)
    project_start = project_start.group()

    project_end = re.search(field_regexp['End date'], data_info)
    project_end = project_end.group()
    
    project_coordinator = re.search(field_regexp['Coordinator'], data_coordinator)
    project_coordinator = project_coordinator.group()    

    project_coord_con = re.search(field_regexp['Coordinator contact'], data_coordinator)
    project_coord_con = project_coord_con.group()

    project_cost = re.search(field_regexp['Project cost'], data_details)
    project_cost = project_cost.group()
    project_cost = project_cost.replace(" ", "")

    project_contribution = re.search(field_regexp['EU contribution'], data_details)
    project_contribution = project_contribution.group()
    project_contribution = project_contribution.replace(" ", "")   

    project_programme = re.search(field_regexp['Programme'], data_details)
    project_programme = project_programme.group()

    project_subprogramme = re.search(field_regexp['Subprogramme'], data_details)
    project_subprogramme = project_subprogramme.group()

    project_contract = re.search(field_regexp['Contract'], data_details)
    project_contract = project_contract.group()

    project_participants = re.findall(field_regexp['Participants'], data_participants)
    #project_participants = project_participants.group()


    project_part_con = re.findall(field_regexp['Participant contact'], data_participants)
    #project_part_con = project_part_con.group()

    project_reference = re.search(field_regexp['Record number'], data_footer)
    project_reference = project_reference.group()


    project_desc = {
        'Title' : project_title,
        'Start date' : project_start,
        'End date' : project_end,
        'Coordinator' : project_coordinator,
        'Coordinator contact' : project_coord_con,
        'Project cost' : project_cost,
        'EU contribution' : project_contribution,
        'Programme' : project_programme,
        'Subprogramme' : project_subprogramme,
        'Contract' : project_contract,
        #'Participants' : project_participants[0],
        #'Participant contact' : project_part_con[0],
        'Reference' : project_reference
    }



    scraperwiki.sqlite.save(unique_keys=['Title'], data=project_desc)


print ">>> CORDIS scraper <<<"


applicants = ["rexroth"]

URL_1 = "http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=EN_PROJ&text=%28"
URL_2="%29&sort=all&querySummary=quick&fieldText=%28MATCH%7BCORDIS%2CWEBPAGESEUROPA%7D%3ASOURCE%29&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&descr="
URL_3 = ";%20Projects"


print "Number of searches: " + str(len(applicants))

# Open CSV file
with open ('output.csv', 'w') as csvfile: 
        csvwriter = csv.writer(open ('output.csv', 'a'))





for applicant in applicants:

    list_url = URL_1 + applicant + URL_2 + applicant + URL_3
    result_links = extract_links(list_url)
    
    
    for link in result_links:
        parse_object(link)