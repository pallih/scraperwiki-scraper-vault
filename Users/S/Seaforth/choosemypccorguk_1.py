import scraperwiki
import StringIO
import re
import lxml.html

"""
  Adapted from timgreens' code. Kudos to you.
"""

police_areas = [x.strip() for x in """Avon Somerset
    Bedfordshire
    Cambridgeshire
    Cheshire
    Cleveland
    Cumbria
    Derbyshire
    Devon Cornwall
    Dorset
    Durham
    Dyfed Powys
    Essex
    Gloucestershire
    Greater Manchester
    Gwent
    Hampshire
    Hertfordshire 
    Humberside 
    Kent 
    Lancashire 
    Leicestershire 
    Lincolnshire 
    Merseyside 
    Norfolk 
    Northamptonshire 
    Northumbria 
    North Wales 
    North Yorkshire 
    Nottinghamshire 
    South Wales 
    South Yorkshire 
    Staffordshire 
    Suffolk 
    Surrey 
    Sussex 
    Thames Valley 
    Warwickshire 
    West Mercia 
    West Midlands 
    West Yorkshire
    Wiltshire""".split("\n")]

print len(police_areas)

area_page = "http://www.choosemypcc.org.uk/candidates/area/%s"





urls = '(?: %s)' % '|'.join("""http telnet gopher file wais
ftp www""".split())
ltrs = r'\w'
gunk = r'/#~:.?+=&%@!\-'
punc = r'.:?\-'
any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                     'gunk' : gunk,
                                     'punc' : punc }

url = r"""
    \b                            # start at word boundary
        %(urls)s    :             # need resource and a colon
        [%(any)s]  +?             # followed by one or more
                                  #  of any valid character, but
                                  #  be conservative and take only
                                  #  what you need to....
    (?=                           # look-ahead non-consumptive assertion
            [%(punc)s]*           # either 0 or more punctuation
            (?:   [^%(any)s]      #  followed by a non-url char
                |                 #   or end of the string
                  $
            )
    )
    """ % {'urls' : urls,
           'any' : any,
           'punc' : punc }

url_re = re.compile(url, re.VERBOSE | re.MULTILINE)




candidates = scraperwiki.sqlite.select("* from pcc_candidates")
#candidates = []

if False:
    for police_area in police_areas:
        slug = police_area.replace(" ", "-").lower()
        area_url = area_page % slug
        print(area_url)
        tree = lxml.html.parse(area_url)
        for candidate_box in tree.xpath("//div[@class='related-candidate']"):
            try:
                candidate_image = candidate_box.xpath("./a/img/@src")[0]
            except IndexError:
                candidate_image = None

            candidate_name = candidate_box.xpath("./h4")[0].text_content().strip()
            
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            candidate_party = candidate_box.xpath("./p")[0].text_content().strip()
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            print "%s (%s)" % (candidate_name, candidate_party)
    
            data = {'candidate_url': candidate_url,
                'candidate_image_small': candidate_image,
                'candidate_name': candidate_name,
                'candidate_party': candidate_party,
                'police_area': slug}
    
            candidates.append(data)

print (len(candidates))
scraperwiki.sqlite.save(["candidate_url"], candidates, "pcc_candidates")

for candidate in candidates:
    print candidate['candidate_name']
    print "-" + candidate['candidate_url'][0:7] + "-"
    print ('unknown' in candidate['candidate_url'][0:7])
    if  (candidate['candidate_url'][0:7] == 'unknown'):
        continue

    if 'candidate_content' not in candidate:
        try:
            tree = lxml.html.parse(candidate['candidate_url'])
            content = lxml.html.tostring(tree.xpath("//div[@class='col12']")[0])
            candidate['candidate_content'] = content
        except:
            continue
    else:
        tree = lxml.html.parse(StringIO.StringIO(candidate['candidate_content']))

    if 'candidate_image_big' not in candidate:
        candidate_image_big = tree.xpath('//img[@class="attachment-candidate"]/@src')[0]
        candidate['candidate_image_big'] = candidate_image_big


    if candidate['candidate_content'] is not None:
        candidate['candidate_content_text'] = lxml.html.fromstring(candidate['candidate_content']).text_content()
    else:
        candidate['candidate_content'] = ""
        candidate['candidate_content_text'] = ""

    print(candidate['candidate_content'])
    print(candidate['candidate_content_text'])
    facebook = re.findall("www\.facebook\.com/([^ ]+)", candidate['candidate_content_text'])

    if len(facebook) != 0:
        candidate['facebook'] = "https://www.facebook.com/" + facebook[0]

    website = url_re.findall(candidate['candidate_content_text'])
    if len(website) != 0:
        websites = ""
        for wbs in website:
            websites = websites.join(wbs.join("\n"))
        candidate['website'] = websites
    
    try:
        candidate_en_email = tree.xpath("//a[@id='__cf_email__']/@class")[0]
    except:
        candidate_en_email = ""

    if candidate_en_email != "":
        a = candidate_en_email 
        s=''
        r = int(a[0:2],16)
        for j in xrange(2, len(a), 2):
            c = a[j:j+2]
            cstr = str(unichr(int(c,16)^r))
            s = s + cstr    
        candidate_email = s
    else:
        candidate_email = "" 


    candidate['email'] = candidate_email


    scraperwiki.sqlite.save(["candidate_url"], candidate, "pcc_candidates")


import scraperwiki
import StringIO
import re
import lxml.html

"""
  Adapted from timgreens' code. Kudos to you.
"""

police_areas = [x.strip() for x in """Avon Somerset
    Bedfordshire
    Cambridgeshire
    Cheshire
    Cleveland
    Cumbria
    Derbyshire
    Devon Cornwall
    Dorset
    Durham
    Dyfed Powys
    Essex
    Gloucestershire
    Greater Manchester
    Gwent
    Hampshire
    Hertfordshire 
    Humberside 
    Kent 
    Lancashire 
    Leicestershire 
    Lincolnshire 
    Merseyside 
    Norfolk 
    Northamptonshire 
    Northumbria 
    North Wales 
    North Yorkshire 
    Nottinghamshire 
    South Wales 
    South Yorkshire 
    Staffordshire 
    Suffolk 
    Surrey 
    Sussex 
    Thames Valley 
    Warwickshire 
    West Mercia 
    West Midlands 
    West Yorkshire
    Wiltshire""".split("\n")]

print len(police_areas)

area_page = "http://www.choosemypcc.org.uk/candidates/area/%s"





urls = '(?: %s)' % '|'.join("""http telnet gopher file wais
ftp www""".split())
ltrs = r'\w'
gunk = r'/#~:.?+=&%@!\-'
punc = r'.:?\-'
any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                     'gunk' : gunk,
                                     'punc' : punc }

url = r"""
    \b                            # start at word boundary
        %(urls)s    :             # need resource and a colon
        [%(any)s]  +?             # followed by one or more
                                  #  of any valid character, but
                                  #  be conservative and take only
                                  #  what you need to....
    (?=                           # look-ahead non-consumptive assertion
            [%(punc)s]*           # either 0 or more punctuation
            (?:   [^%(any)s]      #  followed by a non-url char
                |                 #   or end of the string
                  $
            )
    )
    """ % {'urls' : urls,
           'any' : any,
           'punc' : punc }

url_re = re.compile(url, re.VERBOSE | re.MULTILINE)




candidates = scraperwiki.sqlite.select("* from pcc_candidates")
#candidates = []

if False:
    for police_area in police_areas:
        slug = police_area.replace(" ", "-").lower()
        area_url = area_page % slug
        print(area_url)
        tree = lxml.html.parse(area_url)
        for candidate_box in tree.xpath("//div[@class='related-candidate']"):
            try:
                candidate_image = candidate_box.xpath("./a/img/@src")[0]
            except IndexError:
                candidate_image = None

            candidate_name = candidate_box.xpath("./h4")[0].text_content().strip()
            
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            candidate_party = candidate_box.xpath("./p")[0].text_content().strip()
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            print "%s (%s)" % (candidate_name, candidate_party)
    
            data = {'candidate_url': candidate_url,
                'candidate_image_small': candidate_image,
                'candidate_name': candidate_name,
                'candidate_party': candidate_party,
                'police_area': slug}
    
            candidates.append(data)

print (len(candidates))
scraperwiki.sqlite.save(["candidate_url"], candidates, "pcc_candidates")

for candidate in candidates:
    print candidate['candidate_name']
    print "-" + candidate['candidate_url'][0:7] + "-"
    print ('unknown' in candidate['candidate_url'][0:7])
    if  (candidate['candidate_url'][0:7] == 'unknown'):
        continue

    if 'candidate_content' not in candidate:
        try:
            tree = lxml.html.parse(candidate['candidate_url'])
            content = lxml.html.tostring(tree.xpath("//div[@class='col12']")[0])
            candidate['candidate_content'] = content
        except:
            continue
    else:
        tree = lxml.html.parse(StringIO.StringIO(candidate['candidate_content']))

    if 'candidate_image_big' not in candidate:
        candidate_image_big = tree.xpath('//img[@class="attachment-candidate"]/@src')[0]
        candidate['candidate_image_big'] = candidate_image_big


    if candidate['candidate_content'] is not None:
        candidate['candidate_content_text'] = lxml.html.fromstring(candidate['candidate_content']).text_content()
    else:
        candidate['candidate_content'] = ""
        candidate['candidate_content_text'] = ""

    print(candidate['candidate_content'])
    print(candidate['candidate_content_text'])
    facebook = re.findall("www\.facebook\.com/([^ ]+)", candidate['candidate_content_text'])

    if len(facebook) != 0:
        candidate['facebook'] = "https://www.facebook.com/" + facebook[0]

    website = url_re.findall(candidate['candidate_content_text'])
    if len(website) != 0:
        websites = ""
        for wbs in website:
            websites = websites.join(wbs.join("\n"))
        candidate['website'] = websites
    
    try:
        candidate_en_email = tree.xpath("//a[@id='__cf_email__']/@class")[0]
    except:
        candidate_en_email = ""

    if candidate_en_email != "":
        a = candidate_en_email 
        s=''
        r = int(a[0:2],16)
        for j in xrange(2, len(a), 2):
            c = a[j:j+2]
            cstr = str(unichr(int(c,16)^r))
            s = s + cstr    
        candidate_email = s
    else:
        candidate_email = "" 


    candidate['email'] = candidate_email


    scraperwiki.sqlite.save(["candidate_url"], candidate, "pcc_candidates")


