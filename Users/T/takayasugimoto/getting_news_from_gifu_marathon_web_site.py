import scraperwiki
import urllib2
import lxml.html
import datetime
import pytz

url = 'http://www.gifu-marathon.jp/news/' # 高橋尚子杯 ぎふ清流マラソン 新着情報・お知らせ
content = urllib2.urlopen(url).read()
dom = lxml.html.fromstring(content)

divs = dom.xpath('//div[@class="entry_area"]')
#print divs

entries = []

for i in range(len(divs)):

    div = divs[i]
    id = div.get('id')
    print id

    """エントリーデータを生成"""
    entry = {
        'id': id,  # id属性の値をデータストア保存時のキーに利用
        'date': None,
        'title': None,
        'description': '',
        'link': None,
        'order_num': i # ソートキーとして利用予定
#        'creation_date': datetime.datetime.now()
    }

    img_url = None # 本文内の画像のURL

    """値を取得"""
    # class属性の値によって日付/タイトル/本文を識別    
    date_string = div.xpath('string(./p[@class="date"])') # 日付文字列（e.g. "2011/12/31"）
    date = datetime.datetime.strptime(date_string, '%Y/%m/%d')
    date_jst = date.replace(tzinfo=pytz.timezone('Asia/Tokyo')) # UTCとなっているため日本時間とする
    entry['date'] = date_jst

    entry['title'] = div.xpath('string(./p[@class="title"])') # タイトル

    body_divs = div.xpath('./div[@class="body"]') # 本文（複数のbodyに分割されている場合があり、連結する必要がある）
    for body_div in body_divs:
            string = lxml.html.tostring(body_div, method='text', encoding='utf-8') # 文字列のみを取得（タグは除外され、改行や空白等は含まれる）
            entry['description'] += string.strip()
            imgs = body_div.xpath('.//img[@src]')
            if len(imgs) > 0:
                img_url = imgs[0].get('src') # 本文内の画像は1枚だけという前提

    # 詳細へのリンク
    more_imgs = div.xpath('.//img[contains(@src, "btn_more.gif")]')  # [詳しくはこちら]ボタン画像
    if len(more_imgs) > 0:
        # [詳しくはこちら]ボタンがある場合は、そのリンク先URL
        more_a = more_imgs[0].getparent() # ボタン画像は1枚だけという前提
        entry['link'] = more_a.get('href')
    elif img_url:
        # 上記以外の場合は、本文内に画像があったらそのURL
        entry['link'] = img_url

    entries.append(entry)

if len(entries) > 0:
    # 1件以上なら洗い替え
    print 'Cleaning swdata...'
    scraperwiki.sqlite.execute("drop table if exists swdata")
    """データストアに保存"""
    scraperwiki.sqlite.save(unique_keys=['id'], data=entries)



    """XPathを使っていなかった過去のコード

    for p_or_div in list(div): # 子要素（pまたはdiv）のリストを取得
        # class属性の値によって日付/タイトル/本文を識別
        cls = p_or_div.get('class')

        if 'date' == cls: # 日付
            entry['date'] = p_or_div.text
            continue

        if 'title' == cls: # タイトル
            entry['title'] = p_or_div.text
            continue

        if 'body' == cls: # 本文（複数のbodyに分割されている場合があり、連結する必要がある）
            string = lxml.html.tostring(p_or_div, method='text', encoding='utf-8') # 文字列のみを取得（タグは除外され、改行や空白等は含まれる）
            entry['description'] += string.strip()
            imgs = p_or_div.xpath('.//img[@src]')
            if len(imgs) > 0:
                entry['img_url'] = imgs[0].get('src') # 本文内の画像は1枚だけという前提
            continue
        
        # 詳細へのリンク
        elem = p_or_div[0] # 最初の子
        if 'a' == elem.tag: # a要素の場合
            a_elem = elem
            elem = a_elem[0] # 最初の子
            if 'img' == elem.tag: # img要素の場合
                img_elem = elem
                src = img_elem.get('src')
                if src.endswith('btn_more.gif'): # [詳しくはこちら ▶]ボタン画像
                    entry['link'] = a_elem.get('href')
    """
import scraperwiki
import urllib2
import lxml.html
import datetime
import pytz

url = 'http://www.gifu-marathon.jp/news/' # 高橋尚子杯 ぎふ清流マラソン 新着情報・お知らせ
content = urllib2.urlopen(url).read()
dom = lxml.html.fromstring(content)

divs = dom.xpath('//div[@class="entry_area"]')
#print divs

entries = []

for i in range(len(divs)):

    div = divs[i]
    id = div.get('id')
    print id

    """エントリーデータを生成"""
    entry = {
        'id': id,  # id属性の値をデータストア保存時のキーに利用
        'date': None,
        'title': None,
        'description': '',
        'link': None,
        'order_num': i # ソートキーとして利用予定
#        'creation_date': datetime.datetime.now()
    }

    img_url = None # 本文内の画像のURL

    """値を取得"""
    # class属性の値によって日付/タイトル/本文を識別    
    date_string = div.xpath('string(./p[@class="date"])') # 日付文字列（e.g. "2011/12/31"）
    date = datetime.datetime.strptime(date_string, '%Y/%m/%d')
    date_jst = date.replace(tzinfo=pytz.timezone('Asia/Tokyo')) # UTCとなっているため日本時間とする
    entry['date'] = date_jst

    entry['title'] = div.xpath('string(./p[@class="title"])') # タイトル

    body_divs = div.xpath('./div[@class="body"]') # 本文（複数のbodyに分割されている場合があり、連結する必要がある）
    for body_div in body_divs:
            string = lxml.html.tostring(body_div, method='text', encoding='utf-8') # 文字列のみを取得（タグは除外され、改行や空白等は含まれる）
            entry['description'] += string.strip()
            imgs = body_div.xpath('.//img[@src]')
            if len(imgs) > 0:
                img_url = imgs[0].get('src') # 本文内の画像は1枚だけという前提

    # 詳細へのリンク
    more_imgs = div.xpath('.//img[contains(@src, "btn_more.gif")]')  # [詳しくはこちら]ボタン画像
    if len(more_imgs) > 0:
        # [詳しくはこちら]ボタンがある場合は、そのリンク先URL
        more_a = more_imgs[0].getparent() # ボタン画像は1枚だけという前提
        entry['link'] = more_a.get('href')
    elif img_url:
        # 上記以外の場合は、本文内に画像があったらそのURL
        entry['link'] = img_url

    entries.append(entry)

if len(entries) > 0:
    # 1件以上なら洗い替え
    print 'Cleaning swdata...'
    scraperwiki.sqlite.execute("drop table if exists swdata")
    """データストアに保存"""
    scraperwiki.sqlite.save(unique_keys=['id'], data=entries)



    """XPathを使っていなかった過去のコード

    for p_or_div in list(div): # 子要素（pまたはdiv）のリストを取得
        # class属性の値によって日付/タイトル/本文を識別
        cls = p_or_div.get('class')

        if 'date' == cls: # 日付
            entry['date'] = p_or_div.text
            continue

        if 'title' == cls: # タイトル
            entry['title'] = p_or_div.text
            continue

        if 'body' == cls: # 本文（複数のbodyに分割されている場合があり、連結する必要がある）
            string = lxml.html.tostring(p_or_div, method='text', encoding='utf-8') # 文字列のみを取得（タグは除外され、改行や空白等は含まれる）
            entry['description'] += string.strip()
            imgs = p_or_div.xpath('.//img[@src]')
            if len(imgs) > 0:
                entry['img_url'] = imgs[0].get('src') # 本文内の画像は1枚だけという前提
            continue
        
        # 詳細へのリンク
        elem = p_or_div[0] # 最初の子
        if 'a' == elem.tag: # a要素の場合
            a_elem = elem
            elem = a_elem[0] # 最初の子
            if 'img' == elem.tag: # img要素の場合
                img_elem = elem
                src = img_elem.get('src')
                if src.endswith('btn_more.gif'): # [詳しくはこちら ▶]ボタン画像
                    entry['link'] = a_elem.get('href')
    """
