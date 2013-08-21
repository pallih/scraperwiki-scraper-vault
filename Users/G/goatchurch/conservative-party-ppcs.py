# Target webpage http://www.conservatives.com/People/Prospective%20Parliamentary%20Candidates.aspx?&by=All
# no longer exists

import scraperwiki
import re
import urlparse


# main function
def Main():
    candidatelist = CandidateList()
    for i, (lname, lconstituency, url) in enumerate(candidatelist):
        print (i, lname, lconstituency)
        if lconstituency:
            data = ParseSingleCandidate(lname, lconstituency, url)
            scraperwiki.datastore.save(unique_keys=["constituency", "name"], data=data)
        else:
            print "skipping", lname


def SimplifyHTML(t):
    t = re.sub("<p>", "NEWLINE", t)
    t = re.sub("\s*</li>", "; ", t)
    t = re.sub("<h3.*?>(.*)</h3>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("<h2>(.*)</h2>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t)
    return t.strip()
                          
                          
def DescParse(d):
    mdp = re.match("(MP|Member of Parliament|Parliamentary Candidate) for (.*)$", d)
    if not mdp:
        print "Does not match desc: " + d
        return None, None
    k, v = mdp.group(1), re.sub(" &amp; ", " and ", mdp.group(2))
    if k == "MP" or k == "Member of Parliament":
        k = "MP for"
    elif k == "Parliamentary Candidate":
        k = "constituency"
        v = RegularizeConstituency(v)
        if not v:
            print "Missing con", v
    return k, v


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
def RegularizeConstituency(lcon):
    lcon = re.sub(",", "", lcon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    return twfyconstituencies.get(lcon.lower())


def ParseSingleCandidate(lname, lconstituency, url):
    contents = scraperwiki.scrape(url)
    name = re.search('<div class="main-txt"><h1>(.*?)</h1>', contents).group(1)
    params = { }    

    # one or two positions are limited per candidate, except Alun Cairns where there is a mistake
    # luckily they list both current and future seat for incumbants
    h2contents = re.search('(?s)<h2>(.*?)</h2>', contents).group(1)
    for h2br in h2contents.split("<br>"):
        if h2br:
            k, v = DescParse(h2br)
            if k:
                params[k] = v
    assert params or name == "Alun Cairns"   # he is a welsh assembly member
    params["name"] = name
    
    #name = "".join(maintxt.h1.contents)     # h1 contains the name
    #soup = reading.soup()   # get the text loaded into a BeautifulSoup object
    #maintxt = soup.find("div", "main-txt")  # pull out the div containing the text
    #h2contents = maintxt.h2.contents        # h2 contains positions separated by <br/>
    #h3contents = maintxt.h3.contents
    #if h3contents:
    #    print "*****", ss(h3contents)       # h3 rarely used


    # extract the email and webpage links for the candidate
    #<a class="bld" href="mailto:dorriesn@parliament.uk">dorriesn@parliament.uk</a>
    memail = re.search('<a class="bld" href="mailto:([^"]*)">(.*?)</a>', contents)
    if memail:
        assert memail.group(1) == memail.group(2), ss(memail.group(0))
        params["email"] = memail.group(1)
    mweb = re.search('Web:\s*<a class="bld" href="(http://[^"]*)">(?:http://)?(.*?)</a>', contents)
    if mweb:
        assert mweb.group(1) == mweb.group(2), ss(mweb.group(0))
        params["web"] = mweb.group(1)
        
    mimage = re.search('<div class="personImage"><img src="(.*?)"', contents)
    if mimage:
        params["image"] = urlparse.urljoin(url, re.sub(" ", "%20", mimage.group(1)))

    params["url"] = url
    
    mbio = re.search('(?s)(<div class="personBody">.*?)<div class="rightcol">', contents)
    assert mbio, name
    params["bio"] = SimplifyHTML(mbio.group(1))
    #paras = re.findall('(?s)<(?:h2|p|li)>(.*?)</(?:h2|p|li)>', mbio.group(1))
    
    if "constituency" not in params:
        assert lconstituency == "Vale of Glamorgan"
        params["constituency"] = lconstituency
        
    # should add paras into the output
    return params


def CandidateList():
    urli = "http://www.conservatives.com/People/Prospective%20Parliamentary%20Candidates.aspx?&by=All"
    conservativeindex = scraperwiki.scrape(urli)

    # extract the number for verification
    mcandidatecount = re.search("There are currently (\d+) Prospective Parliamentary Candidates", conservativeindex)
    assert mcandidatecount, "Didn't find candidate count all index page"
    
    mtable = re.search('(?si)<table summary="Table of Conservative MPs and their constituencies".*?>(.*?)</table>', conservativeindex)
    assert mtable, "Didn't find table summary"
    
    rows = re.findall("(?si)<tr.*?>(.*?)</tr>", mtable.group(1))
    headrow = [ hcol.strip()  for hcol in re.findall("(?si)<th>(.*?)</th>", rows[0]) ]
    #print headrow
    assert headrow == ["Name", "Constituency"], "Head mismatch: " + rows[0]
    
    assert len(rows) - 1 == int(mcandidatecount.group(1)), "Reported rows mismatch"

    # loop through each row
    candidatelist = [ ]
    for row in rows[1:]:
        # <td><a href="/People/Prospective_Parliamentary_Candidates/Aldous_Peter.aspx">Peter Aldous</a></td><td>Waveney</td>
        mrow = re.match('<td><a href="(/People/.*?)">(.*?)</a></td><td>(.*?)</td>', row)
        lurl = mrow.group(1)
        name = mrow.group(2)
        constituency = re.sub(" (?:&amp;|&) ", " and ", mrow.group(3))
        urlp = urlparse.urljoin(urli, lurl)

        #text = scraperwiki.scrape(url=urlp)
        #print name, urlp
        candidatelist.append((name, constituency, urlp))
    return candidatelist

Main()
