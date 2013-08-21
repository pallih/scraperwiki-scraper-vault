import scraperwiki           
import lxml.html
from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://empleos.trabajo.gob.pe:8080/empleoperu/Vacante.do?method=listado_vacantes")
soup = BeautifulSoup(html)
pretty_html = soup.prettify()

root = lxml.html.fromstring(pretty_html)

#tds = root.xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[8]/td/table/tbody/tr[2]/td')
#tds = root.xpath('/html/body/table/tr[1]/td[2]/table/tr[8]/td[1]/table/tr[2]/td')

rows = root.xpath('/html/body/table/tr/td[2]/table/tr[8]/td/table/tr')

print len(rows)

for row in rows:
    print row.at_css('td').text_content()



#for row in rows:
    #cols = row.xpath('//td/table/tr[2]/td')
    #agencia = cols[1].text_content()
    #print row.text_content()
#cols = rows[0].xpath('//td/table/tr[2]/td[2]') 
