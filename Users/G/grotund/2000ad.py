import scraperwiki
import lxml.html
import pickle
import datetime

def get_month(longmonth):
    if "January" in longmonth:
        return 1;
    elif "February" in longmonth:
        return 2;
    elif "March" in longmonth:
        return 3;
    elif "April" in longmonth:
        return 4;
    elif "May" in longmonth:
        return 5;
    elif "June" in longmonth:
        return 6;
    elif "July" in longmonth:
        return 7;
    elif "August" in longmonth:
        return 8;
    elif "September" in longmonth:
        return 9;
    elif "October" in longmonth:
        return 10;
    elif "November" in longmonth:
        return 11;
    elif "December" in longmonth:
        return 12;
    else:
        return 0;

new_prog  = 1780;
base_url   = 'http://www.2000ad.org/?zone=prog&page=profiles&choice='

for prog in range(1,2):
    html = scraperwiki.scrape(base_url + str(prog))
    root = lxml.html.fromstring(html)
    content = root.cssselect("td[id='content'] td")[1]

##    scraperwiki.sqlite.save_var('timestamp', pickle.dumps(datetime.datetime.now()));
##    print pickle.loads(scraperwiki.sqlite.get_var('timestamp'));
    
    for issue in content.cssselect("h1"):
        issue_num  = issue.text_content()[12:len(issue.text_content())];
        print "Issue #" + issue_num;

    for cover in content.cssselect("h3"):
        cover_longdate = cover.text_content()[12:len(cover.text_content())];
        space_pos = cover_longdate.find(' ');
        comma_pos = cover_longdate.find(',');

        cover_day   = cover_longdate[0:space_pos-2];
        cover_month = get_month(cover_longdate); 
        cover_year  = cover_longdate[comma_pos+2:len(cover_longdate)];
        cover_date  = datetime.date(int(cover_year), cover_month, int(cover_day));
        print(cover_date);

    for issue_details in content.cssselect("td b"):
        if "Reprinted" not in issue_details.text_content():
            print issue_details.text_content();        

#        cover_longdate_sp1   = cover_text.find(' ', longdate);
#        issue_num = issue_text[prog_pos+5:len(issue_text)];
#        print issue_num;

#        for thrill in content.cssselect("h2 a"):
#            print thrill.text_content();

import scraperwiki
import lxml.html
import pickle
import datetime

def get_month(longmonth):
    if "January" in longmonth:
        return 1;
    elif "February" in longmonth:
        return 2;
    elif "March" in longmonth:
        return 3;
    elif "April" in longmonth:
        return 4;
    elif "May" in longmonth:
        return 5;
    elif "June" in longmonth:
        return 6;
    elif "July" in longmonth:
        return 7;
    elif "August" in longmonth:
        return 8;
    elif "September" in longmonth:
        return 9;
    elif "October" in longmonth:
        return 10;
    elif "November" in longmonth:
        return 11;
    elif "December" in longmonth:
        return 12;
    else:
        return 0;

new_prog  = 1780;
base_url   = 'http://www.2000ad.org/?zone=prog&page=profiles&choice='

for prog in range(1,2):
    html = scraperwiki.scrape(base_url + str(prog))
    root = lxml.html.fromstring(html)
    content = root.cssselect("td[id='content'] td")[1]

##    scraperwiki.sqlite.save_var('timestamp', pickle.dumps(datetime.datetime.now()));
##    print pickle.loads(scraperwiki.sqlite.get_var('timestamp'));
    
    for issue in content.cssselect("h1"):
        issue_num  = issue.text_content()[12:len(issue.text_content())];
        print "Issue #" + issue_num;

    for cover in content.cssselect("h3"):
        cover_longdate = cover.text_content()[12:len(cover.text_content())];
        space_pos = cover_longdate.find(' ');
        comma_pos = cover_longdate.find(',');

        cover_day   = cover_longdate[0:space_pos-2];
        cover_month = get_month(cover_longdate); 
        cover_year  = cover_longdate[comma_pos+2:len(cover_longdate)];
        cover_date  = datetime.date(int(cover_year), cover_month, int(cover_day));
        print(cover_date);

    for issue_details in content.cssselect("td b"):
        if "Reprinted" not in issue_details.text_content():
            print issue_details.text_content();        

#        cover_longdate_sp1   = cover_text.find(' ', longdate);
#        issue_num = issue_text[prog_pos+5:len(issue_text)];
#        print issue_num;

#        for thrill in content.cssselect("h2 a"):
#            print thrill.text_content();

