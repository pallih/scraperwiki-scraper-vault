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
    streams = ["2"]
    #options = soup.find("select", {"id":"ctl00_ContentPlaceHolder1_ddlstream"}).findAll("option")
    for stream in streams:
        br.select_form(name='aspnetForm')
        br.form.set_all_readonly(False)
        br['ctl00$ContentPlaceHolder1$ddlstream'] = [stream]
        br.submit()
        soup = BeautifulSoup(br.response().read())
        rounds = ["1","2","3","4","5","6","7"]
        #options = soup.find("select", {"id":"ctl00_ContentPlaceHolder1_ddlround"}).findAll("option")

        for round in rounds:
            br.select_form(name='aspnetForm')
            br.form.set_all_readonly(False)
            br['ctl00$ContentPlaceHolder1$ddlround'] = [round]
            br['ctl00$ContentPlaceHolder1$ddlquota'] = ["AL"]
            br['ctl00$ContentPlaceHolder1$ddlinstitute'] = ["All"]
            br['ctl00$ContentPlaceHolder1$ddlbranch'] = ["All"]
            br.submit()
            soup = BeautifulSoup(br.response().read())
            rows = soup.findAll("tr",  "labeltxt2" )
            print len(rows)
            for row in rows:
                cols = row.findAll("td")
                record = {
                            "round":cols[0].text,
                            "quota":cols[1].text,
                            "institute":cols[2].text,
                            "branch":cols[3].text,
                            "op1":cols[4].text,
                            "op2":cols[5].text,
                            "opph1":cols[6].text,
                            "opph2":cols[7].text,
                            "sc1":cols[8].text,
                            "sc2":cols[9].text,
                            "scph1":cols[10].text,
                            "scph2":cols[11].text,
                            "st1":cols[12].text,
                            "st2":cols[13].text,
                            "stph1":cols[14].text,
                            "stph2":cols[15].text,
                            "ob1":cols[16].text,
                            "ob2":cols[17].text,
                            "obph1":cols[18].text,
                            "obph2":cols[19].text
                            }
                scraperwiki.datastore.save(["round","quota","institute","branch"], record)    

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser,
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------

base_url = 'http://ccb.nic.in/'
starting_url = base_url + 'ccb2011/AieeeCouns/orcr2010/Stream.aspx'
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