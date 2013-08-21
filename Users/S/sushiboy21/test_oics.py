import scraperwiki
import re
from BeautifulSoup import BeautifulSoup          

# Blank Python

url = "http://www.pco-bcp.gc.ca/oic-ddc.asp?lang=eng&txtToDate=&txtPrecis=&Page=&txtOICID=&txtAct=&txtBillNo=&txtFromDate=&txtDepartment=&txtChapterNo=&txtChapterYear=&rdoComingIntoForce=&DoSearch=Search+/+List&pg=1"

html = scraperwiki.scrape(url)

soup = BeautifulSoup(''.join(html))

print soup.findAll('p', align="center")
