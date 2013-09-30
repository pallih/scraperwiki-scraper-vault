import scraperwiki
import lxml.html
import itertools


pdf=scraperwiki.scrape("http://dump.tentacleriot.eu/2004ParliamentaryResults.pdf")
xml=scraperwiki.pdftoxml(pdf)
root=lxml.html.fromstring(xml)
print xml

def find_section(fn,nodes):
    return [i for i in itertools.takewhile(fn,nodes)]

def find_block(fn,nodes):
    r=find_section(fn,nodes)
    while r:
        yield r
        r=find_section(fn,nodes)

def tonumber(el):
    return int(el.text_content().strip().replace(",",""))

def extract_candidates(cnd):
    r=[i for i in itertools.islice(cnd,6)]
    while len(r)==6:
        yield r
        r=[i for i in itertools.islice(cnd,6)]
    

def get_regions(nodes):
    regions=find_block(lambda x: not (x.get("left")=="114") & (x.get("font")=="3"),nodes)
    regions.next() # drop first block
    for r in regions:
        region=r[0].text_content().title().strip()
        constituencies=find_block(lambda x: not (x.get("left")=="114") & (x.get("font")=="4"),(i for i in r)) #constituencies
        constituencies.next()
        for c in constituencies:
            constituency=c[0].text_content().title().strip()
            cd=[i for i in itertools.ifilter(lambda x: x.get("font")=="5",c[1:])]
            
            registered_voters=tonumber(cd[0])
            valid_votes=tonumber(cd[1])
            votes_cast=tonumber(cd[2])
            voter_turnout=cd[3].text_content()
            invalid_votes=tonumber(cd[4])
            candidates=extract_candidates(itertools.ifilter(lambda x: (x.get("font")=="6") or (x.get("font")=="7"),c))
            for candidate in candidates:
                candidate_data=[i.text_content() for i in candidate]
                keys=["Party","Name","Votes","Percent","Age","Sex","Constituency","Registered_Voters","Valid_Votes","Votes_Cast","Voter_Turnout",
                    "Invalid_Votes","Region"]
                cnd=dict(zip(keys,candidate_data+[constituency,registered_voters,valid_votes,votes_cast,voter_turnout,invalid_votes,region]))
                cnd["ukey"]="%s-%s"%(cnd["Name"],cnd["Constituency"])
                scraperwiki.sqlite.save(unique_keys=["ukey"],data=cnd)

            
            


tnodes=(i for i in root.cssselect("text"))
get_regions(tnodes)

import scraperwiki
import lxml.html
import itertools


pdf=scraperwiki.scrape("http://dump.tentacleriot.eu/2004ParliamentaryResults.pdf")
xml=scraperwiki.pdftoxml(pdf)
root=lxml.html.fromstring(xml)
print xml

def find_section(fn,nodes):
    return [i for i in itertools.takewhile(fn,nodes)]

def find_block(fn,nodes):
    r=find_section(fn,nodes)
    while r:
        yield r
        r=find_section(fn,nodes)

def tonumber(el):
    return int(el.text_content().strip().replace(",",""))

def extract_candidates(cnd):
    r=[i for i in itertools.islice(cnd,6)]
    while len(r)==6:
        yield r
        r=[i for i in itertools.islice(cnd,6)]
    

def get_regions(nodes):
    regions=find_block(lambda x: not (x.get("left")=="114") & (x.get("font")=="3"),nodes)
    regions.next() # drop first block
    for r in regions:
        region=r[0].text_content().title().strip()
        constituencies=find_block(lambda x: not (x.get("left")=="114") & (x.get("font")=="4"),(i for i in r)) #constituencies
        constituencies.next()
        for c in constituencies:
            constituency=c[0].text_content().title().strip()
            cd=[i for i in itertools.ifilter(lambda x: x.get("font")=="5",c[1:])]
            
            registered_voters=tonumber(cd[0])
            valid_votes=tonumber(cd[1])
            votes_cast=tonumber(cd[2])
            voter_turnout=cd[3].text_content()
            invalid_votes=tonumber(cd[4])
            candidates=extract_candidates(itertools.ifilter(lambda x: (x.get("font")=="6") or (x.get("font")=="7"),c))
            for candidate in candidates:
                candidate_data=[i.text_content() for i in candidate]
                keys=["Party","Name","Votes","Percent","Age","Sex","Constituency","Registered_Voters","Valid_Votes","Votes_Cast","Voter_Turnout",
                    "Invalid_Votes","Region"]
                cnd=dict(zip(keys,candidate_data+[constituency,registered_voters,valid_votes,votes_cast,voter_turnout,invalid_votes,region]))
                cnd["ukey"]="%s-%s"%(cnd["Name"],cnd["Constituency"])
                scraperwiki.sqlite.save(unique_keys=["ukey"],data=cnd)

            
            


tnodes=(i for i in root.cssselect("text"))
get_regions(tnodes)

