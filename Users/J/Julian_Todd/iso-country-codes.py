import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import re
import urllib

#<table border="0" cellpadding="0" cellspacing="1" style="font-size:10px;">
def LoadCodes():
    url = "http://www.iso.org/iso/country_codes/iso_3166_code_lists/iso-3166-1_decoding_table.htm"
    print url
    html = urllib.urlopen(url).read()
    html = re.sub("<tr><", "<tr>", html)   # type on Finland
    root = lxml.html.fromstring(html)

    table = root.cssselect("table")[2]
    rows = table.cssselect("tr")
    headings = [ std.text  for std in rows[0].cssselect("td strong") ]
    assert headings == ['Code', 'English Name ', 'French Name ', None, 'Remark ', 'Status of Code Element'], headings

    for row in rows[1:]:
        tds = row.cssselect("td")
        data = {}
        data["code"] = tds[0].cssselect("div")[0].text
        data["english"] = tds[1].cssselect("a")[0].tail
        data["french"] = tds[2].text
        data["status"] = tds[4].text
        scraperwiki.datastore.save(unique_keys=["code"], data=data)

        
countrycorrections = { 
   "USA":"UNITED STATES", 
                     }

def convertcode(country, language):
    ucountry = country.upper()
    ucountry = countrycorrections.get(ucountry, ucountry)
    if language == "french" and ucountry == "FRANCE":
        ucountry = "France"
    result = scraperwiki.datastore.retrieve({language:ucountry})
    result = [ data  for data in result  if data["data"][language] == ucountry ]   # seems to match case insensitive!
    if len(result) == 1:
        return result[0]["data"]["code"]
    return "AAuknown"

    
def getcode(input, language="english"):
    result = [ ]
    for country in input.split(","):
        if country:
            result.append(convertcode(country, language))
    print ", ".join(result)

    
def getcountry(code, language="english"):
    result = scraperwiki.datastore.retrieve({"code":code})
    if result:
        print result[0]["data"][language]
    else:
        print "Not found"
