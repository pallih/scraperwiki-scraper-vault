from urlparse import urlparse, parse_qs
from datetime import datetime
from lxml.html import parse
import scraperwiki

project = 'zen'
baseurl = 'http://drupal.org/project/issues/' + project + '?text=&status=All&priorities=All&categories=All&version=All&component=All'

firstpage = parse(baseurl).getroot()

urls = [baseurl]
queue = []

pager = firstpage.cssselect('.view-id-project_issue_project .pager-last a')

if pager:
    lastpage = pager[0].get('href')
    totalpages = int(parse_qs(urlparse(lastpage).query)['page'][0])
    urls.extend([baseurl + '&page='+ str(i) for i in range(1,totalpages)])

for url in urls:
    doc = parse(url).getroot()
    for issueref in doc.cssselect('.view-id-project_issue_project tbody tr'):

        link = issueref.cssselect('.views-field-title a')[0]
        id = link.get('href').strip('/node/')
        title = link.text_content()

        status = issueref.cssselect('.views-field-sid')[0].text_content().strip()
        category = issueref.cssselect('.views-field-category')[0].text_content().strip()

        issueurl = 'http://drupal.org/node/' + id
        print issueurl
        issuepage = parse(issueurl).getroot()
        
        createdstring = issuepage.cssselect('.node .submitted em')[0].text_content().strip()
        created = datetime.strptime(createdstring, "%B %d, %Y at %I:%M%p").isoformat()

        author = issuepage.cssselect('.node .submitted a')[0]
        authorname = author.text_content().strip()
        authorid = author.get('href').strip('/user/')

        issue = {"id":id, "title":title, "status":status, "category":category, "created": created}
        queue.append(issue)

scraperwiki.sqlite.save(unique_keys=["id"], data=queue)
