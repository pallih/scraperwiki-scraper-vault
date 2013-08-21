###############################################################################
# START HERE: Tutorial for scraping ASP.NET pages (HTML pages that end .aspx), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on 
# .aspx pages, you're actually submitting a form.
# This tutorial demonstrates scraping a particularly tricky example. 
###############################################################################
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

def bootstrap(soup):
    br.open(base_url + 'default.aspx')
    br.open(base_url + 'defaulthome.aspx')
    current = base_url + 'allotedseat/stream.aspx'
    br.open(base_url + 'allotedseat/stream.aspx')
    soup = BeautifulSoup(br.response().read())
    print soup

    alink = "http://seeuptu.nic.in/allotedseat/strconn_OPCR.aspx?streamcd=10&__EVENTARGUMENT=&__EVENTTARGET=STRMNM&__EVENTVALIDATION=%2FwEWDAKd0MScAgLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BAwLNiZW%2BA1Rj7Q3On1yIicBeWq3K%2Bdv9%2Fx6n&__PREVIOUSPAGE=_A0fAcgbfcl7jZI6MTsl0RhBaMQr9o92tyUw3tPTTk8hKPOJUV8RrKtqY9-_OYa1gsmdZxPLORNdVEiCkEA_Kztd6GVW4KRZuVaH8aoE_w8dfH690&__VIEWSTATE=%2FwEPDwUJNjE0NTgzMzgxZGR3h8JfMHDP635QJ3PCDYpgC6GJeQ%3D%3D"
    br.open(alink)
    soup = BeautifulSoup(br.response().read())
    print soup
    options = soup.find("select", {"id":"DDL_Institute"}).findAll("option")
    for option in options:
        print option["value"]
        br.select_form(name='form1')
        br.form.set_all_readonly(False)
        br['DDL_Institute'] = [option["value"]]
        institute = option.text
        institute_code = option["value"]
        br.submit()
        soup = BeautifulSoup(br.response().read())
        rows = soup.find("table", {"id":"Table1"}).findAll("tr");
        cols = ["","","","","",""]
        for row in rows[1:]:
            index =0
            for col in row.findAll("td"):
                if col.text: cols[index]=col.text
                index=index+1
            print "%s,%s,%s,%s,%s,%s,%s" %(institute_code,institute,cols[0],cols[1],cols[2],cols[3],cols[4])
            record = { 
                        "InstituteCode":institute_code,
                        "InstituteName":institute,
                        "SerialNumber":cols[0],
                        "BranchCourse":cols[1],
                        "AlottedUCAT":cols[2],
                        "OPRank":cols[3],
                        "CLRank":cols[4]
                        }

            scraperwiki.datastore.save(["InstituteCode","BranchCourse","AlottedUCAT"],record)

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser, 
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'http://seeuptu.nic.in/'
starting_url = base_url + 'index.aspx'
br = mechanize.Browser()

# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(starting_url)
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
bootstrap(soup)
