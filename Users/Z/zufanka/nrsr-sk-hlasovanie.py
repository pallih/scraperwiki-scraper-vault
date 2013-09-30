import scraperwiki
from lxml import etree

url = ""
scrape = etree.HTML(scraperwiki.scrape(url))

klub = scrape.xpath('//td[@class="hpo_result_block_title"]')

poslanci = scrape.xpath('//td[@class="hpo_result_block_title"]/following::td')

for i in poslanci:
    print i.text

import scraperwiki
from lxml import etree

url = ""
scrape = etree.HTML(scraperwiki.scrape(url))

klub = scrape.xpath('//td[@class="hpo_result_block_title"]')

poslanci = scrape.xpath('//td[@class="hpo_result_block_title"]/following::td')

for i in poslanci:
    print i.text

