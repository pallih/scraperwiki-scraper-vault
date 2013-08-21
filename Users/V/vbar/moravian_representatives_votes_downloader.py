import scraperwiki

scraperwiki.sqlite.attach('moravian_representatives_minutes', 'src')
done_date = scraperwiki.sqlite.get_var('date1', None)
if done_date:
    input = scraperwiki.sqlite.select("* from src.swdata where date(date)>date('%s') order by date(date)" % done_date)
else:
    input = scraperwiki.sqlite.select("* from src.swdata order by date(date)")

old_date = None
for rd in input:
    url = rd['vote']
    date = rd['date']
    if not date:
        raise Exception("no date")

    html = scraperwiki.scrape(url)

    # strictly speaking, one key (i.e. url) should be enough, but the downstream
    # scraper will need the date & vote_no and it's easier making it read just one
    # table (especially considering that different tables might be out of sync)...
    data = { 'url': url, 'html': html, 'date': date, 'vote_no': rd['vote_no'] }
    scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    if old_date:
        if old_date != date:
            scraperwiki.sqlite.save_var('date1', old_date)
            old_date = date
    else:
        old_date = date

