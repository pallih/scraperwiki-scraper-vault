import lxml.html
import re
import scraperwiki

scraperwiki.sqlite.attach('brno_councillors_protocols', 'src')

summary_cell = re.compile(r'(?:tomno|Ano|Ne|Nehlasoval):\s*\d+')

def is_summary_row(tds):
    for td in tds:
        if summary_cell.search(td.text_content()):
            return True

    return False

def get_vote_no(page):
    vote_no = None
    for p in page.xpath("//p[@class='header']"):
        match = re.search(r'Hlasov\D+(\d+)', p.text_content())
        if match:
            n = int(match.group(1))
            if vote_no:
                if vote_no != n:
                    raise Exception("vote_no mismatch")
            else:
                vote_no = n

    if not vote_no:
        raise Exception("vote_no not found")

    return vote_no

done_date = scraperwiki.sqlite.get_var('date1')
if done_date:
    print "date1=", done_date
    input = scraperwiki.sqlite.select("* from src.swdata where date>date(%s) order by date" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date")

for rd in input:
    date = rd['date']
    if done_date and (date < done_date): # the select above should limit the dates but doesn't...
        print "skipping", date
        continue

    base_url = rd['protocol']
    html = scraperwiki.scrape(base_url)
    page = lxml.html.fromstring(html)
    vote_no = get_vote_no(page)
    for tr in page.xpath("//table/tr"):
        tds = tr.xpath("td")
        if (len(tds) == 6) and not is_summary_row(tds):
            i = 0
            while i < 6:
                club_name = tds[i].text_content().strip()
                if club_name and club_name[-1] == ':':
                    club_name = club_name[0:-1].strip()
                
                vote = tds[i + 1].text_content().strip()

                if club_name and vote:
                    data = { 'date': date,
                        'vote_no': vote_no,
                        'club_name': club_name,
                        'vote': vote }
                    scraperwiki.sqlite.save(unique_keys=['date', 'vote_no', 'club_name'], data=data)

                i += 2

    if not done_date:
        done_date = date
    else:
        if date != done_date:            
            scraperwiki.sqlite.save_var('date1', done_date)
            done_date = date

