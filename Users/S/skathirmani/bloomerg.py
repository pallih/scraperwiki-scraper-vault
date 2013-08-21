
import scraperwiki

# Blank Python
import urllib
from lxml import etree
from bs4 import BeautifulSoup

data = []
url = 'http://www.bloomberg.com/markets/companies/country/singapore/1'
text = scraperwiki.scrape(url)
tree = etree.HTML(text)
for link in tree.findall('.//div[@class="ticker_container"]//a'):
    href = link.get('href')
    if href and href.startswith('/quote/'):
        urls = ('http://www.bloomberg.com' + href+'/profile')
        text = scraperwiki.scrape(urls)
        tree = etree.HTML(text)
        company = (tree.find('.//title').text).split("-")[-2]
        print company
        span = tree.findall('.//div[@class="exchange_type"]//span')
        industry = span[5].text
        address_temp = tree.findall('.//div[@class="left_column"]//div')
        address =[]
        for row in address_temp: address.append(row.text)
        phone = [] 
        phone_temp = tree.findall('.//div[@class="right_column"]//div')
        for row in phone_temp: phone.append(row.text)
        executives = []
        executives_temp = tree.findall('.//div[@class="executive clearfix"]//span')
        for row in executives_temp: executives.append(row.text)
       
       
        url_income = ('http://www.bloomberg.com' + href+'/income-statement')
        text = scraperwiki.scrape(url_income)
        print text
        tree = etree.HTML(text)
        print url_income
        revenue_index = tree.findall('.//table[@class="key_stat_data alt_rows_stat_table"]//tr[@class="indentation_0 even"]//th')
        revenue_value = tree.findall('.//table[@class="key_stat_data alt_rows_stat_table"]//tr[@class="indentation_0 even"]//td')
      
        if revenue_index:
            for row in range(len(revenue_index)):
                if revenue_index[row].text == ' Revenue':
                    revenue = revenue_value[row].text
        else:
            revenue = 0
        print revenue

        netincome_index = tree.findall('.//table[@class="key_stat_data alt_rows_stat_table"]//tr[@class="indentation_0 even"]//th')
        netincome_value = tree.findall('.//table[@class="key_stat_data alt_rows_stat_table"]//tr[@class="indentation_0 even"]//td')
      
        if netincome_index:
            for row in range(len(netincome_index)):
                if revenue_index[row].text == ' Net Income':
                    netincome = netincome_value[row].text
        else:
            netincome = 0
        print netincome
        data = {'company':company,'industry':industry,'address':address,'executives':executives,'revenue':revenue,'netincome':netincome}
        scraperwiki.sqlite.save(unique_keys=['company','industry','address','executives','revenue','netincome'],data=data) 
