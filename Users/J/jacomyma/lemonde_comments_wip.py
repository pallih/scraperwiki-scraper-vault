import scraperwiki, csv, urllib2, re, time
from lxml import etree

sources_url = 'https://spreadsheets.google.com/tq?tqx=out:csv&tq=select%20A%20where%20A%21%3D%27%27&key=0AvpuSyVziOZEdGVSbkxxdGdWRGNEdEVvVVU3cTNWT2c&gid='
sleep_delay = 60

def dropper(table):
    if table != '':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

# dropper('comments')

nReader = csv.DictReader(urllib2.urlopen(sources_url))

for row in nReader:
    url = row['']
    _,_,domain,section,content_type,year,month,day,page = url.split('/')
    id,_ = page.split('.')
    base_comment_url = 'http://%s/%s/reactions/%s/%s/%s/%s' % (domain,section,year,month,day,id)
    print 'Scraping article %s' % id
    base_comment_relative_url = '/reactions/%s/%s/%s/%s' % (year,month,day,id)
    counter = 1
    flag = True
    article_metas = {'article_url': url, 'article_id': id, 'article_section': section, 'article_year': year, 'article_month': month, 'article_day': day, 'article_date':'%s-%s-%s' % (year, month, day), 'reply_to':'', 'timestamp':''}
    last_comment_id = ''
    
    while flag:
        flag = False
        datarow = article_metas.copy()
        datarow['source_url'] = '%s_%s.html' % (base_comment_url, counter)
        print 'Scrapping comments page %s' % counter
        comment_next_url = '%s_%s.html' % (base_comment_relative_url, counter+1)
        content = urllib2.urlopen(datarow['source_url']).read()
        if(comment_next_url in content):
            flag = True
            print ('There is a next page (%s)' % (counter+1)), comment_next_url
        tree = etree.HTML(content)
        divs = tree.xpath('//div[@data-reaction_id]')
        for div in divs:
            datarow['comment_id'] = div.attrib['data-reaction_id']
            imgs = div.xpath('./p/img[@data-src]')
            datarow['user_avatar_img'] = imgs[0].attrib['data-src'] if len(imgs) > 0 else ''
            links = div.xpath('./div/p[@class="references"]/a')
            if len(links) > 0:
                # There is a link
                datarow['user_name'] = links[0].text.strip()
                datarow['user_link'] = links[0].attrib['href']
            else:
                datarow['user_name'] = div.xpath('./div/p[@class="references"]')[0].text.strip()
                datarow['user_link'] = ''
            datarow['comment_date'] = div.xpath('.//span[@data-date-iso]')[0].attrib['data-date-iso']
            text = div.xpath('./div/p')[1].text
            if text:
                datarow['comment_text'] = text.strip()
            else:
                datarow['comment_text'] = ''
            datarow['timestamp'] = time.time()
            if 'reponse' in div.attrib['class']:
                datarow['reply_to'] = last_comment_id
            scraperwiki.sqlite.save(unique_keys=['comment_id'], table_name='comments', data=datarow)
            last_comment_id = datarow['comment_id']
        counter += 1
        time.sleep(sleep_delay)
import scraperwiki, csv, urllib2, re, time
from lxml import etree

sources_url = 'https://spreadsheets.google.com/tq?tqx=out:csv&tq=select%20A%20where%20A%21%3D%27%27&key=0AvpuSyVziOZEdGVSbkxxdGdWRGNEdEVvVVU3cTNWT2c&gid='
sleep_delay = 60

def dropper(table):
    if table != '':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

# dropper('comments')

nReader = csv.DictReader(urllib2.urlopen(sources_url))

for row in nReader:
    url = row['']
    _,_,domain,section,content_type,year,month,day,page = url.split('/')
    id,_ = page.split('.')
    base_comment_url = 'http://%s/%s/reactions/%s/%s/%s/%s' % (domain,section,year,month,day,id)
    print 'Scraping article %s' % id
    base_comment_relative_url = '/reactions/%s/%s/%s/%s' % (year,month,day,id)
    counter = 1
    flag = True
    article_metas = {'article_url': url, 'article_id': id, 'article_section': section, 'article_year': year, 'article_month': month, 'article_day': day, 'article_date':'%s-%s-%s' % (year, month, day), 'reply_to':'', 'timestamp':''}
    last_comment_id = ''
    
    while flag:
        flag = False
        datarow = article_metas.copy()
        datarow['source_url'] = '%s_%s.html' % (base_comment_url, counter)
        print 'Scrapping comments page %s' % counter
        comment_next_url = '%s_%s.html' % (base_comment_relative_url, counter+1)
        content = urllib2.urlopen(datarow['source_url']).read()
        if(comment_next_url in content):
            flag = True
            print ('There is a next page (%s)' % (counter+1)), comment_next_url
        tree = etree.HTML(content)
        divs = tree.xpath('//div[@data-reaction_id]')
        for div in divs:
            datarow['comment_id'] = div.attrib['data-reaction_id']
            imgs = div.xpath('./p/img[@data-src]')
            datarow['user_avatar_img'] = imgs[0].attrib['data-src'] if len(imgs) > 0 else ''
            links = div.xpath('./div/p[@class="references"]/a')
            if len(links) > 0:
                # There is a link
                datarow['user_name'] = links[0].text.strip()
                datarow['user_link'] = links[0].attrib['href']
            else:
                datarow['user_name'] = div.xpath('./div/p[@class="references"]')[0].text.strip()
                datarow['user_link'] = ''
            datarow['comment_date'] = div.xpath('.//span[@data-date-iso]')[0].attrib['data-date-iso']
            text = div.xpath('./div/p')[1].text
            if text:
                datarow['comment_text'] = text.strip()
            else:
                datarow['comment_text'] = ''
            datarow['timestamp'] = time.time()
            if 'reponse' in div.attrib['class']:
                datarow['reply_to'] = last_comment_id
            scraperwiki.sqlite.save(unique_keys=['comment_id'], table_name='comments', data=datarow)
            last_comment_id = datarow['comment_id']
        counter += 1
        time.sleep(sleep_delay)
