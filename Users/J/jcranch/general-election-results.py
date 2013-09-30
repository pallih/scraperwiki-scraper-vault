"""
Results of the general election for the UK Parliament in 2005

Obtained from:
http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2006

Heavily documented for the benefit of Python novices interested in scraping.
"""

# standard library imports

# "datastore" is the scraperwiki builtin functionality for saving data records
# "scrape" is the builtin functionality for downloading stuff off the Internet
# "re" is the standard Python regular expression engine
from scraperwiki import datastore, scrape
import re



def main():
    url = "http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2005"

    # grab the HTML at that URL
    page = scrape(url)

    # make an empty list of constituencies; we'll add to it soon
    constituencies = []

    # this regular expression identifies links to webpages containing data on constituencies
    # the two parenthesised parts are "groups" and match the URL (group 0) and the constituency name (group 1)
    r = re.compile('<option value="(http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2005/[^>]*)">([^<]*)</option>')

    # we'll go through every match of that regular expression on the page
    # for every match, t is set to a "match object", which tells you about the way that r matches the given data
    # (and from which, in particular, you can extract the groups)
    for t in r.finditer(page):
        
        # HTML encodes ampersands as '&amp;'; let's decode that
        name = t.group(2).replace("&amp;","&")
        url = t.group(1)
        
        # now we know the name and URL, add it to the list!
        constituencies.append((name,url))

    # OK, so we've got a list of pairs consisting of a constituency name and a page URL. We need to process each one separately.
    for (name,url) in constituencies:
        subscrape(name,url)



def subscrape(name,url):
    "This scrapes data about one constituency"

    # produce a pretty text heading as a report
    s = "Now scraping: "+name
    print
    print s
    print "-"*len(s)
    
    # download the page
    page = scrape(url)

    # we need to make a key/value dictionary to store later on... we'll start by adding the two pieces of information we know already
    d = {"Constituency":name, "Electoral Commission URL":url}

    # this is a subroutine. It takes a match object, where group 0 is expected to be a data key and group 1 is expected to be its value
    # it saves that key/value pair in d, and then prints a report about it
    def process(m):
        a, b = m.groups()
        d[a] = b
        print "%s: %s"%(a,b)

    # we search for the title, which (as is visible from the example pages) tells us the winning candidate
    # then we use the subroutine above to carve it up
    r = re.compile('<h2>(Winning candidate): ([^<]*)</h2>')
    process(r.search(page))
    
    # we search for the other bits of miscellaneous data from the top of the page
    # whereas we expect only one title, we expect several such bits of data, so we need a loop
    r = re.compile('<p>([^:]*): ([^<]*)</p>')
    for m in r.finditer(page):
        process(m)
        
    # now make a big list of all table entries in the page
    r = re.compile('<td>([^<]*)</td>')
    l = list(r.findall(page))
    print l
    
    # we need to handle them five-at-a-time, since there's five columns
    # so as long as there are any left, we let the first five be the surname, initials, party, number of votes and vote pecentage
    while len(l)>0:
        surname = l[0]
        initials = l[1]
        party = l[2]
        if party=="Independent":
            # We need to rename the parties given as "Independent", because they're all independent!
            # This is really important since we could have two Independent candidates in the same constituency
            # ... if we didn't do this we'd overwrite the first with the data from the second
            # so we rename them in the form "J. W. Bloggs, Independent"
            party="%s %s, Independent"%(initials,surname)
        votes = l[3]
        percentage = l[4]
        print "%s %s (%s): %s votes (%s%%)"%(initials,surname,party,votes,percentage)

        # now we generate four key/value pairs with names like "Liberal Democrat surname", "Liberal Democrat initials", and so on
        d[party+" surname"] = surname
        d[party+" initials"] = initials
        d[party+" votes"] = votes
        d[party+" percentage"] = percentage
        
        # lastly we remove the first five entries of l since we've just processed them
        l = l[5:]

    # after all that, our record is complete! We can save it.
    # "unique_keys" are the set of keys that are "jointly primary": if we already had a record with the same primary keys it gets overwritten
    # with a lot of care, that's a really good thing: it means when the ScraperWiki server reruns the code every night,
    # it just freshens up and updates the data you already had rather than causing duplicates to pile up
    datastore.save(unique_keys=["Constituency"], data=d)

    
# last of all, we'd better make sure we run the main routine defined above!
main()"""
Results of the general election for the UK Parliament in 2005

Obtained from:
http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2006

Heavily documented for the benefit of Python novices interested in scraping.
"""

# standard library imports

# "datastore" is the scraperwiki builtin functionality for saving data records
# "scrape" is the builtin functionality for downloading stuff off the Internet
# "re" is the standard Python regular expression engine
from scraperwiki import datastore, scrape
import re



def main():
    url = "http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2005"

    # grab the HTML at that URL
    page = scrape(url)

    # make an empty list of constituencies; we'll add to it soon
    constituencies = []

    # this regular expression identifies links to webpages containing data on constituencies
    # the two parenthesised parts are "groups" and match the URL (group 0) and the constituency name (group 1)
    r = re.compile('<option value="(http://www.electoralcommission.org.uk/elections/results/general_elections/uk-general-election-2005/[^>]*)">([^<]*)</option>')

    # we'll go through every match of that regular expression on the page
    # for every match, t is set to a "match object", which tells you about the way that r matches the given data
    # (and from which, in particular, you can extract the groups)
    for t in r.finditer(page):
        
        # HTML encodes ampersands as '&amp;'; let's decode that
        name = t.group(2).replace("&amp;","&")
        url = t.group(1)
        
        # now we know the name and URL, add it to the list!
        constituencies.append((name,url))

    # OK, so we've got a list of pairs consisting of a constituency name and a page URL. We need to process each one separately.
    for (name,url) in constituencies:
        subscrape(name,url)



def subscrape(name,url):
    "This scrapes data about one constituency"

    # produce a pretty text heading as a report
    s = "Now scraping: "+name
    print
    print s
    print "-"*len(s)
    
    # download the page
    page = scrape(url)

    # we need to make a key/value dictionary to store later on... we'll start by adding the two pieces of information we know already
    d = {"Constituency":name, "Electoral Commission URL":url}

    # this is a subroutine. It takes a match object, where group 0 is expected to be a data key and group 1 is expected to be its value
    # it saves that key/value pair in d, and then prints a report about it
    def process(m):
        a, b = m.groups()
        d[a] = b
        print "%s: %s"%(a,b)

    # we search for the title, which (as is visible from the example pages) tells us the winning candidate
    # then we use the subroutine above to carve it up
    r = re.compile('<h2>(Winning candidate): ([^<]*)</h2>')
    process(r.search(page))
    
    # we search for the other bits of miscellaneous data from the top of the page
    # whereas we expect only one title, we expect several such bits of data, so we need a loop
    r = re.compile('<p>([^:]*): ([^<]*)</p>')
    for m in r.finditer(page):
        process(m)
        
    # now make a big list of all table entries in the page
    r = re.compile('<td>([^<]*)</td>')
    l = list(r.findall(page))
    print l
    
    # we need to handle them five-at-a-time, since there's five columns
    # so as long as there are any left, we let the first five be the surname, initials, party, number of votes and vote pecentage
    while len(l)>0:
        surname = l[0]
        initials = l[1]
        party = l[2]
        if party=="Independent":
            # We need to rename the parties given as "Independent", because they're all independent!
            # This is really important since we could have two Independent candidates in the same constituency
            # ... if we didn't do this we'd overwrite the first with the data from the second
            # so we rename them in the form "J. W. Bloggs, Independent"
            party="%s %s, Independent"%(initials,surname)
        votes = l[3]
        percentage = l[4]
        print "%s %s (%s): %s votes (%s%%)"%(initials,surname,party,votes,percentage)

        # now we generate four key/value pairs with names like "Liberal Democrat surname", "Liberal Democrat initials", and so on
        d[party+" surname"] = surname
        d[party+" initials"] = initials
        d[party+" votes"] = votes
        d[party+" percentage"] = percentage
        
        # lastly we remove the first five entries of l since we've just processed them
        l = l[5:]

    # after all that, our record is complete! We can save it.
    # "unique_keys" are the set of keys that are "jointly primary": if we already had a record with the same primary keys it gets overwritten
    # with a lot of care, that's a really good thing: it means when the ScraperWiki server reruns the code every night,
    # it just freshens up and updates the data you already had rather than causing duplicates to pile up
    datastore.save(unique_keys=["Constituency"], data=d)

    
# last of all, we'd better make sure we run the main routine defined above!
main()