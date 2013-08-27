import scraperwiki
import mechanize
import re

# this page is essential :: http://blog.scraperwiki.com/2011/11/09/how-to-get-along-with-an-asp-webpage/

url = 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

html = response.read()
#print html



#eventArg = 'Page$' + str(pagenum)
br.select_form(name='aspnetForm')
br.form.set_all_readonly(False)
# I thought I might need these, but they generate an error 500
#br.find_control("ctl00$cmdLogin").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$Button1").disabled = True
br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$GridView1'
br['__EVENTARGUMENT'] = 'Page$79'
print br.form
response2 = br.submit()

html2 = response2.read()
print html2


import scraperwiki
import mechanize
import re

# this page is essential :: http://blog.scraperwiki.com/2011/11/09/how-to-get-along-with-an-asp-webpage/

url = 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

html = response.read()
#print html



#eventArg = 'Page$' + str(pagenum)
br.select_form(name='aspnetForm')
br.form.set_all_readonly(False)
# I thought I might need these, but they generate an error 500
#br.find_control("ctl00$cmdLogin").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$Button1").disabled = True
br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$GridView1'
br['__EVENTARGUMENT'] = 'Page$79'
print br.form
response2 = br.submit()

html2 = response2.read()
print html2


import scraperwiki
import mechanize
import re

# this page is essential :: http://blog.scraperwiki.com/2011/11/09/how-to-get-along-with-an-asp-webpage/

url = 'http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314'
br = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

html = response.read()
#print html



#eventArg = 'Page$' + str(pagenum)
br.select_form(name='aspnetForm')
br.form.set_all_readonly(False)
# I thought I might need these, but they generate an error 500
#br.find_control("ctl00$cmdLogin").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$Button1").disabled = True
br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$GridView1'
br['__EVENTARGUMENT'] = 'Page$79'
print br.form
response2 = br.submit()

html2 = response2.read()
print html2


