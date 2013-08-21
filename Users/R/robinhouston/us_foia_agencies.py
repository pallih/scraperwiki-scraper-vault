import scraperwiki
import re
import urllib

def get_agency_stubs():
    html = scraperwiki.scrape("http://www.foia.gov/foiareport.js")
    names, abbreviations = {}, {}
    
    for mo in re.finditer(r"^agencies\[(\d+)\]\s*=\s*'([^']*)'", html, re.M):
        names[int(mo.group(1))] = mo.group(2)
    
    for mo in re.finditer(r"^agenciesAb\[(\d+)\]\s*=\s*'([^']*)'", html, re.M):
        abbreviations[int(mo.group(1))] = mo.group(2)
    
    for mo in re.finditer(r"^agenciesFile\[(\d+)\]\s*=\s*'([^']*)'", html, re.M):
        abbreviation = abbreviations[int(mo.group(1))]
        if abbreviation != mo.group(2):
            raise Exception("abbreviation = %s but file = %s" % (abbreviation, mo.group(2)))
    
    return [
        {
            "name": names[n],
            "abbreviation": abbreviations[n],
        }
        for n in names.keys()
    ]

def extract_offices(html, agency_name):
    name, email, website = {}, {}, {}
    for mo in re.finditer(r"""<option value="([^"])">([^<]*)</option>""", html):
        n = int(mo.group(1))
        if n > 0:
            name[n] = mo.group(2)
    
    for n in name.keys():
        mo = re.search(r"""<div id="{n}"[^>]*>(.*?)</div>""".format(n=n), html)
        if mo is None:
            raise Exception("""Failed to find <div id="{n}">""".format(n=n))
        office_html = mo.group(1)
        
        email_mo = re.search(r"""mailto:([^"]*)""", office_html)
        if email_mo is None:
            print "Failed to find email address for %s: %s" % (agency_name, name[n],)
            email[n] = None
        else:
            email[n] = email_mo.group(1)
        
        website_mo = re.search(r"<strong>Website: </strong><a[^>]*>([^<]*)</a>", office_html)
        website[n] = re.sub(r"\s", "", website_mo.group(1))
    
    return [
        {
            "name": name[n],
            "email": email[n],
            "website": website[n],
        }
        for n in sorted(name.keys())
    ]

def get_agency(agency_stub):
    agency_html = scraperwiki.scrape("http://www.foia.gov/foia/FoiaMakeRequest?agency=" + urllib.quote(agency_stub["abbreviation"]))
    return {
        "name": agency_stub["name"],
        "abbreviation": agency_stub["abbreviation"],
        "offices": extract_offices(agency_html, agency_name=agency_stub["name"])
    }

for agency_stub in get_agency_stubs():
    if agency_stub["abbreviation"] == "ALL":
        # The ofices listed in this section are also listed under
        # their actual agencies -- but despite the name not all offices
        # are listed under ALL. So it is best just to ignore it.
        continue
    agency = get_agency(agency_stub)
    for office in agency["offices"]:
        scraperwiki.sqlite.save(unique_keys=["agency_name", "office_name"], data={
            "agency_name": agency["name"],
            "agency_abbreviation": agency["abbreviation"],
            "office_name": office["name"],
            "office_email": office["email"],
            "office_url": office["website"],
        })


