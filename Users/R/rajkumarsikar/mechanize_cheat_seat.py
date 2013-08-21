import scraperwiki

# Blank Python
import mechanize 
br = mechanize.Browser()

br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False) 

br.open('http://agcensus.dacnet.nic.in/TalukCharacteristics.aspx') 
for form in br.forms(): print "Form name:", form.name 
print form
