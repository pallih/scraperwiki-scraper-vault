import scraperwiki
import mechanize
import re
from StringIO import StringIO

from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree


# main loop going through all the pages and using lists of readings
def Main():
    br = mechanize.Browser()
    br.set_handle_robots(False)  # whole thing crashes if you don't do this
    for n in range(1, 120):
        print "*** Scraping page", n
        readings = ScrapeFromIndexPage(br, n)
                       
        # this is the place we would save the pages into the datastore
        for reading in readings:        
            params = Parse(reading)
            print "%s (%s)" % (params["name"], params["constituency"])
            scraperwiki.datastore.save(["constituency"], params)


def TWFYconstituencies():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    result = { }
    for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist):
        lcon = re.sub(",", "", con)
        lcon = re.sub("-", " ", lcon).lower()
        result[lcon] = con
    return result

twfyconstituencies = TWFYconstituencies()


twfyconstituencies
def RegularizeConstituency(lcon):
    lcon = re.sub(",", "", lcon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    corrections = {'Dover and Deal':"Dover", 'Carmarthen W and S Pembrokeshire':'Carmarthen West and South Pembrokeshire', 
                   'Ribble South and West Lancashire':"South Ribble", 'Morecombe and Lunesdale':"Morecambe and Lunesdale", 
                   'Hereford':"Hereford and South Herefordshire", 'Ogwr':"Ogmore", 
                   'Canterbury and Whitstable':"Canterbury", 'Ayrshire Central':"Central Ayrshire", 
                   'Dorset Mid and North Poole':'Mid Dorset and North Poole', 'Taunton':'Taunton Deane', 'Castlepoint':'Castle Point',
                   'Romsey':'Romsey and Southampton North', 'Linlithgow and Falkirk East':'Linlithgow and East Falkirk', 
                   'Pontefract and Castleford':'Normanton Pontefract and Castleford', 'Worthing East and Shoreham': 'East Worthing and Shoreham',
                   'East Kilbride Stathaven and Lesmahagow': 'East Kilbride Strathaven and Lesmahagow',
                   'Ayr New Cumnock and Carrick': 'Ayr Carrick and Cumnock', 'North Ayrshire and Isle of Arran': 'North Ayrshire and Arran',
                   'South East Oxfordshire': 'Henley'}
    lcon = corrections.get(lcon, lcon)
    return twfyconstituencies[lcon.lower()]

def SimplifyHTML(div):
    html = lxml.etree.tostring(div)
    t = re.sub("<p>", "NEWLINE", html)
    t = re.sub("<h2>(.*)</h2>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t


def Parse(reading):
    result = { "url": reading["url"] }
    text = reading["text"]

    text = re.sub("<p<", "", text)   # this error too severe for parser to handle
    doc = lxml.html.parse(StringIO(text))
    root = doc.getroot()
    #body = h.find(".//body")
    maindiv = CSSSelector("#divMiddleLeftCentreBottomRight")(root)[0]    

    heading = CSSSelector("#divHeading h1")(maindiv)[0].text
    intro = CSSSelector("#divIntroduction h2")(maindiv)[0]
    h2 = lxml.etree.tounicode(intro)
    #print [heading, h2]
    
    mheading = re.match(u"([\w\s\-']*?)\s*(?:\u2013\s*(?:PPC for (.*?)$)?|$)", heading)
    result["name"] = mheading.group(1)

    mmpfor = re.search(u'(?:<br\s*/>)?\s*MP for (.*?)\s*<br\s*/>', h2)
    if mmpfor:
        result["MP for"] = mmpfor.group(1)
        result["MP for"] = result["MP for"]   # needs to be regularized for the 2005 boundaries

        
    mcandidate = re.search(u'Liberal Democrat candidate for <a href="in_your_area_detail.aspx.*?">(.*?)</a>', h2)
    if mcandidate:
        result["constituency"] = RegularizeConstituency(mcandidate.group(1))
    elif mheading.group(2):
        result["constituency"] = RegularizeConstituency(mheading.group(2))
    elif "MP for" in result:
        result["constituency"] = RegularizeConstituency(result["MP for"])
    else:
        assert False, (h2, heading)
    
    divImage = maindiv.cssselect("#divIntroduction a img")
    if divImage:
        result["image"] = divImage[0].get("src")
        
        
    #print maindiv.cssselect("#divAboutMe h2")[0].text, "About Me"
    
    for traboutme in maindiv.cssselect("#divAboutMe tr"):
        key = traboutme.cssselect("th")[0].text[:-1]
        assert key in ["Marital Status", "Occupation", "Education"]
        value = traboutme.cssselect("td")[0].text
        if value:
            value = re.sub(u"\u2019", "'", value).strip()
            value = re.sub(u"\u2013", "-", value)
            value = re.sub("\xae", "", value)
            value = re.sub("\s*\n\s*", "; ", value)
            result[key] = value
        
    divBiography = maindiv.cssselect("#divBiography")
    if divBiography:
        result["bio"] = SimplifyHTML(divBiography[0])
        result["bio"] = re.sub("^Biography\s+", "", result["bio"])  # clean out leading title


    contacttext = lxml.etree.tounicode(maindiv.cssselect("#divIndividualContactInfo")[0])
    
    memail = re.search('<strong>Email:</strong> <a href="(?:mailto:)?(.*?)">', contacttext)
    if memail:
        result["email"] = memail.group(1)
        
    mwebsite = re.search('<strong>Website:</strong> <a href="(.*?)">', contacttext)
    if mwebsite:
        result["website"] = mwebsite.group(1)
        
    mphone = re.search('<strong>Telephone:</strong> ([\d\s]+)', contacttext)
    if mphone:
        result["phone"] = mphone.group(1).strip()
        
    address = "; ".join([ addressline.text  for addressline in maindiv.cssselect("#divIndividualContactInfo ul li") ])
    if address:
        result["address"] = address.encode("ascii", "replace")  # the database doesn't seem to be unicode.  it should be
        
    return result
    


# single page of links to Candidate pages.  There are 85 of them
def ScrapeFromIndexPage(br, n):
    readings = [ ]
    br.open("http://www.libdems.org.uk/parliamentary_candidates.aspx?show=Candidates&pgNo=%d" % n)
    for link in list(br.links()):
        if re.match("parliamentary_candidates_detail.aspx\?", link.url) and not re.search("\[IMG\]", link.text):
            response = br.follow_link(link)
            reading = { "text": response.read(), "url": br.geturl() }
            readings.append(reading)
            br.back()
    return readings


Main()                      
