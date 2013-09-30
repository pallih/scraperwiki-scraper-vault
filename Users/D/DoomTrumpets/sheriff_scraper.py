import scraperwiki
import lxml.html
import urllib2

ymd = "2012-04-17" 

html1 = urllib2.urlopen("http://report.boonecountymo.org/mrcjava/servlet/SH02_MP.I00080s?rls_RUNDATE=EQ&val_RUNDATE=" + str(ymd))
html = html1.read()
root = lxml.html.fromstring(html)

mugshot = []
name = []
addressstreet = []
addresscity = []
birthdate = []
gender = []
arrestdate = []
arrestingagency = []
bailamount = []
releasereason = []
chargenumber = []
chargename = []
warrant = []
casenum = []
disposition = []

namefiller = "PREVIOUS NAME"
streetfiller = "PREVIOUS STREET"
cityfiller = "PREVIOUS CITY"
genderfiller = "PREVIOUS GENDER"
birthdatefiller = "PREVIOUS BIRTHDATE"

pos = 0
tab = [3,5,7,9,11,13,15,17,19,21]
key = 1

for table_row in tab:
    for counter in root.xpath("/html/body/table/tbody/tr/td/div[2]/form/table/tbody/tr/td/table[2]/tbody/tr[" + str(table_row) + "]"):
        mugshot_ele = counter.xpath("td[1]")
        name_ele = counter.xpath("td[2]/strong")
        street_ele = counter.xpath("td[2]/table/tbody/tr[1]/td[2]")
        city_ele= counter.xpath("td[2]/table/tbody/tr[1]/td[2]/br")
        birth_ele = counter.xpath("td[2]/table/tbody/tr[2]/td[2]")
        gender_ele = counter.xpath("td[2]/table/tbody/tr[3]/td[2]")
        arrestdate_ele = counter.xpath("td[4]/table/tbody/tr[1]/td[2]")
        arrestingagency_ele = counter.xpath("td[4]/table/tbody/tr[2]/td[2]")
        bail_ele = counter.xpath("td[4]/table/tbody/tr[3]/td[2]")
        releasereason_ele = counter.xpath("td[4]/table/tbody/tr[4]/td[2]")
        chargenumber_ele = counter.xpath("td[5]")
        chargename_ele = counter.xpath("td[5]/br")
        warrant_ele = counter.xpath("td[6]")
        casenum_ele = counter.xpath("td[7]")
        disposition_ele = counter.xpath("td[8]")
          
        if name_ele == []:
            name.insert(pos, namefiller)
            addressstreet.insert(pos, streetfiller)
            addresscity.insert(pos, cityfiller)
            birthdate.insert(pos, birthdatefiller)
            gender.insert(pos, genderfiller)
            arrestdate.insert(pos, arrestdate_ele[0].text)
            arrestingagency.insert(pos, arrestingagency_ele[0].text)
            bailamount.insert(pos, bail_ele[0].text)
            releasereason.insert(pos, releasereason_ele[0].text)
            chargenumber.insert(pos, chargenumber_ele[0].text)
            chargename.insert(pos, chargename_ele[0].tail)
            warrant.insert(pos, warrant_ele[0].text)
            casenum.insert(pos, casenum_ele[0].text)
            disposition.insert(pos, disposition_ele[0].text)
        else:
            name.insert(pos, name_ele[0].text_content())
            addressstreet.insert(pos, street_ele[0].text)
            addresscity.insert(pos, city_ele[0].tail)
            birthdate.insert(pos, birth_ele[0].text)
            gender.insert(pos, gender_ele[0].text)
            arrestdate.insert(pos, arrestdate_ele[0].text)
            arrestingagency.insert(pos, arrestingagency_ele[0].text)
            bailamount.insert(pos, bail_ele[0].text)
            releasereason.insert(pos, releasereason_ele[0].text)
            chargenumber.insert(pos, chargenumber_ele[0].text)
            chargename.insert(pos, chargename_ele[0].tail)
            warrant.insert(pos, warrant_ele[0].text)
            casenum.insert(pos, casenum_ele[0].text)
            disposition.insert(pos, disposition_ele[0].text)

    scraperwiki.sqlite.save(unique_keys=["index"], data={"index":key, "Name":name[0], "Street Address":addressstreet[0], "City":addresscity[0], "Birthdate":birthdate[0], "Gender":gender[0], "Arrest Date":arrestdate[0], "Arresting Agency":arrestingagency[0], "Bail Amount":bailamount[0], "Release Reason":releasereason[0], "Charge Number":chargenumber[0], "Charge Name":chargename[0], "Warrant":warrant[0], "Case Number":casenum[0], "Disposition Comment":disposition[0]})
    key = key + 1
    if key == 10:
        print scraperwiki.sqlite.execute("select * from swdata")

import scraperwiki
import lxml.html
import urllib2

ymd = "2012-04-17" 

html1 = urllib2.urlopen("http://report.boonecountymo.org/mrcjava/servlet/SH02_MP.I00080s?rls_RUNDATE=EQ&val_RUNDATE=" + str(ymd))
html = html1.read()
root = lxml.html.fromstring(html)

mugshot = []
name = []
addressstreet = []
addresscity = []
birthdate = []
gender = []
arrestdate = []
arrestingagency = []
bailamount = []
releasereason = []
chargenumber = []
chargename = []
warrant = []
casenum = []
disposition = []

namefiller = "PREVIOUS NAME"
streetfiller = "PREVIOUS STREET"
cityfiller = "PREVIOUS CITY"
genderfiller = "PREVIOUS GENDER"
birthdatefiller = "PREVIOUS BIRTHDATE"

pos = 0
tab = [3,5,7,9,11,13,15,17,19,21]
key = 1

for table_row in tab:
    for counter in root.xpath("/html/body/table/tbody/tr/td/div[2]/form/table/tbody/tr/td/table[2]/tbody/tr[" + str(table_row) + "]"):
        mugshot_ele = counter.xpath("td[1]")
        name_ele = counter.xpath("td[2]/strong")
        street_ele = counter.xpath("td[2]/table/tbody/tr[1]/td[2]")
        city_ele= counter.xpath("td[2]/table/tbody/tr[1]/td[2]/br")
        birth_ele = counter.xpath("td[2]/table/tbody/tr[2]/td[2]")
        gender_ele = counter.xpath("td[2]/table/tbody/tr[3]/td[2]")
        arrestdate_ele = counter.xpath("td[4]/table/tbody/tr[1]/td[2]")
        arrestingagency_ele = counter.xpath("td[4]/table/tbody/tr[2]/td[2]")
        bail_ele = counter.xpath("td[4]/table/tbody/tr[3]/td[2]")
        releasereason_ele = counter.xpath("td[4]/table/tbody/tr[4]/td[2]")
        chargenumber_ele = counter.xpath("td[5]")
        chargename_ele = counter.xpath("td[5]/br")
        warrant_ele = counter.xpath("td[6]")
        casenum_ele = counter.xpath("td[7]")
        disposition_ele = counter.xpath("td[8]")
          
        if name_ele == []:
            name.insert(pos, namefiller)
            addressstreet.insert(pos, streetfiller)
            addresscity.insert(pos, cityfiller)
            birthdate.insert(pos, birthdatefiller)
            gender.insert(pos, genderfiller)
            arrestdate.insert(pos, arrestdate_ele[0].text)
            arrestingagency.insert(pos, arrestingagency_ele[0].text)
            bailamount.insert(pos, bail_ele[0].text)
            releasereason.insert(pos, releasereason_ele[0].text)
            chargenumber.insert(pos, chargenumber_ele[0].text)
            chargename.insert(pos, chargename_ele[0].tail)
            warrant.insert(pos, warrant_ele[0].text)
            casenum.insert(pos, casenum_ele[0].text)
            disposition.insert(pos, disposition_ele[0].text)
        else:
            name.insert(pos, name_ele[0].text_content())
            addressstreet.insert(pos, street_ele[0].text)
            addresscity.insert(pos, city_ele[0].tail)
            birthdate.insert(pos, birth_ele[0].text)
            gender.insert(pos, gender_ele[0].text)
            arrestdate.insert(pos, arrestdate_ele[0].text)
            arrestingagency.insert(pos, arrestingagency_ele[0].text)
            bailamount.insert(pos, bail_ele[0].text)
            releasereason.insert(pos, releasereason_ele[0].text)
            chargenumber.insert(pos, chargenumber_ele[0].text)
            chargename.insert(pos, chargename_ele[0].tail)
            warrant.insert(pos, warrant_ele[0].text)
            casenum.insert(pos, casenum_ele[0].text)
            disposition.insert(pos, disposition_ele[0].text)

    scraperwiki.sqlite.save(unique_keys=["index"], data={"index":key, "Name":name[0], "Street Address":addressstreet[0], "City":addresscity[0], "Birthdate":birthdate[0], "Gender":gender[0], "Arrest Date":arrestdate[0], "Arresting Agency":arrestingagency[0], "Bail Amount":bailamount[0], "Release Reason":releasereason[0], "Charge Number":chargenumber[0], "Charge Name":chargename[0], "Warrant":warrant[0], "Case Number":casenum[0], "Disposition Comment":disposition[0]})
    key = key + 1
    if key == 10:
        print scraperwiki.sqlite.execute("select * from swdata")

