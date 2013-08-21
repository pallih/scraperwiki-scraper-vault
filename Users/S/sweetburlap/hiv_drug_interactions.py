import scraperwiki
import lxml.html
import urllib2

# http://www.hiv-druginteractions.org/InteractionDetail.aspx?CombinationId=13568

baseurl = "http://www.hiv-druginteractions.org/InteractionDetail.aspx?CombinationId="

for i in range (15000):

    data = {}
    combinationId = i

    sourceUrl = baseurl + str(combinationId)

    page = urllib2.urlopen(sourceUrl)

    if page.geturl() == sourceUrl: #ie. we haven't been redirected

        data = {}
        data["combinationId"] = combinationId

        data["sourceUrl"] = sourceUrl


        html = lxml.html.parse(page).getroot()



        data["drugClass"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblClass").text
        data["drugName"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblDrugName").text
        data["HIVDrugName"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblHIVDrugName").text
        data["warning"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblIntearctionName").text
        data["evidence"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblGradeName").text
        data["summary"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblSummary").text
        descriptionElement = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_lblTitle")
        data["description"] = descriptionElement.text
        try:
            data["reference"] = descriptionElement[1].text #This could be vulnerabel if there were many references, or none
        except: 
            pass
        data["HIVDrugURL"] = html.get_element_by_id("ctl00_ContentPlaceHolder1_FormView1_hypInteractionsList").get("href")

        scraperwiki.sqlite.save(unique_keys=["combinationId"], data=data)

    else:
        pass
