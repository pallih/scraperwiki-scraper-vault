import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
import string

url="http://www.censusindia.gov.in/Census_Data_2001/Census_Data_Online/Online_Migration/By_Place_of_Birth.aspx"

state_count=0
c=1

#run loop for all state and union territories
while state_count<1:
    data=[]
    count=0
    l_c=0
    row=[]

    # code added by Usha Nair
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)
    VAR1 = response.read() #reads the source file for the web page
    br.select_form(name="Form1")
    br.set_all_readonly(False)


    br["rdbState[checked]"]='checked'
    br["__EVENTTARGET"] = 'rdbState'
    br["__EVENTARGUMENT"] = 'checked'

    #br.find_control("btnSearch").disabled = True
    response = br.submit()
    VAR2 = response.read() # source code after submitting show all
    print(VAR2)
    # Usha Nair till here

    state_count+=1

#new internet code

