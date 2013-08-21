import scraperwiki

# Blank Python

#Juiste CSS selectors importeren
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.gaslicht.com/energie-vergelijken/stroom-en-gas.aspx?result=on&huishouden=gezin&typeaansluitingstroom=aansluiting2&typeaansluitinggas=aansluitinggas2&huidigeleverancier=onbekend&postcode=9724EM&pchuisnr=&wat_vergelijk=stroomgas&ewijz_stroomverbruik_input=3500&ewijz_hoogtarrief_input=2100&ewijz_laagtarrief_input=1400&ewijz_gasverbruik_input=1800&submit.x=51&submit.y=6")
root = lxml.html.fromstring(html)


el1 = root.cssselect(".jaarkosten")    [0:10]
print el1[0:10]




class NorthAfricaSpider:
   name = "northafrica"
   allowed_domains = ["http://www.north-africa.com/"]
   start_urls = [
       "http://www.north-africa.com/naj_news/news_na/index.1.html",
   ]

   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sites = hxs.select('//ul/li')
       items = []
       for site in sites:
           item = NorthAfricaItem()
           item['title'] = site.select('//div[@class="short_holder"]    /h2/a/text()').extract()
       item['link'] = site.select('//div[@class="short_holder"]/h2/a/@href').extract()
       item['desc'] = site.select('//span[@class="summary"]/text()').extract()
       items.append(item)
   return items