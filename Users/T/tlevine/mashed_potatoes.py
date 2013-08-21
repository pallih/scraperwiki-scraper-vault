import scraperwiki
import lxml.html

def scrape_twocolumn_table(url,tagsyntax,table_name,key='key',value='value'):
  htmldata = scraperwiki.scrape(url)
  root = lxml.html.fromstring(htmldata)
  for tr in root.cssselect(tagsyntax):
    tds = tr.cssselect("td")
    data = {
      key : tds[0].text_content(),
      value : tds[1].text_content()
    }
    scraperwiki.sqlite.save([],data,table_name)

scrape_twocolumn_table("http://unstats.un.org/unsd/demographic/products/socind/education.htm","div[align='left'] tr.tcont",'unstats',key='country',value='years_in_school')
scrape_twocolumn_table("http://bestplaces.net/zip-code/illinois/des_plaines/60016","table[rules='cols'] tr[class!='header']",'bestplaces')
