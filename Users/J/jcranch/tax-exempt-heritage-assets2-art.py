"""
HMRC's tax-exempt heritage assets: works of art

The second category listed here:
  http://www.hmrc.gov.uk/heritage/
"""


from scraperwiki import datastore
import scraperwiki
from urllib import urlopen
import re


def main():

    url = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDbQueryServlet?location=All&class1=All&freetext=&Submit=search"
    lines = iter(urlopen(url))

    postcode = re.compile("^\s*([A-Z][A-Z]?[0-9][0-9]?[A-Z]?)\s*([0-9][ABD-HJLNP-UW-Z][ABD-HJLNP-UW-Z])\s*$")
    
    keyvaluepairs = {}

    for l in lines:

        for l in lines:
            if re.search("<TR align=\"left\" Valign='top'>",l):
                keyvaluepairs = {}
                break
        else:
            break # Don't loop through if there's no more records

        # link and serial number
        l = lines.next()
        m = re.search("<A HREF='(.*)'>",l)
        link = "http://www.visitukheritage.gov.uk" + m.groups()[0]
        keyvaluepairs["Link"] = link
        m = re.search("<B>([0-9]*)</B>",l)
        serial = m.groups()[0]
        keyvaluepairs["Serial"] = serial
        print
        print "%s:"%serial

        # location
        for l in lines:
            m = re.search("<TD>(.*)</TD>",l)
            if m:
                keyvaluepairs["Location"] = m.groups()[0]
                break

        # separate page
        datapage = "".join(urlopen(link)).replace("\n","")
        for m in re.finditer("<font face=\"Arial, Helvetica, sans-serif\" size=\"-1\">([^<]*)</font></b></td><td[^>]*align=\"left\">([^<]*)</td",datapage):
            k = m.groups()[0].strip().strip(":")
            v = m.groups()[1].replace("<br>","\n").strip()
            if v != "":
                keyvaluepairs[k] = v
        for m in re.finditer("<font face=\"Arial, Helvetica, sans-serif\" size=\"-1\">([^<]*)</font></b></td><td[^>]*align=\"left\"><a href=([^>]*)>",datapage):
            k = m.groups()[0].strip().strip(":")
            v = m.groups()[1].replace("<br>","\n").strip()
            if v != "":
                keyvaluepairs[k] = v

        # tidy up the address
        if "Contact Address" in keyvaluepairs:
            raw_address = [x.strip() for x in keyvaluepairs["Contact Address"].split(",")]
            # separate off a phone number
            if len(raw_address)>0 and re.match("[ 0-9]*",raw_address[-1]):
                keyvaluepairs["Contact Telephone Number"] = raw_address[-1]
                raw_address = raw_address[:-1]
            if len(raw_address)>0 and re.match(postcode,raw_address[-1]):
                keyvaluepairs["Contact Postcode"] = raw_address[-1]
                raw_address = raw_address[:-1]
            keyvaluepairs["Contact Address"] = ", ".join(raw_address)

                
        # describe the item        
        if "Description" in keyvaluepairs:
            print " - " + keyvaluepairs["Description"]

        if not "Unique ID" in keyvaluepairs:
            print keyvaluepairs

        # now save it
        scraperwiki.sqlite.save(unique_keys=["Unique ID"],data=keyvaluepairs)


        
main()
