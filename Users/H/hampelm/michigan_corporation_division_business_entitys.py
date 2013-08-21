# You got cookie.
# So share it maybe?
from bs4 import BeautifulSoup

import mechanize
from mechanize import ParseResponse, urlopen, urljoin

import re
import scraperwiki
import string


base = "http://www.dleg.state.mi.us/bcs_corp/"
search_page = "sr_corp.asp"
result_page = "dt_corp.asp"

# Next page link: rs_corp.asp?s_button=sname&v_search=a&hiddenField=&offset=40

# Get the main name search form
print urljoin(base, search_page)
main_page = urlopen(urljoin(base, search_page))
br = mechanize.Browser()
br.open(base)
forms = mechanize.ParseResponse(main_page, backwards_compat=False)
form = forms[0]
print form

# Search for something:
form.set_value("a", name="v_search")

br.open(form.click())



# Find all URLS that begin with 'dt_corp.asp'
# for letter in string.lowercase:
#     print letter

