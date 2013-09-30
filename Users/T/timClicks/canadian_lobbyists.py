# General pattern
#   + iterate through index of lobbyists
#     https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/publicBasicSearch;jsessionid=0001L5eSoTn1UkWadD75AaG5z3Y:-2S0FEQ?language=en_CA
#   + save individual lobbyist's info
#   + look into lobbyist
#   + add all comms reports
#     https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/_ls63_ls6f_ls6d_ls6d_ls4c_ls6f_ls67_ls50_ls75_ls62_ls6c_ls69_ls63_ls42_ls61_ls73_ls69_ls63_ls53_ls65_ls61_ls72_ls63_ls68?_ls66_ls72_ls6d_ls70_ls73=true&_ls73_ls65_ls61_ls72_ls63_ls68_ls54_ls79_ls70_ls65=true&_ls63_ls6c_ls69_ls65_ls6e_ls74_ls49_ls64=217887&_ls72_ls65_ls67_ls69_ls73_ls74_ls72_ls61_ls6e_ls74_ls49_ls64=766739&_ls73_ls74_ls61_ls72_ls74_ls44_ls61_ls74_ls65=2011-05-16&_ls65_ls6e_ls64_ls44_ls61_ls74_ls65=&_ls73_ls4d_ls64_ls4b_ls79=1305609378730&_STRTG3=tr
#   + 
from cookielib import CookieJar
import json
import twisted.web
from Queue import LifoQueue
from threading import Thread
import urllib2
from gzip import GzipFile
from StringIO import StringIO
import zlib

from lxml import html
import scraperwiki as SW
from scrapemark import scrape

CJ = CookieJar()
Q = LifoQueue()
start_url="https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/publicBasicSearch"

params = [
("registrationText", ""),
("exactPhraseText", ""),
("oneorMoreWordsText", ""),
("searchTypeAll", "Search"),
("registrationStatus", "STATUS_ACTIVE"),
("registrationType", "")
]

def GET(url):
    req = urllib2.Request(url)
    req.add_header("Accept-Encoding", "gzip, deflate")
    res = urllib2.urlopen(req)
    if res.headers.get("content-encoding") == "gzip":
        data = GzipFile(fileobj=StringIO(res.read()),mode="r")
    elif res.headers.get("content-encoding") == "deflate":
        data = StringIO(deflate(res.read()))
    else:
        data = res.read()
    try:
        encoding = res.headers.get('Content-Type').split("charset=")[1]
    except IndexError:
        encoding = 'ISO-8859-1'
    return data.decode(encoding).encode('utf-8')
    
def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def clean(text):
    return text.replace('\n', ' ').replace('\xa0', ' ').strip()

def norm(label):
    """
    >>> norm('Associated registration:')
    'associated_registration'
    """                                       
    return label.lower().replace(':', '').replace(',', '').replace("'", '').replace(' ', '_')[:100]



def get_departments_from_registration(lobbyist):
    name = lobbyist['name']
    rn = lobbyist['registration_number']
    depts = []
    for dept in lobbyist['federal_departments_or_organizations_which_have_been_or_will_be_communicated_with_during_the_course_of_the_undertaking'].split(','):
        if '(' in dept:
            dept, abbr = dept.split(' (')
            abbr = abbr.strip()[:-1]
        else:
            abbr = None
        depts.append(dict(department_name=dept, department_abbr=abbr, lobbyist_name=name, lobbyist_registration_number=rn))
    SW.sqlite.save(["department_name", "lobbyist_name"], depts, table_name="federal_departments")

def save_client(client):
    SQ.sqlite.save(['client'], data=client, table_name='clients')

def save_lobbyist(lobbyist):
    SQ.sqlite.save(['lobbyist_id'], data=lobbyist, table_name='lobbyists')

def save_official(official):
    SQ.sqlite.save(['name', 'org'], data=official, table_name='officials')

def save_client(client):
    SQ.sqlite.save(['name'], data=client, table_name='clients')

def save_communication_report(report):
    SQ.sqlite.save(['communication_number'], data=report, table_name='communication_reports')

def save_consulting_firm(firm):
    SQ.sqlite.save(['name'], data=firm, table_name='save_consulting_firms')

def save_agency(agency):
    SQ.sqlite.save(['name'], data=agency, table_name='agencies')

def save_topic(topic):
    SQ.sqlite.save(['communications_id', 'topic'], data=topic, table_name='topics')


def comms_report(url):
    report_data = html.parse(url).getroot()
    report = {}
    for row in report_data.cssselect('table')[0].cssselect('tr'):
        report[norm(row[0].text_content().strip())] = row[1].text_content().strip()
        report['lobbyist_id'] = report['associated_registration']
        report['communication_id'] = report['communication_number']
    for row in comms_lxml.cssselect('table')[1].cssselect('tr'):
        label = row[0].text_content()
        if 'Designated' in text:
            fragments = html.tostring(row[1]).split('<br><br>')
            talked_to = [scrape("{* <strong>{{ name }}</strong>{{ role }}<br>{{ org }} *}", html=fragment) for fragment in fragments]
            for official in talked_to:
                official['name'] = official['name'].replace(u'\xa0',' ').strip()
                official['role'] = official['role'].replace(',', '').strip()
                official['org'] = official['org'].strip()
                official['communication_id'] = report['communication_number']
            Q.put((save_official, talked_to))
            report['officials'] = '\n'.join(', '.join([off['name'], off['role'], offl['org']]) for off in talked_to)
            for agency in set([official['org'] for official in talked_to]):
                if '(' in agency:
                    name, abbr = agency.rsplit('(',1)
                    abbr = abbr[:-1]
                else:
                    name = agency.strip()
                    abbr = ''
                Q.put(save_agency, dict(name=name, abbr=abbr))
        elif 'Subject Matter' in label:
            topics = [topic.strip() for topic in row[1].text_content().split(',')]
            report['topics'] = '\n'.join(topics)
        elif 'Responsible Officer' in label:
            report['filer'] = row[1].text_content().strip()
        elif '' == label.strip():
            pass
        else:
            print 'HOLY SMOKES BATMAN a new field that we did not know about', label, row[1].text_content().strip()
            raise ValueError

            
    Q.put((save_report, report))


def comms_report_index(url):
    pattern = """<tr>Date<th></th><th></th><th></th>
</tr>
{*
  <tr>
    <td><a href="[reports].link|abs"></a></td>
    <td></td>
    <td></td>
  </tr>
*}
{* <a href="{{ next|abs }}">Next</a> *}
"""
    res = scrape(pattern, url=url, cookie_jar=CJ)
    try:
        links = res['links']
        for link in links:
            Q.put((comms_report, url))
        next_page_url = res['next']
        if next_page_url:
            Q.put((comms_report_index, next_page_url))
    except TypeError:
        print 'ERROR, having difficulty getting communications reports from', url

def corporation_registration(page):
    pattern = """Corporation:{{ name }}Name change history
Responsible Officer:{{ responsible_officer_name }}
Position Title:    {{ responsible_officer_name }}
Version:{{ registration_id }}
Type:{{ registration_type }}
Active from:{{ registration_active_from_date }}
Activity last confirmed:{{ registration_last_confirmed_date }}

A. Information about Responsible Officer and Corporation
Corporation:{{ corporation_name }}
Telephone number:{{ corporation_phone }}
Fax number:{{ corporation_fax }}
Description of the corporation's business activities: {{ corporation_business_activities }}
 
Parent:{{ parent|html }}
Subsidiary:{{ subsidiary|html }}
Was the corporation funded in whole or in part by any domestic or foreign government institution in the last completed financial year, or does the client expect funding in the current financial year?{{ is_government_funded }}

B. Lobbyists Employed by the Corporation
List of Senior Officers whose lobbying activities represent less than 20% of their Duties
{*
Name:{{ [lobbyists].name }}
Position title:{{ [lobbyists].title }}
Public offices held:{{ [lobbyists].public_offices_held }}
Designated public office holder:{{ [lobbyists].is_public_officer }}Name
*}{*
Name:{{ [lobbyists].name }}
Position title:{{ [lobbyists].title }}
Public offices held:{{ [lobbyists].public_offices_held }}
Designated public office holder:{{ [lobbyists].is_public_officer }}
*}

C. Lobbying Activity Information
Federal departments or organizations which have been or will be communicated with during the course of the undertaking: {{ agencies_talked_to }}
Communication techniques that have been used or are expected to be used in the course of the undertaking: 
{{ lobbying_activities }}
Information about Subject matter:{{ lobbying_subject_matter }}
 
Details Regarding the Identified Subject Matter
"""
    subject_matter_pattern = """Details Regarding the Identified Subject Matter
{* <tr><td>{{ [topics].category }}</td><td>{{ [topics].description }}</td></tr> *} 
"""
    page = GET(url)
    registration = scrape(pattern, html=html.tostring(html.fromstring(page), encoding='utf-8', method='text'))
    registration['lobbyists'] = [l for l in registration['lobbyists'] if len(l['is_public_officer'].split()) == 1]
    registration['topics'] = scrape(subject_matter_pattern, html=page)
    registration['parent'] = registration['parent'].strip()
    registration['parent_name'] = registration['parent'].split('\n')[0]
    registration['subsidiary'] = registration['subsidiary'].strip()
    registration['subsidiary_name'] = registration['subsidiary'].split('\n')[0]
    
    


def registration(url):
    page = GET(url)
    lowered = page.lower()
    if 'consultant lobbyist name' in lowered:
        lobbyist_registration(html.document_fromstring(page))

def lobbyist_registration(page):
    registration = {}
    activities = {}
    client = {}
    lobbyist = {}
    tables = registration_data.cssselect('table')
    for row in tables[1].cssselect('tr'):
        try:
            lobbyist[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            if row[0].text.strip() == '':
                pass
            elif '<th' in html.tostring(row):
                pass
            else:
                print html.tostring(row)
                print row.text_content().strip()
                raise
    try:
        lobbyist['name'] = lobbyist['consultant_lobbyist_name'].split('Lobbyist business address')[0].strip().replace('\xa0', ' ')
        lobbyist['consulting_firm_name'] = lobbyist['consulting_firm'].split('\n')[0].replace('\xa0', ' ')
        lobbyist['consulting_firm_address'] = lobbyist['consulting_firm'].split(lobbyist['consulting_firm_name'])[-1].replace('\xa0', ' ').strip()
        Q.put(save_consulting_firm, dict(name=lobbyist['consulting_firm_name'], address=lobbyist['consulting_firm_address']))
    except KeyError:
        if 'corporation' in lobbyist:
            lobbyist['name'] = lobbyist['corporation']
        else:
            from pprint import pprint
            pprint(lobbyist, indent=4)
            raise

    for row in tables[2].cssselect('tr'):
        try:
            client[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            print row.text_content().strip()
    client['name'] = client['client'].split('\n')[0].strip()
    client['address'] = client['client'].split('\n')[1].strip()
    del client['client']
    client['telephone_number'] = clean(client['telephone_number'])
    client['principal_representative_of_the_client'] = clean(client['principal_representative_of_the_client'])
    client['parent_text'] = client['parent']
    if client['parent'] == 'The client is not a subsidiary of any other parent companies.':
        client['parent'] = None
    client['subsidiary_text'] = client['subsidiary']
    if client['subsidiary'] == 'The client does not have any subsidiaries that could be affected by the outcome of the undertaking.':
        client['subsidiary'] = None
    client['control_or_direction_from_others_text'] = client['person_or_organization']
    if client['person_or_organization'] == "The client's activities are not controlled or directed by another person or organization with a direct interest in the outcome of this undertaking.":
        client['control_or_direction_from_other'] = False
    del client['person_or_organization']
    client['government_funded'] = client['was_the_client_funded_in_whole_or_in_part_by_any_domestic_or_foreign_government_institution_in_the_l']
    if 'N' in client['overnment_funded'].upper():
        client['overnment_funded'] = False
    else:
        client['overnment_funded'] = True
    del client['was_the_client_funded_in_whole_or_in_part_by_any_domestic_or_foreign_government_institution_in_the_l']
    Q.put(save_client, client)

    for row in tables[3].cssselect('tr'):
        try:
            activities[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            pass
    
    activities['agencies_communicated_with'] = activities['federal_departments_or_organizations_which_have_been_or_will_be_communicated_with_during_the_course_']
    agencies = []
    for agency in activities['agencies_communicated_with'].split(','):
        agency=agency.strip()
        agencies.append(agency)
        if '(' in agency:
            name, abbr = agency.rsplit('(',1)
            abbr = abbr[:-1]
        else:
            name = agency.strip()
            abbr = ''
        Q.put(save_agency, dict(name=name, abbr=abbr))
    activities['agencies_communicated_with'] = ', '.join(agencies)
    activities['methods'] = activities['communication_techniques_that_have_been_used_or_are_expected_to_be_used_in_the_course_of_the_underta']
    activities['methods'] = ', '.join(m.strip() for m in activities['methods'].split(','))
    for method in activities['methods'].split(', '):
        Q.add(save_method, dict(method=method, lobbyist=lobbyist['name'], client=client['name']))
    if 'Y' in activities['i_arranged_or_expect_to_arrange_one_or_more_meetings_on_behalf_of_my_client_between_a_public_office_'].upper():
        activities['meetings_arranged'] = True
    else:
        activities['meetings_arranged'] = False
    
    del activities['categories']
    del activities['communication_techniques_that_have_been_used_or_are_expected_to_be_used_in_the_course_of_the_underta']
    del activities['i_arranged_or_expect_to_arrange_one_or_more_meetings_on_behalf_of_my_client_between_a_public_office_']
    Q.put(save_registration, dict(client_name=client['name'], lobbyist_name=lobbyist['name'], data=json.dumps(dict(activities=activities, agencies=agencies, client=client, lobbyist=lobbyist))))


def parse_search_results(url, first=False):
    pattern = """{*
<td>{{ [lobbyists]].type }}:<strong>{{ [lobbyists]].name }}</strong>

{{ [lobbyists].lobbyist_details|html }}<a href="{{ [lobbyists].communication_reports_link|abs }}">View communication reports</a>
</td>
          <td class="tableTop">          
            <a href="{{ [lobbyists].registration_link|abs }}>
              {{ [lobbyists].registration_begining }}to{{ [lobbyists].registration_ending }}
            </a>
          </td>
*}

{* <a href="{{ next|abs }}">Next</a> *}
"""
    if first:
        res = scrape(pattern=pattern, url=url, post=params, cookie_jar=CJ)
    else:
        res = scrape(pattern=pattern, url=url, cookie_jar=CJ)
    print res
    lobbyists = res['lobbyists']
    next_page_url = res['next']
    print next_page_url
    for lobbyist in lobbyists:        
        details = html.fromstring(lobbyist['lobbyist_details'])
        if lobbyist['type'] == u'Consultant':
            lobbyist['consulting_firm'] = details[1].text
            lobbyist['client'] = details[3].text
            lobbyist['lobbyist_id'] = details[4].tail.strip()
        elif lobbyist['type'] == u'In-house Organization' or lobbyist['type'] == u'In-house Corporation':
            lobbyist['responsible_officer'] = ' '.join(part.strip() for part in details[1].text.split())
            lobbyist['lobbyist_id'] = details[2].tail.strip()
        else:
            print 'CRAZINESS: new type found: ', lobbyist['type'], 
            print lobbyist
            raise ValueError
        del lobbyist['lobbyist_details']
        Q.put((comms_report_index, lobbyist['communication_reports_link']))
        Q.put((registration, lobbyist['registration_link']))

    #if next_page_url:
    #    Q.put((parse_search_results, next_page_url))

def main(queue, threaded):
    queue.put((parse_search_results, start_url, True))
    
    if threaded:
        def worker():
            while True:
                job = Q.get()
                try:
                    apply(job[0], job[1:])
                except Exception as e:
                    print 'EXCEPTION', job, e
                    raise 
                Q.task_done()
    
        for i in xrange(3):
             t = Thread(target=worker)
             #t.daemon = True
             t.start()
    
        queue.join()
    else:
        while 1:
            try:
                job = queue.get()
            except Queue.Empty:
                break
            print job
            apply(job[0], job[1:])



main(queue=Q, threaded=False)# General pattern
#   + iterate through index of lobbyists
#     https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/publicBasicSearch;jsessionid=0001L5eSoTn1UkWadD75AaG5z3Y:-2S0FEQ?language=en_CA
#   + save individual lobbyist's info
#   + look into lobbyist
#   + add all comms reports
#     https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/_ls63_ls6f_ls6d_ls6d_ls4c_ls6f_ls67_ls50_ls75_ls62_ls6c_ls69_ls63_ls42_ls61_ls73_ls69_ls63_ls53_ls65_ls61_ls72_ls63_ls68?_ls66_ls72_ls6d_ls70_ls73=true&_ls73_ls65_ls61_ls72_ls63_ls68_ls54_ls79_ls70_ls65=true&_ls63_ls6c_ls69_ls65_ls6e_ls74_ls49_ls64=217887&_ls72_ls65_ls67_ls69_ls73_ls74_ls72_ls61_ls6e_ls74_ls49_ls64=766739&_ls73_ls74_ls61_ls72_ls74_ls44_ls61_ls74_ls65=2011-05-16&_ls65_ls6e_ls64_ls44_ls61_ls74_ls65=&_ls73_ls4d_ls64_ls4b_ls79=1305609378730&_STRTG3=tr
#   + 
from cookielib import CookieJar
import json
import twisted.web
from Queue import LifoQueue
from threading import Thread
import urllib2
from gzip import GzipFile
from StringIO import StringIO
import zlib

from lxml import html
import scraperwiki as SW
from scrapemark import scrape

CJ = CookieJar()
Q = LifoQueue()
start_url="https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/publicBasicSearch"

params = [
("registrationText", ""),
("exactPhraseText", ""),
("oneorMoreWordsText", ""),
("searchTypeAll", "Search"),
("registrationStatus", "STATUS_ACTIVE"),
("registrationType", "")
]

def GET(url):
    req = urllib2.Request(url)
    req.add_header("Accept-Encoding", "gzip, deflate")
    res = urllib2.urlopen(req)
    if res.headers.get("content-encoding") == "gzip":
        data = GzipFile(fileobj=StringIO(res.read()),mode="r")
    elif res.headers.get("content-encoding") == "deflate":
        data = StringIO(deflate(res.read()))
    else:
        data = res.read()
    try:
        encoding = res.headers.get('Content-Type').split("charset=")[1]
    except IndexError:
        encoding = 'ISO-8859-1'
    return data.decode(encoding).encode('utf-8')
    
def deflate(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def clean(text):
    return text.replace('\n', ' ').replace('\xa0', ' ').strip()

def norm(label):
    """
    >>> norm('Associated registration:')
    'associated_registration'
    """                                       
    return label.lower().replace(':', '').replace(',', '').replace("'", '').replace(' ', '_')[:100]



def get_departments_from_registration(lobbyist):
    name = lobbyist['name']
    rn = lobbyist['registration_number']
    depts = []
    for dept in lobbyist['federal_departments_or_organizations_which_have_been_or_will_be_communicated_with_during_the_course_of_the_undertaking'].split(','):
        if '(' in dept:
            dept, abbr = dept.split(' (')
            abbr = abbr.strip()[:-1]
        else:
            abbr = None
        depts.append(dict(department_name=dept, department_abbr=abbr, lobbyist_name=name, lobbyist_registration_number=rn))
    SW.sqlite.save(["department_name", "lobbyist_name"], depts, table_name="federal_departments")

def save_client(client):
    SQ.sqlite.save(['client'], data=client, table_name='clients')

def save_lobbyist(lobbyist):
    SQ.sqlite.save(['lobbyist_id'], data=lobbyist, table_name='lobbyists')

def save_official(official):
    SQ.sqlite.save(['name', 'org'], data=official, table_name='officials')

def save_client(client):
    SQ.sqlite.save(['name'], data=client, table_name='clients')

def save_communication_report(report):
    SQ.sqlite.save(['communication_number'], data=report, table_name='communication_reports')

def save_consulting_firm(firm):
    SQ.sqlite.save(['name'], data=firm, table_name='save_consulting_firms')

def save_agency(agency):
    SQ.sqlite.save(['name'], data=agency, table_name='agencies')

def save_topic(topic):
    SQ.sqlite.save(['communications_id', 'topic'], data=topic, table_name='topics')


def comms_report(url):
    report_data = html.parse(url).getroot()
    report = {}
    for row in report_data.cssselect('table')[0].cssselect('tr'):
        report[norm(row[0].text_content().strip())] = row[1].text_content().strip()
        report['lobbyist_id'] = report['associated_registration']
        report['communication_id'] = report['communication_number']
    for row in comms_lxml.cssselect('table')[1].cssselect('tr'):
        label = row[0].text_content()
        if 'Designated' in text:
            fragments = html.tostring(row[1]).split('<br><br>')
            talked_to = [scrape("{* <strong>{{ name }}</strong>{{ role }}<br>{{ org }} *}", html=fragment) for fragment in fragments]
            for official in talked_to:
                official['name'] = official['name'].replace(u'\xa0',' ').strip()
                official['role'] = official['role'].replace(',', '').strip()
                official['org'] = official['org'].strip()
                official['communication_id'] = report['communication_number']
            Q.put((save_official, talked_to))
            report['officials'] = '\n'.join(', '.join([off['name'], off['role'], offl['org']]) for off in talked_to)
            for agency in set([official['org'] for official in talked_to]):
                if '(' in agency:
                    name, abbr = agency.rsplit('(',1)
                    abbr = abbr[:-1]
                else:
                    name = agency.strip()
                    abbr = ''
                Q.put(save_agency, dict(name=name, abbr=abbr))
        elif 'Subject Matter' in label:
            topics = [topic.strip() for topic in row[1].text_content().split(',')]
            report['topics'] = '\n'.join(topics)
        elif 'Responsible Officer' in label:
            report['filer'] = row[1].text_content().strip()
        elif '' == label.strip():
            pass
        else:
            print 'HOLY SMOKES BATMAN a new field that we did not know about', label, row[1].text_content().strip()
            raise ValueError

            
    Q.put((save_report, report))


def comms_report_index(url):
    pattern = """<tr>Date<th></th><th></th><th></th>
</tr>
{*
  <tr>
    <td><a href="[reports].link|abs"></a></td>
    <td></td>
    <td></td>
  </tr>
*}
{* <a href="{{ next|abs }}">Next</a> *}
"""
    res = scrape(pattern, url=url, cookie_jar=CJ)
    try:
        links = res['links']
        for link in links:
            Q.put((comms_report, url))
        next_page_url = res['next']
        if next_page_url:
            Q.put((comms_report_index, next_page_url))
    except TypeError:
        print 'ERROR, having difficulty getting communications reports from', url

def corporation_registration(page):
    pattern = """Corporation:{{ name }}Name change history
Responsible Officer:{{ responsible_officer_name }}
Position Title:    {{ responsible_officer_name }}
Version:{{ registration_id }}
Type:{{ registration_type }}
Active from:{{ registration_active_from_date }}
Activity last confirmed:{{ registration_last_confirmed_date }}

A. Information about Responsible Officer and Corporation
Corporation:{{ corporation_name }}
Telephone number:{{ corporation_phone }}
Fax number:{{ corporation_fax }}
Description of the corporation's business activities: {{ corporation_business_activities }}
 
Parent:{{ parent|html }}
Subsidiary:{{ subsidiary|html }}
Was the corporation funded in whole or in part by any domestic or foreign government institution in the last completed financial year, or does the client expect funding in the current financial year?{{ is_government_funded }}

B. Lobbyists Employed by the Corporation
List of Senior Officers whose lobbying activities represent less than 20% of their Duties
{*
Name:{{ [lobbyists].name }}
Position title:{{ [lobbyists].title }}
Public offices held:{{ [lobbyists].public_offices_held }}
Designated public office holder:{{ [lobbyists].is_public_officer }}Name
*}{*
Name:{{ [lobbyists].name }}
Position title:{{ [lobbyists].title }}
Public offices held:{{ [lobbyists].public_offices_held }}
Designated public office holder:{{ [lobbyists].is_public_officer }}
*}

C. Lobbying Activity Information
Federal departments or organizations which have been or will be communicated with during the course of the undertaking: {{ agencies_talked_to }}
Communication techniques that have been used or are expected to be used in the course of the undertaking: 
{{ lobbying_activities }}
Information about Subject matter:{{ lobbying_subject_matter }}
 
Details Regarding the Identified Subject Matter
"""
    subject_matter_pattern = """Details Regarding the Identified Subject Matter
{* <tr><td>{{ [topics].category }}</td><td>{{ [topics].description }}</td></tr> *} 
"""
    page = GET(url)
    registration = scrape(pattern, html=html.tostring(html.fromstring(page), encoding='utf-8', method='text'))
    registration['lobbyists'] = [l for l in registration['lobbyists'] if len(l['is_public_officer'].split()) == 1]
    registration['topics'] = scrape(subject_matter_pattern, html=page)
    registration['parent'] = registration['parent'].strip()
    registration['parent_name'] = registration['parent'].split('\n')[0]
    registration['subsidiary'] = registration['subsidiary'].strip()
    registration['subsidiary_name'] = registration['subsidiary'].split('\n')[0]
    
    


def registration(url):
    page = GET(url)
    lowered = page.lower()
    if 'consultant lobbyist name' in lowered:
        lobbyist_registration(html.document_fromstring(page))

def lobbyist_registration(page):
    registration = {}
    activities = {}
    client = {}
    lobbyist = {}
    tables = registration_data.cssselect('table')
    for row in tables[1].cssselect('tr'):
        try:
            lobbyist[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            if row[0].text.strip() == '':
                pass
            elif '<th' in html.tostring(row):
                pass
            else:
                print html.tostring(row)
                print row.text_content().strip()
                raise
    try:
        lobbyist['name'] = lobbyist['consultant_lobbyist_name'].split('Lobbyist business address')[0].strip().replace('\xa0', ' ')
        lobbyist['consulting_firm_name'] = lobbyist['consulting_firm'].split('\n')[0].replace('\xa0', ' ')
        lobbyist['consulting_firm_address'] = lobbyist['consulting_firm'].split(lobbyist['consulting_firm_name'])[-1].replace('\xa0', ' ').strip()
        Q.put(save_consulting_firm, dict(name=lobbyist['consulting_firm_name'], address=lobbyist['consulting_firm_address']))
    except KeyError:
        if 'corporation' in lobbyist:
            lobbyist['name'] = lobbyist['corporation']
        else:
            from pprint import pprint
            pprint(lobbyist, indent=4)
            raise

    for row in tables[2].cssselect('tr'):
        try:
            client[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            print row.text_content().strip()
    client['name'] = client['client'].split('\n')[0].strip()
    client['address'] = client['client'].split('\n')[1].strip()
    del client['client']
    client['telephone_number'] = clean(client['telephone_number'])
    client['principal_representative_of_the_client'] = clean(client['principal_representative_of_the_client'])
    client['parent_text'] = client['parent']
    if client['parent'] == 'The client is not a subsidiary of any other parent companies.':
        client['parent'] = None
    client['subsidiary_text'] = client['subsidiary']
    if client['subsidiary'] == 'The client does not have any subsidiaries that could be affected by the outcome of the undertaking.':
        client['subsidiary'] = None
    client['control_or_direction_from_others_text'] = client['person_or_organization']
    if client['person_or_organization'] == "The client's activities are not controlled or directed by another person or organization with a direct interest in the outcome of this undertaking.":
        client['control_or_direction_from_other'] = False
    del client['person_or_organization']
    client['government_funded'] = client['was_the_client_funded_in_whole_or_in_part_by_any_domestic_or_foreign_government_institution_in_the_l']
    if 'N' in client['overnment_funded'].upper():
        client['overnment_funded'] = False
    else:
        client['overnment_funded'] = True
    del client['was_the_client_funded_in_whole_or_in_part_by_any_domestic_or_foreign_government_institution_in_the_l']
    Q.put(save_client, client)

    for row in tables[3].cssselect('tr'):
        try:
            activities[norm(row[0].text_content().strip())]= row[1].text_content().strip()
        except IndexError:
            pass
    
    activities['agencies_communicated_with'] = activities['federal_departments_or_organizations_which_have_been_or_will_be_communicated_with_during_the_course_']
    agencies = []
    for agency in activities['agencies_communicated_with'].split(','):
        agency=agency.strip()
        agencies.append(agency)
        if '(' in agency:
            name, abbr = agency.rsplit('(',1)
            abbr = abbr[:-1]
        else:
            name = agency.strip()
            abbr = ''
        Q.put(save_agency, dict(name=name, abbr=abbr))
    activities['agencies_communicated_with'] = ', '.join(agencies)
    activities['methods'] = activities['communication_techniques_that_have_been_used_or_are_expected_to_be_used_in_the_course_of_the_underta']
    activities['methods'] = ', '.join(m.strip() for m in activities['methods'].split(','))
    for method in activities['methods'].split(', '):
        Q.add(save_method, dict(method=method, lobbyist=lobbyist['name'], client=client['name']))
    if 'Y' in activities['i_arranged_or_expect_to_arrange_one_or_more_meetings_on_behalf_of_my_client_between_a_public_office_'].upper():
        activities['meetings_arranged'] = True
    else:
        activities['meetings_arranged'] = False
    
    del activities['categories']
    del activities['communication_techniques_that_have_been_used_or_are_expected_to_be_used_in_the_course_of_the_underta']
    del activities['i_arranged_or_expect_to_arrange_one_or_more_meetings_on_behalf_of_my_client_between_a_public_office_']
    Q.put(save_registration, dict(client_name=client['name'], lobbyist_name=lobbyist['name'], data=json.dumps(dict(activities=activities, agencies=agencies, client=client, lobbyist=lobbyist))))


def parse_search_results(url, first=False):
    pattern = """{*
<td>{{ [lobbyists]].type }}:<strong>{{ [lobbyists]].name }}</strong>

{{ [lobbyists].lobbyist_details|html }}<a href="{{ [lobbyists].communication_reports_link|abs }}">View communication reports</a>
</td>
          <td class="tableTop">          
            <a href="{{ [lobbyists].registration_link|abs }}>
              {{ [lobbyists].registration_begining }}to{{ [lobbyists].registration_ending }}
            </a>
          </td>
*}

{* <a href="{{ next|abs }}">Next</a> *}
"""
    if first:
        res = scrape(pattern=pattern, url=url, post=params, cookie_jar=CJ)
    else:
        res = scrape(pattern=pattern, url=url, cookie_jar=CJ)
    print res
    lobbyists = res['lobbyists']
    next_page_url = res['next']
    print next_page_url
    for lobbyist in lobbyists:        
        details = html.fromstring(lobbyist['lobbyist_details'])
        if lobbyist['type'] == u'Consultant':
            lobbyist['consulting_firm'] = details[1].text
            lobbyist['client'] = details[3].text
            lobbyist['lobbyist_id'] = details[4].tail.strip()
        elif lobbyist['type'] == u'In-house Organization' or lobbyist['type'] == u'In-house Corporation':
            lobbyist['responsible_officer'] = ' '.join(part.strip() for part in details[1].text.split())
            lobbyist['lobbyist_id'] = details[2].tail.strip()
        else:
            print 'CRAZINESS: new type found: ', lobbyist['type'], 
            print lobbyist
            raise ValueError
        del lobbyist['lobbyist_details']
        Q.put((comms_report_index, lobbyist['communication_reports_link']))
        Q.put((registration, lobbyist['registration_link']))

    #if next_page_url:
    #    Q.put((parse_search_results, next_page_url))

def main(queue, threaded):
    queue.put((parse_search_results, start_url, True))
    
    if threaded:
        def worker():
            while True:
                job = Q.get()
                try:
                    apply(job[0], job[1:])
                except Exception as e:
                    print 'EXCEPTION', job, e
                    raise 
                Q.task_done()
    
        for i in xrange(3):
             t = Thread(target=worker)
             #t.daemon = True
             t.start()
    
        queue.join()
    else:
        while 1:
            try:
                job = queue.get()
            except Queue.Empty:
                break
            print job
            apply(job[0], job[1:])



main(queue=Q, threaded=False)