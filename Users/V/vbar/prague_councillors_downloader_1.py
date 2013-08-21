import re
import scraperwiki

scraperwiki.sqlite.attach('prague_councillors_resolutions', 'src')
done_idx = scraperwiki.sqlite.get_var('idx', 0)
input = scraperwiki.sqlite.select("* from src.swdata order by period_id, resolution limit -1 offset " + str(done_idx))

idx = done_idx
for rd in input:
    raw_url = rd['resolution']
    period_id = rd['period_id']
    match = re.search(r'votingId=(\d+)&size=$', raw_url)
    if match:
        voting_id = int(match.group(1))
        url = raw_url + "500" # should be enough to suppress paging
        html = scraperwiki.scrape(url)

        # again including columns which aren't strictly necessary        
        data = { 'url': url, 'html': html, 'period_id': period_id, 'voting_id': voting_id }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    else:
        raise Exception("unexpected url " + raw_url)

    idx += 1
    scraperwiki.sqlite.save_var('idx', idx)

