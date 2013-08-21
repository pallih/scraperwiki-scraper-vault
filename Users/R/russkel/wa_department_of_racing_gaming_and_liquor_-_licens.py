import scraperwiki, lxml.html, urllib2, re
from datetime import datetime
import lxml.etree

doc = lxml.html.parse(urllib2.urlopen("http://liquor.reports.rgl.wa.gov.au/liquor/appqry.php"))
root = doc.getroot()

#the html seems rather clean for a gov website, the problem is that it'll need to pull address from the PDF... bah!

for tr in root.xpath("//div[@id='premresult']/table/tr")[1:]:
    data = {
        'council_reference': tr[0].text_content().strip(),
        'description': "%s - %s" % (tr[1].text_content().strip(), tr[2].text_content().strip()),
        'date_received': datetime.strptime(tr[3].text_content().strip(), "%d/%m/%Y"),
        'on_notice_to': datetime.strptime(tr[4].text_content().strip(), "%d/%m/%Y"),
        'address': None, #pulled from LDD2
        'info_url': "http://liquor.reports.rgl.wa.gov.au" + tr[5].xpath(".//a/acronym[@title='Public Interest Assessment']")[0].getparent().get("href"), #PIA pdf
        'comment_url': None,
        'date_scraped': datetime.today()
        #'pdf': tr[5].xpath(".//a")[0].get("href")
    }

    pdfraw = urllib2.urlopen("http://liquor.reports.rgl.wa.gov.au" + tr[5].xpath(".//a/acronym[@title='Notice of Application (Posting on Premises)']")[0].getparent().get("href")).read()
    xmldata = scraperwiki.pdftoxml(pdfraw)

    #simply the xml a little
    xmldata = re.sub("</?[bi]>", '', xmldata)
    print xmldata

    xmlroot = lxml.etree.fromstring(xmldata)

    def flatten_tree(elem):
        res = ""
        if elem.text != None:
            return elem.text
        else:
            for el in elem:
                res += flatten_tree(el)

        return res

    pdfdata = ""

    for page in xmlroot:
        for el in page:
            if el.tag == "text": pdfdata += flatten_tree(el)

    print pdfdata

    data['address'] = re.search("of (.*?) has given notice", pdfdata).group(1)
    print data

    #scraperwiki.sqlite.save(unique_keys=['council_reference'], data=data)

