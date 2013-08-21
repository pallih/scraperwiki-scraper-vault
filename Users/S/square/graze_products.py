import scraperwiki
import BeautifulSoup
import urllib2
from scraperwiki import sqlite

base_url = 'http://www.graze.com/products'

def save_product(product, group):
    data = {
        'group' : group['group_name'],
        'product' : product['product_name'],
        'ingredients' : product['product_ingredients'],
    }
    sqlite.save(unique_keys=['group', 'product'], data=data)    
    return

def get_products(group_url):
    products = []

    products_html = urllib2.urlopen(group_url).read()
    products_page = BeautifulSoup.BeautifulSoup(products_html)
    
    products_div = products_page.find('div', {'class': 'productList'})
    for product_div in products_div.findAll('div', {'class': 'productLargeLabelContent'}):
        product_a = product_div.find('a')
        print product_a
        product_url = base_url + product_a['href']
        product_name = product_a.string
        if product_name is None:
            product_name = product_a.find('img')['alt']
        product_name = product_name.replace('"','').strip()
        product_ingredients = product_div.find('div', {'class': 'productLargeIngredients'}).string.strip()
        products.append({'product_name': product_name, 'product_url': product_url, 'product_ingredients': product_ingredients})
        print product_name, product_url, product_ingredients
    return products


def get_groups():
    
    groups = []
    
    group_html = urllib2.urlopen(base_url).read()
    group_page = BeautifulSoup.BeautifulSoup(group_html)
    
    menu_div = group_page.find('div', {'class': 'productMenu'})
    menu_ul = menu_div.findAll('ul')[1]
    for menu_li in menu_ul.findAll('li', {'class': True}):
        group_url = menu_li.find('a')['href']
        group_name = menu_li.find('a').find('span').string
        groups.append({'group_name': group_name, 'group_url': group_url})
        print group_name, group_url
    
    return groups


def run_scraper():
    
    group_list = get_groups()
    
    for group in group_list:
        product_list = get_products(group['group_url'])
        for product in product_list:
            save_product(product, group)


run_scraper()


