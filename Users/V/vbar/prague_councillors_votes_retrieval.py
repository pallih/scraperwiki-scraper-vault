import lxml.html
import scraperwiki

scraperwiki.sqlite.attach('prague_councillors_downloader_1', 'src')
done_idx = scraperwiki.sqlite.get_var('idx1', 0)
input = scraperwiki.sqlite.select("* from src.swdata order by period_id, voting_id limit -1 offset " + str(done_idx))

for rd in input:
    page = lxml.html.fromstring(rd['html'])
    for tr in page.xpath("//table/tbody/tr"):
        tds = tr.xpath("td")
        name = tds[0].text_content()
        vote = tds[1].text_content()
        data = { 'period_id': rd['period_id'],
            'voting_id': rd['voting_id'],
            'name': name.strip(),
            'vote': vote.strip() }
        scraperwiki.sqlite.save(unique_keys=['period_id', 'voting_id', 'name'], data=data)

    done_idx += 1
    scraperwiki.sqlite.save_var('idx1', done_idx)

