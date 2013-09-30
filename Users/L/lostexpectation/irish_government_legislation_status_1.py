import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


# The URLs we're going to scrape:
url = "http://www.rte.ie/news/election2011/newtds.html"


html = scraperwiki.scrape(url)

# http://www.taoiseach.gov.ie/eng/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html SECTION A - Lists 23 Bills which the Government expect to publish from the start of the Dáil session up to the beginning of the next session
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_B1.html SECTION B - Lists 13 Bills in respect of which Heads of Bills have been approved by Government and of which texts are being prepared
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_C11.html SECTION C - Lists 55 Bills in respect of which heads have yet to be approved by Government
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_D1.html SECTION D - Lists 25 Bills which are currently before the Dáil or Seanad
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_E1.html SECTION E - Lists 113 Bills which were enacted since the Government came to office on 14th June, 2007
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_F1.html SECTION F - Lists 121 Bills which were published since the Government came to office on 14th June, 2007

# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.

# def gettext(html):
#    """Return the text within html, removing any HTML tags i
#    cleaned = re.sub('<.*?>', '', html)  # remove tags
#    cleaned = ' '.join(cleaned.split())  # collapse whitespace
#    return cleaned

#text = scraperwiki.scrape(url)



soup = BeautifulSoup(html)


#rows = re.findall('(?si)<tr[^>]*>(.*?)</tr>', text)
# <td valign="top">Forestry Bill</td><td valign="top">To reform and update the legislative framework relating to forestry in order to support the development of a modern forestry sector, which enshrines #the principles of sustainable forest management and protection of the environment<br /><br /></td></tr><tr>
#for row in rows:

#td valign="top">Veterinary Practice (Amendment) Bill</td><td valign="top">To enable the Minister to make regulations providing that specified procedures carried out on animals are not restricted to registered veterinary practitioners or registered veterinary nurses and to make a number of technical improvements to the Act in light of experience of operation<br /><br /></td></tr><tr><td colspan="3"><strong>Communications Energy and Natural Resources</strong></td></tr>

trs = soup.findAll('tr') 
for tr in trs:
    if tr.find(colspan="3"):
        continue
#    elif tr.contents[1].contents[0]==" Name Of Company ":
#        continue
    else:
        number, bill, desc = tr.contents[0].content, tr.contents[1].content, tr.contents[2].content

    #dept = re.search('<td colspan="3"><strong>(.*?)</strong></td>', row)
    #if dept:
    #    deptb = dept
    
    
        
      #  deptb, number, bill, desc  = None, None, None, None    
    





    #print deptb, number, bill, desc
    data = {'number': number,  'bill': bill, 'desc': desc } #'deptb':deptb, 
    scraperwiki.sqlite.save(['number'], data)   
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


# The URLs we're going to scrape:
url = "http://www.rte.ie/news/election2011/newtds.html"


html = scraperwiki.scrape(url)

# http://www.taoiseach.gov.ie/eng/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html SECTION A - Lists 23 Bills which the Government expect to publish from the start of the Dáil session up to the beginning of the next session
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_B1.html SECTION B - Lists 13 Bills in respect of which Heads of Bills have been approved by Government and of which texts are being prepared
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_C11.html SECTION C - Lists 55 Bills in respect of which heads have yet to be approved by Government
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_D1.html SECTION D - Lists 25 Bills which are currently before the Dáil or Seanad
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_E1.html SECTION E - Lists 113 Bills which were enacted since the Government came to office on 14th June, 2007
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_F1.html SECTION F - Lists 121 Bills which were published since the Government came to office on 14th June, 2007

# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.

# def gettext(html):
#    """Return the text within html, removing any HTML tags i
#    cleaned = re.sub('<.*?>', '', html)  # remove tags
#    cleaned = ' '.join(cleaned.split())  # collapse whitespace
#    return cleaned

#text = scraperwiki.scrape(url)



soup = BeautifulSoup(html)


#rows = re.findall('(?si)<tr[^>]*>(.*?)</tr>', text)
# <td valign="top">Forestry Bill</td><td valign="top">To reform and update the legislative framework relating to forestry in order to support the development of a modern forestry sector, which enshrines #the principles of sustainable forest management and protection of the environment<br /><br /></td></tr><tr>
#for row in rows:

#td valign="top">Veterinary Practice (Amendment) Bill</td><td valign="top">To enable the Minister to make regulations providing that specified procedures carried out on animals are not restricted to registered veterinary practitioners or registered veterinary nurses and to make a number of technical improvements to the Act in light of experience of operation<br /><br /></td></tr><tr><td colspan="3"><strong>Communications Energy and Natural Resources</strong></td></tr>

trs = soup.findAll('tr') 
for tr in trs:
    if tr.find(colspan="3"):
        continue
#    elif tr.contents[1].contents[0]==" Name Of Company ":
#        continue
    else:
        number, bill, desc = tr.contents[0].content, tr.contents[1].content, tr.contents[2].content

    #dept = re.search('<td colspan="3"><strong>(.*?)</strong></td>', row)
    #if dept:
    #    deptb = dept
    
    
        
      #  deptb, number, bill, desc  = None, None, None, None    
    





    #print deptb, number, bill, desc
    data = {'number': number,  'bill': bill, 'desc': desc } #'deptb':deptb, 
    scraperwiki.sqlite.save(['number'], data)   
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


# The URLs we're going to scrape:
url = "http://www.rte.ie/news/election2011/newtds.html"


html = scraperwiki.scrape(url)

# http://www.taoiseach.gov.ie/eng/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html SECTION A - Lists 23 Bills which the Government expect to publish from the start of the Dáil session up to the beginning of the next session
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_B1.html SECTION B - Lists 13 Bills in respect of which Heads of Bills have been approved by Government and of which texts are being prepared
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_C11.html SECTION C - Lists 55 Bills in respect of which heads have yet to be approved by Government
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_D1.html SECTION D - Lists 25 Bills which are currently before the Dáil or Seanad
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_E1.html SECTION E - Lists 113 Bills which were enacted since the Government came to office on 14th June, 2007
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_F1.html SECTION F - Lists 121 Bills which were published since the Government came to office on 14th June, 2007

# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.

# def gettext(html):
#    """Return the text within html, removing any HTML tags i
#    cleaned = re.sub('<.*?>', '', html)  # remove tags
#    cleaned = ' '.join(cleaned.split())  # collapse whitespace
#    return cleaned

#text = scraperwiki.scrape(url)



soup = BeautifulSoup(html)


#rows = re.findall('(?si)<tr[^>]*>(.*?)</tr>', text)
# <td valign="top">Forestry Bill</td><td valign="top">To reform and update the legislative framework relating to forestry in order to support the development of a modern forestry sector, which enshrines #the principles of sustainable forest management and protection of the environment<br /><br /></td></tr><tr>
#for row in rows:

#td valign="top">Veterinary Practice (Amendment) Bill</td><td valign="top">To enable the Minister to make regulations providing that specified procedures carried out on animals are not restricted to registered veterinary practitioners or registered veterinary nurses and to make a number of technical improvements to the Act in light of experience of operation<br /><br /></td></tr><tr><td colspan="3"><strong>Communications Energy and Natural Resources</strong></td></tr>

trs = soup.findAll('tr') 
for tr in trs:
    if tr.find(colspan="3"):
        continue
#    elif tr.contents[1].contents[0]==" Name Of Company ":
#        continue
    else:
        number, bill, desc = tr.contents[0].content, tr.contents[1].content, tr.contents[2].content

    #dept = re.search('<td colspan="3"><strong>(.*?)</strong></td>', row)
    #if dept:
    #    deptb = dept
    
    
        
      #  deptb, number, bill, desc  = None, None, None, None    
    





    #print deptb, number, bill, desc
    data = {'number': number,  'bill': bill, 'desc': desc } #'deptb':deptb, 
    scraperwiki.sqlite.save(['number'], data)   
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup


# The URLs we're going to scrape:
url = "http://www.rte.ie/news/election2011/newtds.html"


html = scraperwiki.scrape(url)

# http://www.taoiseach.gov.ie/eng/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_A1.html SECTION A - Lists 23 Bills which the Government expect to publish from the start of the Dáil session up to the beginning of the next session
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_B1.html SECTION B - Lists 13 Bills in respect of which Heads of Bills have been approved by Government and of which texts are being prepared
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_C11.html SECTION C - Lists 55 Bills in respect of which heads have yet to be approved by Government
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_D1.html SECTION D - Lists 25 Bills which are currently before the Dáil or Seanad
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_E1.html SECTION E - Lists 113 Bills which were enacted since the Government came to office on 14th June, 2007
# http://www.taoiseach.gov.ie/eng/Taoiseach_and_Government/Government_Legislation_Programme/SECTION_F1.html SECTION F - Lists 121 Bills which were published since the Government came to office on 14th June, 2007

# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.

# def gettext(html):
#    """Return the text within html, removing any HTML tags i
#    cleaned = re.sub('<.*?>', '', html)  # remove tags
#    cleaned = ' '.join(cleaned.split())  # collapse whitespace
#    return cleaned

#text = scraperwiki.scrape(url)



soup = BeautifulSoup(html)


#rows = re.findall('(?si)<tr[^>]*>(.*?)</tr>', text)
# <td valign="top">Forestry Bill</td><td valign="top">To reform and update the legislative framework relating to forestry in order to support the development of a modern forestry sector, which enshrines #the principles of sustainable forest management and protection of the environment<br /><br /></td></tr><tr>
#for row in rows:

#td valign="top">Veterinary Practice (Amendment) Bill</td><td valign="top">To enable the Minister to make regulations providing that specified procedures carried out on animals are not restricted to registered veterinary practitioners or registered veterinary nurses and to make a number of technical improvements to the Act in light of experience of operation<br /><br /></td></tr><tr><td colspan="3"><strong>Communications Energy and Natural Resources</strong></td></tr>

trs = soup.findAll('tr') 
for tr in trs:
    if tr.find(colspan="3"):
        continue
#    elif tr.contents[1].contents[0]==" Name Of Company ":
#        continue
    else:
        number, bill, desc = tr.contents[0].content, tr.contents[1].content, tr.contents[2].content

    #dept = re.search('<td colspan="3"><strong>(.*?)</strong></td>', row)
    #if dept:
    #    deptb = dept
    
    
        
      #  deptb, number, bill, desc  = None, None, None, None    
    





    #print deptb, number, bill, desc
    data = {'number': number,  'bill': bill, 'desc': desc } #'deptb':deptb, 
    scraperwiki.sqlite.save(['number'], data)   
