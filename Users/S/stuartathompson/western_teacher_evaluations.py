import scraperwiki
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
r = br.open('https://www.ipb.uwo.ca/evaluation/index.php')

html = r.read()

# Select the first (index zero) form
br.select_form(nr=0)

#User credentials
br.form['uwo_id'] = '#3#3'
br.form['uwo_password'] = '#3#3#'

br.submit()

br.response().read() #NECESSARY to enter new page...
#print br.response().read()

br.select_form(nr=0)

br.submit()

br.response().read()
#print br.response().read()

def enterView(allLinks):
    for link in allLinks:
        #print 'enter for link'
        br.follow_link(link)
        br.response().read()

        soup = BeautifulSoup(br.response().read())

        tableProf = soup.find('table').findAll('table')[0] #get the prof's info
        for row in tableProf.findAll('tr')[1:]: #get all the rows but skip the first two
            col = row.findAll({'td'}) #find all cells in this row
            prof = { #this iterates through each cell, assigning each value to the corresponding key
                'instructor_name': col[0].getText(),
                'teaching_faculty': col[1].getText(),
                'teaching_dept': col[2].getText(),
                'subject': col[3].getText(),
                'course_num': col[4].getText(),
                'section': col[5].getText(),
                'year': col[6].getText(),
                'term': col[7].getText(),
                'enrolment': col[8].getText(),
                'responses': col[9].getText(),
                'course_id':col[4].getText() + col[5].getText() + col[6].getText()
            }
            #print prof
            scraperwiki.sqlite.save(unique_keys=['course_id'], data=prof, table_name="profs", verbose=2) #save data
        
        tableEval = soup.find('table').findAll('table')[1] #get the course eval info
        i = 0;
        for row in tableEval.findAll('tr')[15:]: #get all the rows but skip the first 14
            i = i+1
            col = row.findAll({'td'}) #find all cells in this row
            record = { #this iterates through each cell, assigning each value to the corresponding key
                '_db_key':prof['course_num'] + prof['section'] + prof['year'] + '-' + str(i), 
                'question': col[0].getText(),
        #        'number_of_responses': col[1].getText(),
        #        'q1': col[2].getText(),
         #       'q2': col[3].getText(),
          #      'q3': col[4].getText(),
           #     'q4': col[5].getText(),
            #    'q5': col[6].getText(),
             #   'q6': col[7].getText(),
              #  'q7': col[8].getText(),
                'mean': col[9].getText(),
                'standard_deviation': col[10].getText(),
                'median': col[10].getText(),
                'course_id': prof['course_num'] + prof['section'] + prof['year'],
                'instructor_name':prof['instructor_name']
            }
            #print record
            scraperwiki.sqlite.save(unique_keys=['_db_key'], data=record, table_name="evals", verbose=2) #save data

for x in range(1,1117): #1117 (or 1116 total)
    #print x
    allLinks = br.links(text="View")
    nowUrl = br.geturl()
    enterView( allLinks )
    
    br.open(nowUrl)
    br.response().read()
    print br.response().read()

    br.follow_link(text="next")

    br.response().read()



import scraperwiki
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
r = br.open('https://www.ipb.uwo.ca/evaluation/index.php')

html = r.read()

# Select the first (index zero) form
br.select_form(nr=0)

#User credentials
br.form['uwo_id'] = '#3#3'
br.form['uwo_password'] = '#3#3#'

br.submit()

br.response().read() #NECESSARY to enter new page...
#print br.response().read()

br.select_form(nr=0)

br.submit()

br.response().read()
#print br.response().read()

def enterView(allLinks):
    for link in allLinks:
        #print 'enter for link'
        br.follow_link(link)
        br.response().read()

        soup = BeautifulSoup(br.response().read())

        tableProf = soup.find('table').findAll('table')[0] #get the prof's info
        for row in tableProf.findAll('tr')[1:]: #get all the rows but skip the first two
            col = row.findAll({'td'}) #find all cells in this row
            prof = { #this iterates through each cell, assigning each value to the corresponding key
                'instructor_name': col[0].getText(),
                'teaching_faculty': col[1].getText(),
                'teaching_dept': col[2].getText(),
                'subject': col[3].getText(),
                'course_num': col[4].getText(),
                'section': col[5].getText(),
                'year': col[6].getText(),
                'term': col[7].getText(),
                'enrolment': col[8].getText(),
                'responses': col[9].getText(),
                'course_id':col[4].getText() + col[5].getText() + col[6].getText()
            }
            #print prof
            scraperwiki.sqlite.save(unique_keys=['course_id'], data=prof, table_name="profs", verbose=2) #save data
        
        tableEval = soup.find('table').findAll('table')[1] #get the course eval info
        i = 0;
        for row in tableEval.findAll('tr')[15:]: #get all the rows but skip the first 14
            i = i+1
            col = row.findAll({'td'}) #find all cells in this row
            record = { #this iterates through each cell, assigning each value to the corresponding key
                '_db_key':prof['course_num'] + prof['section'] + prof['year'] + '-' + str(i), 
                'question': col[0].getText(),
        #        'number_of_responses': col[1].getText(),
        #        'q1': col[2].getText(),
         #       'q2': col[3].getText(),
          #      'q3': col[4].getText(),
           #     'q4': col[5].getText(),
            #    'q5': col[6].getText(),
             #   'q6': col[7].getText(),
              #  'q7': col[8].getText(),
                'mean': col[9].getText(),
                'standard_deviation': col[10].getText(),
                'median': col[10].getText(),
                'course_id': prof['course_num'] + prof['section'] + prof['year'],
                'instructor_name':prof['instructor_name']
            }
            #print record
            scraperwiki.sqlite.save(unique_keys=['_db_key'], data=record, table_name="evals", verbose=2) #save data

for x in range(1,1117): #1117 (or 1116 total)
    #print x
    allLinks = br.links(text="View")
    nowUrl = br.geturl()
    enterView( allLinks )
    
    br.open(nowUrl)
    br.response().read()
    print br.response().read()

    br.follow_link(text="next")

    br.response().read()



