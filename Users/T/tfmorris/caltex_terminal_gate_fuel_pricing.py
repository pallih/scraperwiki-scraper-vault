import scraperwiki
import lxml.html
from datetime import datetime

URL='http://www.caltex.com.au/LatestNews/FuelPricing/Pages/TerminalGatePricing.aspx'
FUELS=['Diesel']
TERMINALS=['Devonport']

def main():
    index_html = scraperwiki.scrape(URL)
    index = lxml.html.fromstring(index_html)
    # '//*[@id="main"]/div[2]/div[2]/table/tbody/tr[10]/td[7]'
    dates = index.cssselect('div.EffectiveDates')
    print 'Effective Dates: %s\n' % dates[0].text_content()
    for terminal in TERMINALS:
        for fuel in FUELS:
            for date in ['Current','Previous']:
                price = index.cssselect('td[headers="%s %s-%s %s"]' % (fuel,fuel,date,terminal))[0].text_content()
                print '%s %s %s: %s' % (fuel,terminal, date, price)

main()

