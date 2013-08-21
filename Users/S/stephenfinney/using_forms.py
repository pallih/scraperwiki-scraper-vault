import scraperwiki
import lxml.html
import mechanize

url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'

br = mechanize.Browser()
br.set_handle_robots(False)
response = br.open(url)

br.select_form(name="_ResultsState")
print br.form

br.form.set_all_readonly(False)

br["UTLIST_NORM_POSTED"] = "0"
br["UTLIST_PAGENUMBER"] = "2"

response = br.submit()
print response.read()import scraperwiki
import lxml.html
import mechanize

url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'

br = mechanize.Browser()
br.set_handle_robots(False)
response = br.open(url)

br.select_form(name="_ResultsState")
print br.form

br.form.set_all_readonly(False)

br["UTLIST_NORM_POSTED"] = "0"
br["UTLIST_PAGENUMBER"] = "2"

response = br.submit()
print response.read()