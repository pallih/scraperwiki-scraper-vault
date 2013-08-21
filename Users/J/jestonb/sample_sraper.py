
import scraperwiki
html = scraperwiki.scrape("https://secure.sos.state.or.us/orestar/publicAccountSummary.do?filerId=931")
print scraperwiki.sqlite.show_tables()

