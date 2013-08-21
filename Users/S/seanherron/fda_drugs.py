import mechanize
import cookielib
import lxml.html
import re
import string
import scraperwiki
import json

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# We'll define the parameters of each JSON object

keys = {"Drug Name": "drug_name", "Active Ingredient" : "active_ingredient", "Strength(s) Available" : "forms_and_strengths_available", "FDA Application" : "fda_application", "Company" : "company", "Chemical Type" : "chemical_type", "Review Classification" : "review_classification", "Approval Date" : "approval_date", "Strength" : "strength", "Dosage Form" : "dosage_form_route", "Marketing Status" : "marketing_status", "RLD" : "reference_listed_drug", "TE Code" : "therapeutic_equivalence_code" }

page_cats = string.ascii_uppercase

for letter in page_cats:
    r = br.open("http://www.accessdata.fda.gov/scripts/cder/drugsatfda/index.cfm?fuseaction=Search.SearchResults_Browse&DrugInitial=%s&StartRow=1&StepSize=1000000" % letter)
    html = r.read()

    for l in br.links(url_regex='DrugName'):
        data = {}
        req = br.click_link(l)
        br.open(req)
        detail = br.response().read()
        root = lxml.html.fromstring(detail)
        drug_overview_div = root.cssselect("table:contains('Drug Name')")[0]
        for tr in drug_overview_div.cssselect("tr"):
            json_object = []
            json_value = []
            tds = tr.cssselect("td")
            if len(tds) > 1:
                json_object = tds[0].text_content().replace("\r", "").replace("\n", "").replace("\t", "").replace(u"\u2022", u"").strip()
                json_value = tds[1].text_content().replace("\r", "").replace("\n", "").replace("\t", "").replace(u"\u2022", u"").strip()
                for k, v in keys.iteritems():
                    if k in json_object:
                        item = {
                            v : json_value
                        }
                        data.update(item)
        print data