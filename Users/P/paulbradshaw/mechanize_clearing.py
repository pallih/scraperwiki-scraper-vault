import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://clearing.ucas.com'
startpage = '/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
combined = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
cache_url = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eHp9VmKNtR1XQeajAzVNZdD9eqG-UH_O/HAHTpage/cl_search.Hssearchh.run'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

html = scraperwiki.scrape(combined)
print html

root = lxml.html.fromstring(html)

links = root.cssselect('FONT a') # get all the <a> tags within <FONT>
for li in links:
    link = li.attrib.get('href')
    print link
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    response =  br.open(base_url+link)
    # print "Page:", response.read()
    print "About to get forms..."
    forms = br.forms() # This triggers a ParseError
    print "Got forms."
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="form0")
    print "Selected form"
    # print br.form
    response = br.submit()
    html = response.read()
    # print html

# <DIV CLASS="f"><FONT face="Arial, Helvetica, sans-serif" size="-1">Please
 #           select the vacancies you are interested in</FONT></DIV>
  #        <DIV CLASS="f">
   #         <DIV><FONT face="Arial, Helvetica, sans-serif" size="+0"><BR>
    #          <A href="/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eMphVmKV9lZlrAajA9cVXlD9sCw-UMJH/HAHTpage/cl_search.Hssearchh.run" ><FONT color="#ff0000">Course Vacancies for Home/EU Applicants</FONT></A></FONT></DIV>



import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://clearing.ucas.com'
startpage = '/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
combined = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
cache_url = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eHp9VmKNtR1XQeajAzVNZdD9eqG-UH_O/HAHTpage/cl_search.Hssearchh.run'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

html = scraperwiki.scrape(combined)
print html

root = lxml.html.fromstring(html)

links = root.cssselect('FONT a') # get all the <a> tags within <FONT>
for li in links:
    link = li.attrib.get('href')
    print link
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    response =  br.open(base_url+link)
    # print "Page:", response.read()
    print "About to get forms..."
    forms = br.forms() # This triggers a ParseError
    print "Got forms."
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="form0")
    print "Selected form"
    # print br.form
    response = br.submit()
    html = response.read()
    # print html

# <DIV CLASS="f"><FONT face="Arial, Helvetica, sans-serif" size="-1">Please
 #           select the vacancies you are interested in</FONT></DIV>
  #        <DIV CLASS="f">
   #         <DIV><FONT face="Arial, Helvetica, sans-serif" size="+0"><BR>
    #          <A href="/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eMphVmKV9lZlrAajA9cVXlD9sCw-UMJH/HAHTpage/cl_search.Hssearchh.run" ><FONT color="#ff0000">Course Vacancies for Home/EU Applicants</FONT></A></FONT></DIV>



import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://clearing.ucas.com'
startpage = '/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
combined = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
cache_url = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eHp9VmKNtR1XQeajAzVNZdD9eqG-UH_O/HAHTpage/cl_search.Hssearchh.run'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

html = scraperwiki.scrape(combined)
print html

root = lxml.html.fromstring(html)

links = root.cssselect('FONT a') # get all the <a> tags within <FONT>
for li in links:
    link = li.attrib.get('href')
    print link
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    response =  br.open(base_url+link)
    # print "Page:", response.read()
    print "About to get forms..."
    forms = br.forms() # This triggers a ParseError
    print "Got forms."
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="form0")
    print "Selected form"
    # print br.form
    response = br.submit()
    html = response.read()
    # print html

# <DIV CLASS="f"><FONT face="Arial, Helvetica, sans-serif" size="-1">Please
 #           select the vacancies you are interested in</FONT></DIV>
  #        <DIV CLASS="f">
   #         <DIV><FONT face="Arial, Helvetica, sans-serif" size="+0"><BR>
    #          <A href="/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eMphVmKV9lZlrAajA9cVXlD9sCw-UMJH/HAHTpage/cl_search.Hssearchh.run" ><FONT color="#ff0000">Course Vacancies for Home/EU Applicants</FONT></A></FONT></DIV>



import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://clearing.ucas.com'
startpage = '/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
combined = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
cache_url = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eHp9VmKNtR1XQeajAzVNZdD9eqG-UH_O/HAHTpage/cl_search.Hssearchh.run'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

html = scraperwiki.scrape(combined)
print html

root = lxml.html.fromstring(html)

links = root.cssselect('FONT a') # get all the <a> tags within <FONT>
for li in links:
    link = li.attrib.get('href')
    print link
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    response =  br.open(base_url+link)
    # print "Page:", response.read()
    print "About to get forms..."
    forms = br.forms() # This triggers a ParseError
    print "Got forms."
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="form0")
    print "Selected form"
    # print br.form
    response = br.submit()
    html = response.read()
    # print html

# <DIV CLASS="f"><FONT face="Arial, Helvetica, sans-serif" size="-1">Please
 #           select the vacancies you are interested in</FONT></DIV>
  #        <DIV CLASS="f">
   #         <DIV><FONT face="Arial, Helvetica, sans-serif" size="+0"><BR>
    #          <A href="/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eMphVmKV9lZlrAajA9cVXlD9sCw-UMJH/HAHTpage/cl_search.Hssearchh.run" ><FONT color="#ff0000">Course Vacancies for Home/EU Applicants</FONT></A></FONT></DIV>



import scraperwiki
import lxml.html
import mechanize 

# global settings

base_url = 'http://clearing.ucas.com'
startpage = '/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
combined = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run'
cache_url = 'http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eHp9VmKNtR1XQeajAzVNZdD9eqG-UH_O/HAHTpage/cl_search.Hssearchh.run'

#scrape page into new object: 'html'
#html = scraperwiki.scrape(base_url)

html = scraperwiki.scrape(combined)
print html

root = lxml.html.fromstring(html)

links = root.cssselect('FONT a') # get all the <a> tags within <FONT>
for li in links:
    link = li.attrib.get('href')
    print link
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    response =  br.open(base_url+link)
    # print "Page:", response.read()
    print "About to get forms..."
    forms = br.forms() # This triggers a ParseError
    print "Got forms."
    print "All forms:", [ form.name  for form in br.forms() ]
    br.select_form(name="form0")
    print "Selected form"
    # print br.form
    response = br.submit()
    html = response.read()
    # print html

# <DIV CLASS="f"><FONT face="Arial, Helvetica, sans-serif" size="-1">Please
 #           select the vacancies you are interested in</FONT></DIV>
  #        <DIV CLASS="f">
   #         <DIV><FONT face="Arial, Helvetica, sans-serif" size="+0"><BR>
    #          <A href="/cgi-bin/hsrun/clv02/cl_search12/StateId/E0eMphVmKV9lZlrAajA9cVXlD9sCw-UMJH/HAHTpage/cl_search.Hssearchh.run" ><FONT color="#ff0000">Course Vacancies for Home/EU Applicants</FONT></A></FONT></DIV>



