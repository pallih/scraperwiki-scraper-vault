import scraperwiki
 
# URL is a value placeholder, called a "variable".
# All members have ID numbers. We're replacing them with "%s" here, 
# which is a placeholder.
URL = 'http://news.bbc.co.uk/democracylive/hi/representatives/profiles/%d.stm'
 
 
# Now, we will take all numbers between 1 and 1000 and for each one,
# replace the %s in our address:
for i in range(27106, 34000):    
    # Now, because of the "for", all code indented by one
    # tab space will be run for each of the numbers.
    # "i" will be a number between 1 and 1000, so mp_url will contain 
    # the URL with "%s" replaced by the value of "i".
    mp_url = URL % i
    
    # We can now load an external utility that will download and 
    # interpret web pages for us.
    from lxml import html
    from urllib import urlopen
    fh = urlopen(mp_url)
    document = html.parse(fh).getroot()
 
    # Now, we'll use a special language to find particular sections in 
    # the page:
    name_sections = document.cssselect('span.fn, li.li-c span, li.li-e span')
 
    # name_sections is now the list of sections of the page that contains 
    # the MPs name.
 
    # some pages do not contain info about an MP, so'we need to skip 
    # those:
    if not name_sections or "Lord" not in name_sections[0].text:
        continue
#    elif "Baroness" not in name_sections[0].text:
#        continue
#    elif "Lord" not in name_sections[0].text:
#        continue
    elif "Baroness" in name_sections[0].text or "Lord" in name_sections[0].text:
        record = {}
        record['Name'] = name_sections[0].text.strip()
        if (len(name_sections) > 0):
            for j in range(1, len(name_sections)):
            
                record['%d' % j] = name_sections[j].text
        #record['b'] = name_sections[2].text
        #record['c'] = name_sections[3].text
    scraperwiki.sqlite.save(['Name'], record)
    print record, '------------'import scraperwiki
 
# URL is a value placeholder, called a "variable".
# All members have ID numbers. We're replacing them with "%s" here, 
# which is a placeholder.
URL = 'http://news.bbc.co.uk/democracylive/hi/representatives/profiles/%d.stm'
 
 
# Now, we will take all numbers between 1 and 1000 and for each one,
# replace the %s in our address:
for i in range(27106, 34000):    
    # Now, because of the "for", all code indented by one
    # tab space will be run for each of the numbers.
    # "i" will be a number between 1 and 1000, so mp_url will contain 
    # the URL with "%s" replaced by the value of "i".
    mp_url = URL % i
    
    # We can now load an external utility that will download and 
    # interpret web pages for us.
    from lxml import html
    from urllib import urlopen
    fh = urlopen(mp_url)
    document = html.parse(fh).getroot()
 
    # Now, we'll use a special language to find particular sections in 
    # the page:
    name_sections = document.cssselect('span.fn, li.li-c span, li.li-e span')
 
    # name_sections is now the list of sections of the page that contains 
    # the MPs name.
 
    # some pages do not contain info about an MP, so'we need to skip 
    # those:
    if not name_sections or "Lord" not in name_sections[0].text:
        continue
#    elif "Baroness" not in name_sections[0].text:
#        continue
#    elif "Lord" not in name_sections[0].text:
#        continue
    elif "Baroness" in name_sections[0].text or "Lord" in name_sections[0].text:
        record = {}
        record['Name'] = name_sections[0].text.strip()
        if (len(name_sections) > 0):
            for j in range(1, len(name_sections)):
            
                record['%d' % j] = name_sections[j].text
        #record['b'] = name_sections[2].text
        #record['c'] = name_sections[3].text
    scraperwiki.sqlite.save(['Name'], record)
    print record, '------------'