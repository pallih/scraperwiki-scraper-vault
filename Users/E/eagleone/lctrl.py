import scraperwiki
import lxml.html
import urllib

    
def rm_spaces(i_string):
    return " ".join(i_string.split())




def parse(url):
    reader = urllib.urlopen(url).read()
    tree = lxml.html.fromstring( reader )

    list_trs = tree.get_element_by_id('TabAnn').cssselect('tr')
    
    count = 1
    data = {}
    for tr in list_trs[1:len(list_trs)]:
        if count == 1:
            try:
                data['url']     = rm_spaces(tr.find_class('lcbrand')[0].cssselect('a')[0].get('href'))
                data['marque']  = rm_spaces(tr.find_class('lcbrand')[0].text_content())
                data['modele']  = rm_spaces(tr.find_class('lcmodel')[0].text_content())
                data['price']   = rm_spaces(tr.find_class('lcprice')[0].text_content())
                data['km']      = rm_spaces(tr.find_class('lcmileage')[0].text_content())
                data['annee']   = rm_spaces(tr.find_class('lcyear')[0].text_content())
                data['dpt']     = rm_spaces(tr.find_class('lcdpt')[0].text_content())
                data['vendeur'] = rm_spaces(tr.find_class('lcorig')[0].text_content())
                data['img']     = rm_spaces(tr.find_class('lcphoto')[0].find_class('lcmultibrdr')[0].cssselect('img')[0].get('src'))
                count += 1
            except IndexError:
                pass
        elif count == 2:
            try:
                data['finition'] = rm_spaces(tr.find_class('lcversion')[0].text_content())
                count += 1
            except IndexError:
                pass
        elif count == 3:
            if data['modele'] != "" and data['annee'] != "":
                scraperwiki.sqlite.save(unique_keys=['url'],data=data)
            data = {}
            count = 1


#url = "http://www.lacentrale.fr/occasion-voiture.html"
url = "http://www.lacentrale.fr/occasion-voiture-modele.html"
reader = urllib.urlopen(url).read()
tree = lxml.html.fromstring( reader )

for column in tree.find_class('ColumnContMarquesModeles'):
    for li in column.cssselect('li'):
        if li.get('class') != 'letter':
            url = li.cssselect('a')[0].get('href')
            parse('http://www.lacentrale.fr/%s' % url)



import scraperwiki
import lxml.html
import urllib

    
def rm_spaces(i_string):
    return " ".join(i_string.split())




def parse(url):
    reader = urllib.urlopen(url).read()
    tree = lxml.html.fromstring( reader )

    list_trs = tree.get_element_by_id('TabAnn').cssselect('tr')
    
    count = 1
    data = {}
    for tr in list_trs[1:len(list_trs)]:
        if count == 1:
            try:
                data['url']     = rm_spaces(tr.find_class('lcbrand')[0].cssselect('a')[0].get('href'))
                data['marque']  = rm_spaces(tr.find_class('lcbrand')[0].text_content())
                data['modele']  = rm_spaces(tr.find_class('lcmodel')[0].text_content())
                data['price']   = rm_spaces(tr.find_class('lcprice')[0].text_content())
                data['km']      = rm_spaces(tr.find_class('lcmileage')[0].text_content())
                data['annee']   = rm_spaces(tr.find_class('lcyear')[0].text_content())
                data['dpt']     = rm_spaces(tr.find_class('lcdpt')[0].text_content())
                data['vendeur'] = rm_spaces(tr.find_class('lcorig')[0].text_content())
                data['img']     = rm_spaces(tr.find_class('lcphoto')[0].find_class('lcmultibrdr')[0].cssselect('img')[0].get('src'))
                count += 1
            except IndexError:
                pass
        elif count == 2:
            try:
                data['finition'] = rm_spaces(tr.find_class('lcversion')[0].text_content())
                count += 1
            except IndexError:
                pass
        elif count == 3:
            if data['modele'] != "" and data['annee'] != "":
                scraperwiki.sqlite.save(unique_keys=['url'],data=data)
            data = {}
            count = 1


#url = "http://www.lacentrale.fr/occasion-voiture.html"
url = "http://www.lacentrale.fr/occasion-voiture-modele.html"
reader = urllib.urlopen(url).read()
tree = lxml.html.fromstring( reader )

for column in tree.find_class('ColumnContMarquesModeles'):
    for li in column.cssselect('li'):
        if li.get('class') != 'letter':
            url = li.cssselect('a')[0].get('href')
            parse('http://www.lacentrale.fr/%s' % url)



