import scraperwiki

# URL is a value placeholder, called a "variable".
# All members have ID numbers. We're replacing them with "%s" here, 
# which is a placeholder.
URL = 'http://mzalendo.com/Members.Details.php?ID=%s'


# Now, we will take all numbers between 1 and 1000 and for each one,
# replace the %s in our address:
for i in range(1, 1000):    
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
    name_sections = document.cssselect('div#posts h1')

    # name_sections is now the list of sections of the page that contains 
    # the MPs name.

    # some pages do not contain info about an MP, so'we need to skip 
    # those:
    if not name_sections:
        # continue will go for the next number of our "for" loop.
        continue

    # we need to get all the text in the first (that's what "[0]" does) 
    # section, which requires a bit of magic (xpath is a way of searching
    # the document).
    name = name_sections[0].xpath('string()').strip()

    print i, "NAME", name

    # WEIRD PART - NOT DOCUMENTED YET.
    mp = {'i': i, 'name': name}
    links = document.cssselect('a')
    for link in links:
        address = link.get('href') or ''
        if 'Constituencies.Details' in address:
            mp['constituency'] = link.text
            mp['constituency_url'] = address
    scraperwiki.sqlite.save(unique_keys=['i'], data=mp)


import scraperwiki

# URL is a value placeholder, called a "variable".
# All members have ID numbers. We're replacing them with "%s" here, 
# which is a placeholder.
URL = 'http://mzalendo.com/Members.Details.php?ID=%s'


# Now, we will take all numbers between 1 and 1000 and for each one,
# replace the %s in our address:
for i in range(1, 1000):    
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
    name_sections = document.cssselect('div#posts h1')

    # name_sections is now the list of sections of the page that contains 
    # the MPs name.

    # some pages do not contain info about an MP, so'we need to skip 
    # those:
    if not name_sections:
        # continue will go for the next number of our "for" loop.
        continue

    # we need to get all the text in the first (that's what "[0]" does) 
    # section, which requires a bit of magic (xpath is a way of searching
    # the document).
    name = name_sections[0].xpath('string()').strip()

    print i, "NAME", name

    # WEIRD PART - NOT DOCUMENTED YET.
    mp = {'i': i, 'name': name}
    links = document.cssselect('a')
    for link in links:
        address = link.get('href') or ''
        if 'Constituencies.Details' in address:
            mp['constituency'] = link.text
            mp['constituency_url'] = address
    scraperwiki.sqlite.save(unique_keys=['i'], data=mp)


