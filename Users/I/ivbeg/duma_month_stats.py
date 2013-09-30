import scraperwiki
import socket
import lxml.html           

# Функция для извлечения данных из страницы статистики
def parse_page(url, data={}):
    h = scraperwiki.scrape(url)
    root = lxml.html.fromstring(h)
    n = 0
# Данные сравнительно просто извлекаются так как находятся в одной таблице
    for tr in root.cssselect("div[class='table-data td-filter'] table tr"):
        tds = tr.cssselect("td")
        if len(tds) < 4: continue
        n += 1
# Делаем словарь
        d = {'name' : tds[0].text_content(), 'num_total' : int(tds[1].text_content()), 'num_fedconst_laws' : int(tds[2].text_content()), 'num_ratif' : int(tds[3].text_content()), 'order' : n}   
# Это искусственный ключ уникальности на ссылке страницы статистики и номере строки со значениями индикаторов
        d['uniq'] = str(d['order']) + '_' + data['url']
        data.update(d)        
        print data
# Сохраняем результат
        scraperwiki.sqlite.save(unique_keys=['uniq'], data=data)
    
socket.setdefaulttimeout(10)

# Мы берём одну страницу и извлекаем из неё список всех остальных из которых нам надо извлечь значения индикаторов
html = scraperwiki.scrape("http://www.duma.gov.ru/legislative/statistics/?type=month&v=01.2010")
# Разбираем страницы с помощью lxml
root = lxml.html.fromstring(html)
# Ссылки на статистику по месяцам можно получить вот таким запросом
for td in root.cssselect("td[class='month']"):
    hr = td.cssselect("a")

# Из относительной ссылки мы получаем: месяц, год и абсолютную ссылку
    s = hr[0].attrib['href'].split('v=')[1]
    month = int(s.split('.')[0])
    year = int(s.split('.')[1])
    url = 'http://www.duma.gov.ru' + hr[0].attrib['href']
# Все данные вносим в словарь
    data = {
      'url' : url,
      'month' : month,
      'year' : year
    }
# Запускаем извлечение данных из страницы, кроме 1996 года, там возникает какая-то ошибка
    if year > 1996:
        data = parse_page(url, data)

import scraperwiki
import socket
import lxml.html           

# Функция для извлечения данных из страницы статистики
def parse_page(url, data={}):
    h = scraperwiki.scrape(url)
    root = lxml.html.fromstring(h)
    n = 0
# Данные сравнительно просто извлекаются так как находятся в одной таблице
    for tr in root.cssselect("div[class='table-data td-filter'] table tr"):
        tds = tr.cssselect("td")
        if len(tds) < 4: continue
        n += 1
# Делаем словарь
        d = {'name' : tds[0].text_content(), 'num_total' : int(tds[1].text_content()), 'num_fedconst_laws' : int(tds[2].text_content()), 'num_ratif' : int(tds[3].text_content()), 'order' : n}   
# Это искусственный ключ уникальности на ссылке страницы статистики и номере строки со значениями индикаторов
        d['uniq'] = str(d['order']) + '_' + data['url']
        data.update(d)        
        print data
# Сохраняем результат
        scraperwiki.sqlite.save(unique_keys=['uniq'], data=data)
    
socket.setdefaulttimeout(10)

# Мы берём одну страницу и извлекаем из неё список всех остальных из которых нам надо извлечь значения индикаторов
html = scraperwiki.scrape("http://www.duma.gov.ru/legislative/statistics/?type=month&v=01.2010")
# Разбираем страницы с помощью lxml
root = lxml.html.fromstring(html)
# Ссылки на статистику по месяцам можно получить вот таким запросом
for td in root.cssselect("td[class='month']"):
    hr = td.cssselect("a")

# Из относительной ссылки мы получаем: месяц, год и абсолютную ссылку
    s = hr[0].attrib['href'].split('v=')[1]
    month = int(s.split('.')[0])
    year = int(s.split('.')[1])
    url = 'http://www.duma.gov.ru' + hr[0].attrib['href']
# Все данные вносим в словарь
    data = {
      'url' : url,
      'month' : month,
      'year' : year
    }
# Запускаем извлечение данных из страницы, кроме 1996 года, там возникает какая-то ошибка
    if year > 1996:
        data = parse_page(url, data)

