import scraperwiki

import lxml.etree
import urllib
import re
import types


words = ["Roman Catholic Archdiocese of Boston","Roman Catholic Diocese of Burlington","Roman Catholic Diocese of Fall River","Roman Catholic Diocese of Manchester","Roman Catholic Diocese of Portland","Roman Catholic Diocese of Springfield in Massachusetts","Roman Catholic Diocese of Worcester","Roman Catholic Archdiocese of Hartford","Roman Catholic Diocese of Bridgeport","Roman Catholic Diocese of Norwich","Roman Catholic Diocese of Providence","Roman Catholic Archdiocese of New York","Roman Catholic Diocese of Albany","Roman Catholic Diocese of Brooklyn","Roman Catholic Diocese of Buffalo","Roman Catholic Diocese of Ogdensburg","Roman Catholic Diocese of Rochester","Roman Catholic Diocese of Rockville Centre","Roman Catholic Diocese of Syracuse","Roman Catholic Archdiocese of Newark","Roman Catholic Diocese of Camden","Roman Catholic Diocese of Metuchen","Roman Catholic Diocese of Paterson","Roman Catholic Diocese of Trenton","Roman Catholic Archdiocese of Philadelphia","Roman Catholic Diocese of Allentown","Roman Catholic Diocese of Altoona-Johnstown","Roman Catholic Diocese of Erie","Roman Catholic Diocese of Greensburg","Roman Catholic Diocese of Harrisburg","Roman Catholic Diocese of Pittsburgh","Roman Catholic Diocese of Scranton","Roman Catholic Archdiocese of Baltimore","Roman Catholic Diocese of Arlington","Roman Catholic Diocese of Richmond","Roman Catholic Diocese of Wheeling-Charleston","Roman Catholic Diocese of Wilmington","Roman Catholic Archdiocese of Washington","Roman Catholic Diocese of Saint Thomas","Roman Catholic Archdiocese of Louisville","Roman Catholic Diocese of Covington","Roman Catholic Diocese of Knoxville","Roman Catholic Diocese of Lexington","Roman Catholic Diocese of Memphis","Roman Catholic Diocese of Nashville","Roman Catholic Diocese of Owensboro","Roman Catholic Archdiocese of Mobile","Roman Catholic Diocese of Biloxi","Roman Catholic Diocese of Birmingham in Alabama","Roman Catholic Diocese of Jackson","Roman Catholic Archdiocese of New Orleans","Roman Catholic Diocese of Alexandria in Louisiana","Roman Catholic Diocese of Baton Rouge","Roman Catholic Diocese of Houma-Thibodaux","Roman Catholic Diocese of Lafayette in Louisiana","Roman Catholic Diocese of Lake Charles","Roman Catholic Diocese of Shreveport","Roman Catholic Archdiocese of Cincinnati","Roman Catholic Diocese of Cleveland","Roman Catholic Diocese of Columbus","Roman Catholic Diocese of Steubenville","Roman Catholic Diocese of Toledo","Roman Catholic Diocese of Youngstown","Roman Catholic Archdiocese of Detroit","Roman Catholic Diocese of Gaylord","Roman Catholic Diocese of Grand Rapids","Roman Catholic Diocese of Kalamazoo","Roman Catholic Diocese of Lansing","Roman Catholic Diocese of Marquette","Roman Catholic Diocese of Saginaw","Roman Catholic Ecclesiasical province of Chicago","Roman Catholic Archdiocese of Chicago","Roman Catholic Diocese of Belleville","Roman Catholic Diocese of Joliet in Illinois","Roman Catholic Diocese of Peoria","Roman Catholic Diocese of Rockford","Roman Catholic Diocese of Springfield in Illinois","Roman Catholic Archdiocese of Indianapolis","Roman Catholic Diocese of Evansville","Roman Catholic Diocese of Fort Wayne-South Bend","Roman Catholic Diocese of Gary","Roman Catholic Diocese of Lafayette in Indiana","Roman Catholic Archdiocese of Milwaukee","Roman Catholic Diocese of Green Bay","Roman Catholic Diocese of La Crosse","Roman Catholic Diocese of Madison","Roman Catholic Diocese of Superior","Roman Catholic Archdiocese of Saint Paul and Minneapolis","Roman Catholic Diocese of Bismarck","Roman Catholic Diocese of Crookston","Roman Catholic Diocese of Duluth","Roman Catholic Diocese of Fargo","Roman Catholic Diocese of New Ulm","Roman Catholic Diocese of Rapid City","Roman Catholic Diocese of Saint Cloud","Roman Catholic Diocese of Sioux Falls","Roman Catholic Diocese of Winona","Roman Catholic Archdiocese of Dubuque","Roman Catholic Diocese of Davenport","Roman Catholic Diocese of Des Moines","Roman Catholic Diocese of Sioux City","Roman Catholic Archdiocese of Kansas City in Kansas","Roman Catholic Diocese of Dodge City","Roman Catholic Diocese of Salina","Roman Catholic Diocese of Wichita","Roman Catholic Archdiocese of Omaha","Roman Catholic Diocese of Grand Island","Roman Catholic Diocese of Lincoln","Roman Catholic Archdiocese of St. Louis","Roman Catholic Diocese of Jefferson City","Roman Catholic Diocese of Kansas City-Saint Joseph","Roman Catholic Diocese of Springfield-Cape Girardeau","Roman Catholic Archdiocese of Galveston-Houston","Roman Catholic Diocese of Austin","Roman Catholic Diocese of Beaumont","Roman Catholic Diocese of Brownsville","Roman Catholic Diocese of Corpus Christi","Roman Catholic Diocese of Tyler","Roman Catholic Diocese of Victoria in Texas","Roman Catholic Archdiocese of Oklahoma City","Roman Catholic Diocese of Little Rock","Roman Catholic Diocese of Tulsa","Roman Catholic Archdiocese of Los Angeles","Roman Catholic Diocese of Fresno","Roman Catholic Diocese of Monterey in California","Roman Catholic Diocese of Orange","Roman Catholic Diocese of San Bernardino","Roman Catholic Diocese of San Diego","Roman Catholic Archdiocese of San Francisco","Roman Catholic Diocese of Honolulu","Roman Catholic Diocese of Las Vegas","Roman Catholic Diocese of Oakland","Roman Catholic Diocese of Reno","Roman Catholic Diocese of Sacramento","Roman Catholic Diocese of Salt Lake City (","Roman Catholic Diocese of San Jose in California","Roman Catholic Diocese of Santa Rosa in California","Roman Catholic Diocese of Stockton","Roman Catholic Archdiocese of Anchorage","Roman Catholic Diocese of Fairbanks","Roman Catholic Diocese of Juneau","Roman Catholic Archdiocese of Portland in Oregon","Roman Catholic Diocese of Baker","Roman Catholic Diocese of Boise","Roman Catholic Diocese of Great Falls-Billings","Roman Catholic Diocese of Helena","Roman Catholic Archdiocese of Seattle","Roman Catholic Diocese of Spokane","Roman Catholic Diocese of Yakima","Roman Catholic Archdiocese of Denver","Roman Catholic Diocese of Cheyenne","Roman Catholic Diocese of Colorado Springs","Roman Catholic Diocese of Pueblo","Roman Catholic Archdiocese of Santa Fe","Roman Catholic Diocese of Gallup","Roman Catholic Diocese of Las Cruces","Roman Catholic Diocese of Phoenix","Roman Catholic Diocese of Tucson","Roman Catholic Archdiocese of San Antonio","Roman Catholic Diocese of Amarillo","Roman Catholic Diocese of Dallas","Roman Catholic Diocese of El Paso","Roman Catholic Diocese of Fort Worth","Roman Catholic Diocese of Laredo","Roman Catholic Diocese of Lubbock","Roman Catholic Diocese of San Angelo","Roman Catholic Archdiocese of Miami","Roman Catholic Diocese of Orlando","Roman Catholic Diocese of Palm Beach","Roman Catholic Diocese of Pensacola-Tallahassee","Roman Catholic Diocese of St. Augustine","Roman Catholic Diocese of Saint Petersburg","Roman Catholic Diocese of Venice in Florida","Roman Catholic Archdiocese of Atlanta","Roman Catholic Diocese of Charleston","Roman Catholic Diocese of Charlotte","Roman Catholic Diocese of Raleigh","Roman Catholic Diocese of Savannah"]
data = {}

for w in words:
    title = w
    
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    
    print "The Wikipedia text for", title, "is"
    fulltext = revs[-1].text
    # print fulltext
    # infobox = re.search(r'(Infobox)*',fulltext) 
    infobox = re.compile('Infobox(.*?)footnotes', re.DOTALL | re.IGNORECASE).findall(fulltext)
    print infobox

    if (len(infobox) > 0):
        #name
        name=""
        name= re.compile('name(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        print name[0][1].strip()
        data['name'] = name[0][1].strip()
    
        #province
        province = ""
        provincew = ""
        province= re.compile('province(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        provincew= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(province[0][1])
        if (type(provincew).__name__ == 'list' and len(provincew) > 0):
            data['province'] = provincew[0].strip()
        else:
            data['province'] = province[0][1].strip()
    
        #bishop
        bishop=""
        bishopw=""
        bishop= re.compile('bishop(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        bishopw= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(bishop[0][1])
        if (type(bishopw).__name__ == 'list' and len(bishopw) > 0):
            data ['bishop'] = bishopw[0].strip()
        else:
            data ['bishop'] = bishop[0][1].strip()
        
        #cathedral
        cathedral = ""
        cathedralw = ""
        cathedral= re.compile('cathedral(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        cathedralw= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(cathedral[0][1])
        if (type(cathedralw).__name__ == 'list' and len(cathedralw) > 0):
            data['cathedral'] = cathedralw[0].strip()
        else:
            data['cathedral'] = cathedral[0][1].strip()
    
        # metropolitan
        metropolitan = ""
        metropolitan = re.compile('metropolitan(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        metropolitan = re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(metropolitan[0][1])
        if (type(metropolitan).__name__ == 'list' and len(metropolitan) > 0):
            data['metropolitan'] = metropolitan[0].strip()
    
    
        # website
        website = ""
        website = re.compile('website(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        website = re.compile("(?P<url>https?://[^\s]+)", re.DOTALL | re.IGNORECASE).findall(website[0][1])
        data['website'] = website[0].strip()
        print "-----"
    
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)import scraperwiki

import lxml.etree
import urllib
import re
import types


words = ["Roman Catholic Archdiocese of Boston","Roman Catholic Diocese of Burlington","Roman Catholic Diocese of Fall River","Roman Catholic Diocese of Manchester","Roman Catholic Diocese of Portland","Roman Catholic Diocese of Springfield in Massachusetts","Roman Catholic Diocese of Worcester","Roman Catholic Archdiocese of Hartford","Roman Catholic Diocese of Bridgeport","Roman Catholic Diocese of Norwich","Roman Catholic Diocese of Providence","Roman Catholic Archdiocese of New York","Roman Catholic Diocese of Albany","Roman Catholic Diocese of Brooklyn","Roman Catholic Diocese of Buffalo","Roman Catholic Diocese of Ogdensburg","Roman Catholic Diocese of Rochester","Roman Catholic Diocese of Rockville Centre","Roman Catholic Diocese of Syracuse","Roman Catholic Archdiocese of Newark","Roman Catholic Diocese of Camden","Roman Catholic Diocese of Metuchen","Roman Catholic Diocese of Paterson","Roman Catholic Diocese of Trenton","Roman Catholic Archdiocese of Philadelphia","Roman Catholic Diocese of Allentown","Roman Catholic Diocese of Altoona-Johnstown","Roman Catholic Diocese of Erie","Roman Catholic Diocese of Greensburg","Roman Catholic Diocese of Harrisburg","Roman Catholic Diocese of Pittsburgh","Roman Catholic Diocese of Scranton","Roman Catholic Archdiocese of Baltimore","Roman Catholic Diocese of Arlington","Roman Catholic Diocese of Richmond","Roman Catholic Diocese of Wheeling-Charleston","Roman Catholic Diocese of Wilmington","Roman Catholic Archdiocese of Washington","Roman Catholic Diocese of Saint Thomas","Roman Catholic Archdiocese of Louisville","Roman Catholic Diocese of Covington","Roman Catholic Diocese of Knoxville","Roman Catholic Diocese of Lexington","Roman Catholic Diocese of Memphis","Roman Catholic Diocese of Nashville","Roman Catholic Diocese of Owensboro","Roman Catholic Archdiocese of Mobile","Roman Catholic Diocese of Biloxi","Roman Catholic Diocese of Birmingham in Alabama","Roman Catholic Diocese of Jackson","Roman Catholic Archdiocese of New Orleans","Roman Catholic Diocese of Alexandria in Louisiana","Roman Catholic Diocese of Baton Rouge","Roman Catholic Diocese of Houma-Thibodaux","Roman Catholic Diocese of Lafayette in Louisiana","Roman Catholic Diocese of Lake Charles","Roman Catholic Diocese of Shreveport","Roman Catholic Archdiocese of Cincinnati","Roman Catholic Diocese of Cleveland","Roman Catholic Diocese of Columbus","Roman Catholic Diocese of Steubenville","Roman Catholic Diocese of Toledo","Roman Catholic Diocese of Youngstown","Roman Catholic Archdiocese of Detroit","Roman Catholic Diocese of Gaylord","Roman Catholic Diocese of Grand Rapids","Roman Catholic Diocese of Kalamazoo","Roman Catholic Diocese of Lansing","Roman Catholic Diocese of Marquette","Roman Catholic Diocese of Saginaw","Roman Catholic Ecclesiasical province of Chicago","Roman Catholic Archdiocese of Chicago","Roman Catholic Diocese of Belleville","Roman Catholic Diocese of Joliet in Illinois","Roman Catholic Diocese of Peoria","Roman Catholic Diocese of Rockford","Roman Catholic Diocese of Springfield in Illinois","Roman Catholic Archdiocese of Indianapolis","Roman Catholic Diocese of Evansville","Roman Catholic Diocese of Fort Wayne-South Bend","Roman Catholic Diocese of Gary","Roman Catholic Diocese of Lafayette in Indiana","Roman Catholic Archdiocese of Milwaukee","Roman Catholic Diocese of Green Bay","Roman Catholic Diocese of La Crosse","Roman Catholic Diocese of Madison","Roman Catholic Diocese of Superior","Roman Catholic Archdiocese of Saint Paul and Minneapolis","Roman Catholic Diocese of Bismarck","Roman Catholic Diocese of Crookston","Roman Catholic Diocese of Duluth","Roman Catholic Diocese of Fargo","Roman Catholic Diocese of New Ulm","Roman Catholic Diocese of Rapid City","Roman Catholic Diocese of Saint Cloud","Roman Catholic Diocese of Sioux Falls","Roman Catholic Diocese of Winona","Roman Catholic Archdiocese of Dubuque","Roman Catholic Diocese of Davenport","Roman Catholic Diocese of Des Moines","Roman Catholic Diocese of Sioux City","Roman Catholic Archdiocese of Kansas City in Kansas","Roman Catholic Diocese of Dodge City","Roman Catholic Diocese of Salina","Roman Catholic Diocese of Wichita","Roman Catholic Archdiocese of Omaha","Roman Catholic Diocese of Grand Island","Roman Catholic Diocese of Lincoln","Roman Catholic Archdiocese of St. Louis","Roman Catholic Diocese of Jefferson City","Roman Catholic Diocese of Kansas City-Saint Joseph","Roman Catholic Diocese of Springfield-Cape Girardeau","Roman Catholic Archdiocese of Galveston-Houston","Roman Catholic Diocese of Austin","Roman Catholic Diocese of Beaumont","Roman Catholic Diocese of Brownsville","Roman Catholic Diocese of Corpus Christi","Roman Catholic Diocese of Tyler","Roman Catholic Diocese of Victoria in Texas","Roman Catholic Archdiocese of Oklahoma City","Roman Catholic Diocese of Little Rock","Roman Catholic Diocese of Tulsa","Roman Catholic Archdiocese of Los Angeles","Roman Catholic Diocese of Fresno","Roman Catholic Diocese of Monterey in California","Roman Catholic Diocese of Orange","Roman Catholic Diocese of San Bernardino","Roman Catholic Diocese of San Diego","Roman Catholic Archdiocese of San Francisco","Roman Catholic Diocese of Honolulu","Roman Catholic Diocese of Las Vegas","Roman Catholic Diocese of Oakland","Roman Catholic Diocese of Reno","Roman Catholic Diocese of Sacramento","Roman Catholic Diocese of Salt Lake City (","Roman Catholic Diocese of San Jose in California","Roman Catholic Diocese of Santa Rosa in California","Roman Catholic Diocese of Stockton","Roman Catholic Archdiocese of Anchorage","Roman Catholic Diocese of Fairbanks","Roman Catholic Diocese of Juneau","Roman Catholic Archdiocese of Portland in Oregon","Roman Catholic Diocese of Baker","Roman Catholic Diocese of Boise","Roman Catholic Diocese of Great Falls-Billings","Roman Catholic Diocese of Helena","Roman Catholic Archdiocese of Seattle","Roman Catholic Diocese of Spokane","Roman Catholic Diocese of Yakima","Roman Catholic Archdiocese of Denver","Roman Catholic Diocese of Cheyenne","Roman Catholic Diocese of Colorado Springs","Roman Catholic Diocese of Pueblo","Roman Catholic Archdiocese of Santa Fe","Roman Catholic Diocese of Gallup","Roman Catholic Diocese of Las Cruces","Roman Catholic Diocese of Phoenix","Roman Catholic Diocese of Tucson","Roman Catholic Archdiocese of San Antonio","Roman Catholic Diocese of Amarillo","Roman Catholic Diocese of Dallas","Roman Catholic Diocese of El Paso","Roman Catholic Diocese of Fort Worth","Roman Catholic Diocese of Laredo","Roman Catholic Diocese of Lubbock","Roman Catholic Diocese of San Angelo","Roman Catholic Archdiocese of Miami","Roman Catholic Diocese of Orlando","Roman Catholic Diocese of Palm Beach","Roman Catholic Diocese of Pensacola-Tallahassee","Roman Catholic Diocese of St. Augustine","Roman Catholic Diocese of Saint Petersburg","Roman Catholic Diocese of Venice in Florida","Roman Catholic Archdiocese of Atlanta","Roman Catholic Diocese of Charleston","Roman Catholic Diocese of Charlotte","Roman Catholic Diocese of Raleigh","Roman Catholic Diocese of Savannah"]
data = {}

for w in words:
    title = w
    
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    tree = lxml.etree.parse(urllib.urlopen(url))
    revs = tree.xpath('//rev')
    
    print "The Wikipedia text for", title, "is"
    fulltext = revs[-1].text
    # print fulltext
    # infobox = re.search(r'(Infobox)*',fulltext) 
    infobox = re.compile('Infobox(.*?)footnotes', re.DOTALL | re.IGNORECASE).findall(fulltext)
    print infobox

    if (len(infobox) > 0):
        #name
        name=""
        name= re.compile('name(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        print name[0][1].strip()
        data['name'] = name[0][1].strip()
    
        #province
        province = ""
        provincew = ""
        province= re.compile('province(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        provincew= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(province[0][1])
        if (type(provincew).__name__ == 'list' and len(provincew) > 0):
            data['province'] = provincew[0].strip()
        else:
            data['province'] = province[0][1].strip()
    
        #bishop
        bishop=""
        bishopw=""
        bishop= re.compile('bishop(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        bishopw= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(bishop[0][1])
        if (type(bishopw).__name__ == 'list' and len(bishopw) > 0):
            data ['bishop'] = bishopw[0].strip()
        else:
            data ['bishop'] = bishop[0][1].strip()
        
        #cathedral
        cathedral = ""
        cathedralw = ""
        cathedral= re.compile('cathedral(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        cathedralw= re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(cathedral[0][1])
        if (type(cathedralw).__name__ == 'list' and len(cathedralw) > 0):
            data['cathedral'] = cathedralw[0].strip()
        else:
            data['cathedral'] = cathedral[0][1].strip()
    
        # metropolitan
        metropolitan = ""
        metropolitan = re.compile('metropolitan(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        metropolitan = re.compile('\[\[(.*?)\|', re.DOTALL | re.IGNORECASE).findall(metropolitan[0][1])
        if (type(metropolitan).__name__ == 'list' and len(metropolitan) > 0):
            data['metropolitan'] = metropolitan[0].strip()
    
    
        # website
        website = ""
        website = re.compile('website(.*?)=(.*?)\n', re.DOTALL | re.IGNORECASE).findall(infobox[0])
        website = re.compile("(?P<url>https?://[^\s]+)", re.DOTALL | re.IGNORECASE).findall(website[0][1])
        data['website'] = website[0].strip()
        print "-----"
    
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)