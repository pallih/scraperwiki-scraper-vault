import scraperwiki
import re

sourcescraper = 'small_e-money_issuer_certificates_fsa_list'

scraperwiki.sqlite.attach(sourcescraper) 

lines = scraperwiki.sqlite.select('* from `small_e-money_issuer_certificates_fsa_list`.swdata')

print "<ol id='small_e-money_issuer_certificates_fsa_list'>"

for line in lines:
    if (line['issuer']):
        #time = re.sub("[^\d]", "", line['time'])
        print "<li class='small_e-money_issuer'><a href='http://opencorporates.com/search?q=" + line['issuer'] + "'>" +line['issuer'] + "</a></li>"

print "</ol>"
