# -*- coding: utf-8 -*-
import sys
import codecs
import lxml.html
import scraperwiki

# プログラム上で使用するエンコーディング.
ENCODING = 'utf_8'

# 対象のURL.
SCRAP_URL          = 'http://www43.atpages.jp/toholyrics/mobile/menu.php?song={0}'
SCRAP_XPATH_LYRICS = '//div[@class="lyrics"]'
SCRAP_ENCODING     = 'utf_8'

# データベース名.
DATABASE_THIS      = 'touhou_karaoke_lyrics'
DATABASE_SONG_LIST = 'touhou_karaoke'

# データベースラベル.
DATA_LABEL_REQUEST = u'request'
DATA_LABEL_LYRICS  = u'lyrics'

DATA_LABEL_UNIQUE_KEYS = [DATA_LABEL_REQUEST, DATA_LABEL_LYRICS]

# データベースで使用する改行コード.
DATA_RECORD_RETURN_CODE = u'\n'

# スクラップしたデータの検証.
def record_validate( record ):
    v1 = DATA_LABEL_REQUEST in record
    v2 = DATA_LABEL_LYRICS in record
    if all( [v1, v2] ):
        item = record[DATA_LABEL_LYRICS]
        return all( [not (item is None), item != ''] )
    else:
        return False

# スクラップしたデータをデータベース格納用に変換.
def record_formalize( record ):
    return record

# レコードの保存.
def record_save( record ):
    scraperwiki.sqlite.save( DATA_LABEL_UNIQUE_KEYS, record )
    return True

# 特殊なスクラップ項目のパーサー
def parse_lyrics( element ):
    text = ''
    for p in element.xpath( 'p' ):
        text += p.text_content()
    return text

# カラオケIDリストを取得.
def karaoke_get_list():
    records = scraperwiki.sqlite.select( 'distinct request from touhou_karaoke.swdata order by request asc' ) 
    return records

# 歌詞をスクラップ
def scrap( request ):
    url = SCRAP_URL.format( request )
    try:
        html = scraperwiki.scrape( url )
    except Exception as e:
        print e
        return False
    root = lxml.html.fromstring( html.decode( SCRAP_ENCODING ) )

    lyrics = root.xpath( SCRAP_XPATH_LYRICS )
    if len( lyrics ) == 1:
        record = {}
        record[DATA_LABEL_REQUEST] = request
        record[DATA_LABEL_LYRICS] = parse_lyrics( lyrics[0] )
        
        if not record_validate( record ):
            return False
        formalized_record = record_formalize( record )
        if record_save( formalized_record ):
            return True
        else:
            return False
    else:
        return False

# main
scraperwiki.sqlite.attach( DATABASE_SONG_LIST )
records = karaoke_get_list()

scraperwiki.sqlite.attach( DATABASE_THIS )
if ( all( map( lambda r: scrap( r[DATA_LABEL_REQUEST] ), records ) ) ):
    sys.exit( 0 )
else:
    sys.exit( 1 )