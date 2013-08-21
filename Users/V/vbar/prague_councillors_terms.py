import lxml.html
import scraperwiki

base_url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html"

html = scraperwiki.scrape(base_url)
page = lxml.html.fromstring(html)
for per_select in page.xpath("//select[@name='periodId']"): # hopefully exactly one
    for per_opt in per_select.xpath("option"):
        opt_val = per_opt.xpath("@value")[0]
        if opt_val:
            data = { 'period_id': int(opt_val), 'period_desc': per_opt.text_content() }
            scraperwiki.sqlite.save(unique_keys=['period_id'], data=data)