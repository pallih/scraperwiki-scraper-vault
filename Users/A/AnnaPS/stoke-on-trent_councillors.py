import scraperwiki
import lxml.html

def get_attendance(url, tag):
    a_html = scraperwiki.scrape(url)
    a_root = lxml.html.fromstring(a_html)
    a_table = a_root.cssselect('table.mgStatsTable')[0].cssselect('tr')
    ABSENT_ROW = None
    for i, row in enumerate(a_table):
        if len(row.cssselect('td')) > 0:
            if row.cssselect('td')[0].text_content().strip() == "Absent (incl. apologies):":
                ABSENT_ROW = i
                break 
    attendance = {}
    attendance['Attendance URL' + tag] = url
    attendance['Total expected' + tag] = a_table[1].cssselect('td')[1].text_content()
    attendance['Present' + tag] = int(a_table[2].cssselect('td')[1].text_content().strip())
    attendance['Present percent' + tag] = int(a_table[2].cssselect('td')[2].text_content().strip().replace("%",""))
    attendance['Absent' + tag] = int(a_table[ABSENT_ROW].cssselect('td')[1].text_content().strip())
    attendance['Absent percent' + tag] = int(a_table[ABSENT_ROW].cssselect('td')[2].text_content().strip().replace("%",""))
    return attendance 

def get_councillor(link, name, party, ward):
    print link
    councillor = {}

    # Profile information
    c_html = scraperwiki.scrape(link)
    c_root = lxml.html.fromstring(c_html)
    councillor['Profile URL'] = link
    councillor['Name'] = name
    councillor['Party'] = party
    councillor['Ward'] = ward
    councillor['Image URL'] = BASE_URL + c_root.cssselect('div.mgBigPhoto img')[0].get('src')
    dates = c_root.cssselect('ul.mgNonBulletList')[-1].cssselect('li')[0]
    councillor['First elected'] = dates.text_content().split(' - ')[0]
    attendance_link = c_root.cssselect('ul.mgActionList li a')[2].get('href')
    attendance_url_recent = BASE_URL + attendance_link 
    attendance_url_alltime = BASE_URL + attendance_link + "&XXR=0&DR=01%2f05%2f2003-12%2f04%2f2012&ACT=Go"

    # Attendance information
    # All time: http://www.moderngov.stoke.gov.uk/mgAttendance.aspx?XXR=0&DR=01%2f05%2f2003-12%2f04%2f2012&ACT=Go&UID=2877
    recent_attendance = get_attendance(attendance_url_recent, ' - last 6 months')
    all_time_attendance = get_attendance(attendance_url_alltime, ' - since 1 May 2003')
    
    for elem in recent_attendance:
        councillor[elem] = recent_attendance[elem]
    for elem in all_time_attendance:
        councillor[elem] = all_time_attendance[elem]

    print councillor
    
    scraperwiki.sqlite.save(unique_keys=['Name'], data=councillor)

BASE_URL = 'http://www.moderngov.stoke.gov.uk/'
START_URL = BASE_URL + '/mgMemberIndex.aspx?VW=TABLE&PIC=1&FN='
html = scraperwiki.scrape(START_URL)
root = lxml.html.fromstring(html)
rows = root.cssselect("table#mgTable1 tr")
for i, row in enumerate(rows): 
    tds = row.cssselect('td')
    if len(tds) > 0:
        link = tds[1].cssselect('p a')[0].get('href')
        name = tds[1].cssselect('p a')[0].text_content().replace("Councillor ","")
        party = tds[2].text_content()
        ward = tds[3].text_content()
        get_councillor(BASE_URL + link, name, party, ward)
import scraperwiki
import lxml.html

def get_attendance(url, tag):
    a_html = scraperwiki.scrape(url)
    a_root = lxml.html.fromstring(a_html)
    a_table = a_root.cssselect('table.mgStatsTable')[0].cssselect('tr')
    ABSENT_ROW = None
    for i, row in enumerate(a_table):
        if len(row.cssselect('td')) > 0:
            if row.cssselect('td')[0].text_content().strip() == "Absent (incl. apologies):":
                ABSENT_ROW = i
                break 
    attendance = {}
    attendance['Attendance URL' + tag] = url
    attendance['Total expected' + tag] = a_table[1].cssselect('td')[1].text_content()
    attendance['Present' + tag] = int(a_table[2].cssselect('td')[1].text_content().strip())
    attendance['Present percent' + tag] = int(a_table[2].cssselect('td')[2].text_content().strip().replace("%",""))
    attendance['Absent' + tag] = int(a_table[ABSENT_ROW].cssselect('td')[1].text_content().strip())
    attendance['Absent percent' + tag] = int(a_table[ABSENT_ROW].cssselect('td')[2].text_content().strip().replace("%",""))
    return attendance 

def get_councillor(link, name, party, ward):
    print link
    councillor = {}

    # Profile information
    c_html = scraperwiki.scrape(link)
    c_root = lxml.html.fromstring(c_html)
    councillor['Profile URL'] = link
    councillor['Name'] = name
    councillor['Party'] = party
    councillor['Ward'] = ward
    councillor['Image URL'] = BASE_URL + c_root.cssselect('div.mgBigPhoto img')[0].get('src')
    dates = c_root.cssselect('ul.mgNonBulletList')[-1].cssselect('li')[0]
    councillor['First elected'] = dates.text_content().split(' - ')[0]
    attendance_link = c_root.cssselect('ul.mgActionList li a')[2].get('href')
    attendance_url_recent = BASE_URL + attendance_link 
    attendance_url_alltime = BASE_URL + attendance_link + "&XXR=0&DR=01%2f05%2f2003-12%2f04%2f2012&ACT=Go"

    # Attendance information
    # All time: http://www.moderngov.stoke.gov.uk/mgAttendance.aspx?XXR=0&DR=01%2f05%2f2003-12%2f04%2f2012&ACT=Go&UID=2877
    recent_attendance = get_attendance(attendance_url_recent, ' - last 6 months')
    all_time_attendance = get_attendance(attendance_url_alltime, ' - since 1 May 2003')
    
    for elem in recent_attendance:
        councillor[elem] = recent_attendance[elem]
    for elem in all_time_attendance:
        councillor[elem] = all_time_attendance[elem]

    print councillor
    
    scraperwiki.sqlite.save(unique_keys=['Name'], data=councillor)

BASE_URL = 'http://www.moderngov.stoke.gov.uk/'
START_URL = BASE_URL + '/mgMemberIndex.aspx?VW=TABLE&PIC=1&FN='
html = scraperwiki.scrape(START_URL)
root = lxml.html.fromstring(html)
rows = root.cssselect("table#mgTable1 tr")
for i, row in enumerate(rows): 
    tds = row.cssselect('td')
    if len(tds) > 0:
        link = tds[1].cssselect('p a')[0].get('href')
        name = tds[1].cssselect('p a')[0].text_content().replace("Councillor ","")
        party = tds[2].text_content()
        ward = tds[3].text_content()
        get_councillor(BASE_URL + link, name, party, ward)
