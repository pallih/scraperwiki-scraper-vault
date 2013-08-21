from scraperwiki.sqlite import save,select
from scraperwiki import swimport
from urllib2 import urlopen
from lxml.html import fromstring
randomsleep=swimport('randomsleep').randomsleep

MENU="http://www.arttrail.com/portfolios.html"
DIR="http://www.arttrail.com/"

def main():
  download()
  standardize()

def download():
  d=[]
  for href in artist_hrefs():
    row=artist_contact_info(href)
    row['href']=href
    d.append(row)
    randomsleep()
  save(['href'],d,'artist-contact-info')

def standardize():
  d=select("""
"http://www.arttrail.com/" || href as "Art Trail page", website as "Website", coalesce(`e-mail`,email) as "Email address", coalesce(coalesce(cell,phone),studio) as "Phone number" from `artist-contact-info`
""")
  save(['Art Trail page'],d,'artist-contact-info-standardized')

def artist_hrefs():
  x=fromstring(urlopen(MENU).read())
  hrefs=x.xpath('id("tab01")/descendant::a/@href')
  return set(hrefs)

def artist_contact_info(href):
  x=fromstring(urlopen(DIR+href).read())
  dts=x.xpath('//h3[text()="CONTACT INFORMATION" or text()=" CONTACT INFORMATION"or text()="CONTACT INFORMATION " or text()=" CONTACT INFORMATION "]/following-sibling::dl/dt')
  row={}
  for dt in dts:
    row[dt.text_content().replace(':','')]=dt.xpath('following-sibling::dd')[0].text_content()
  return row

#print artist_contact_info('artists/BAIRD.html')
#print artist_contact_info('artists/SUN.html')
#main()