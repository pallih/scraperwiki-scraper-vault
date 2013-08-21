import scraperwiki,re
from scraperwiki import sqlite
from datetime import date
def _(bank,url,pattern):
    sqlite.save(unique_keys=["bank","date"],data={'bank':bank,'apy':re.search(pattern,scraperwiki.scrape(url)).group(1),'date':date.today().isoformat()})
    return _
_\
("ING","https://home.capitalone360.com/js/accounttype.js","type_3000_apy='([^']+)'")\
("HSBC","https://www.us.hsbc.com/1/2/home/personal-banking/deposit-rates","(?s)Online Savings.*?>\s*([0-9.]+)\s*%")\
("Ally","http://www.ally.com/rss/rates.xml","(?s)Online Savings.*?>\s*[0-9.]+\s*%.*?>\s*([0-9.]+)\s*%")\
("FNBO Savings","https://www.fnbodirect.com/01d/html/en/",'(?s)<span class="bubblerate_current">Our OSA.*?([0-9.]+)')\
("FNBO Checking","https://www.fnbodirect.com/01d/html/en/",'(?s)<span class="bubblerate_current">Online BillPay.*?([0-9.]+)')\
("AMEX High Yield Savings","http://personalsavings.americanexpress.com/javascripts/rates.json","High Yield Savings.*?apy:([0-9.]+)")\
("CIT Bank","https://www.bankoncit.com/product-savings.htm","(?s)\\$100\s*</td>.*?([0-9.]+)%")\
("Barclays","https://www.banking.barclaysus.com/online-savings.html",'<div class="mainrate">([0-9.]+)</div>')\

