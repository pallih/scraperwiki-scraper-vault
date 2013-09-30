import lxml.html
import scraperwiki

scraperwiki.sqlite.attach('ostrava_councillors_minutes', 'src')
done_vote = scraperwiki.sqlite.get_var('vote_no')
if done_vote:
    input = scraperwiki.sqlite.select("* from src.swdata where vote_no>%s order by vote_no" % done_vote)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by vote_no")

for rd in input:
    vote_no = rd['vote_no']
    url = rd['vote_url']
    html = scraperwiki.scrape(url)
    page = lxml.html.fromstring(html)

    deputy = None
    # going through rows doesn't work - some cells are outside...
    for td in page.xpath("//td"):
        clss = td.xpath("@class")        
        if len(clss) == 1:
            cls = clss[0]
            if cls == "deputy":
                # we could identify last name here, but the
                # post-processing expects whole names anyway...
                deputy = td.text_content().strip()
                if deputy and deputy[-1] == ':':
                    deputy = deputy[0:-1].strip()                
            elif cls == "cast":
                cast = td.text_content().strip()
                if deputy and cast:
                    data = { 'vote_no': vote_no, 'name': deputy, 'vote': cast }
                    scraperwiki.sqlite.save(unique_keys=['vote_no', 'name'], data=data)
                    deputy = None

    scraperwiki.sqlite.save_var('vote_no', vote_no)
import lxml.html
import scraperwiki

scraperwiki.sqlite.attach('ostrava_councillors_minutes', 'src')
done_vote = scraperwiki.sqlite.get_var('vote_no')
if done_vote:
    input = scraperwiki.sqlite.select("* from src.swdata where vote_no>%s order by vote_no" % done_vote)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by vote_no")

for rd in input:
    vote_no = rd['vote_no']
    url = rd['vote_url']
    html = scraperwiki.scrape(url)
    page = lxml.html.fromstring(html)

    deputy = None
    # going through rows doesn't work - some cells are outside...
    for td in page.xpath("//td"):
        clss = td.xpath("@class")        
        if len(clss) == 1:
            cls = clss[0]
            if cls == "deputy":
                # we could identify last name here, but the
                # post-processing expects whole names anyway...
                deputy = td.text_content().strip()
                if deputy and deputy[-1] == ':':
                    deputy = deputy[0:-1].strip()                
            elif cls == "cast":
                cast = td.text_content().strip()
                if deputy and cast:
                    data = { 'vote_no': vote_no, 'name': deputy, 'vote': cast }
                    scraperwiki.sqlite.save(unique_keys=['vote_no', 'name'], data=data)
                    deputy = None

    scraperwiki.sqlite.save_var('vote_no', vote_no)
