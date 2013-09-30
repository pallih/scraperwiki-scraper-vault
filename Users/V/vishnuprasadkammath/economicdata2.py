import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
import md5
 # allow everything to be written to br.set_handle_robots(False) # no robots br.set_handle_refresh(False)
br = mechanize.Browser()
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response=br.open("http://www.censusindia.gov.in/census_Data_2001/Census_Data_Online/Household_Population/Normal_Households_by_Household_Size.aspx")

print response

res=br.open("http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Census_Login_List.aspx?id=")
print res
import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
import md5
 # allow everything to be written to br.set_handle_robots(False) # no robots br.set_handle_refresh(False)
br = mechanize.Browser()
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response=br.open("http://www.censusindia.gov.in/census_Data_2001/Census_Data_Online/Household_Population/Normal_Households_by_Household_Size.aspx")

print response

res=br.open("http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Census_Login_List.aspx?id=")
print res
