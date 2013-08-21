# -*- coding: utf-8 -*-
import sys
import codecs
import urllib2
import lxml.html 
import scraperwiki

# プログラム上で使用するエンコーディング.
ENCODING = 'utf_8'

# スクラップ対象の定義.
# URL.
TARGET_URLS = ( \
    'http://www32.atwiki.jp/toho_karaoke/pages/76.html', #あ \
    'http://www32.atwiki.jp/toho_karaoke/pages/80.html', #か \
    'http://www32.atwiki.jp/toho_karaoke/pages/77.html', #さ \
    'http://www32.atwiki.jp/toho_karaoke/pages/81.html', #た \
    'http://www32.atwiki.jp/toho_karaoke/pages/78.html', #な \
    'http://www32.atwiki.jp/toho_karaoke/pages/82.html', #は \
    'http://www32.atwiki.jp/toho_karaoke/pages/83.html', #ま \
    'http://www32.atwiki.jp/toho_karaoke/pages/84.html', #や \
    'http://www32.atwiki.jp/toho_karaoke/pages/85.html', #ら \
#   'http://www32.atwiki.jp/toho_karaoke/pages/86.html', #わ NO_DATA \
    )

# スクラップ先のページのエンコーディング.
TARGET_ENCODING = 'utf_8'

# サークル名のXPATH
TARGET_XPATH_CIRCLE = '//div[@id="wikibody"]/h3'

# テーブルのXPATH
TARGET_XPATH_TABLES = '//div[@id="wikibody"]/table'

# 取得項目の名前.
TARGET_CIRCLE         = u'サークル'
TARGET_VOCAL          = u'歌手名'
TARGET_ALBUM          = u'アルバム名'
TARGET_SONG           = u'曲名'
TARGET_ORIGINAL       = u'原作名'
TARGET_ORIGINAL_SONG  = u'原曲名'
TARGET_MOVIE_LINK     = u'動画リンク'
TARGET_REQUEST_NUMBER = u'曲番号'
TARGET_PUBLISH        = u'配信日'

# テーブルの項目.
TARGET_TABLE_HEADERS = ( \
    TARGET_VOCAL, \
    TARGET_ALBUM , \
    TARGET_SONG, \
    TARGET_ORIGINAL, \
    TARGET_ORIGINAL_SONG, \
    TARGET_MOVIE_LINK, \
    TARGET_REQUEST_NUMBER, \
    TARGET_PUBLISH, \
    )

# 取得する全項目.
TARGET_RECORD_LABELS = ( \
    TARGET_CIRCLE, \
    TARGET_VOCAL, \
    TARGET_ALBUM , \
    TARGET_SONG, \
    TARGET_ORIGINAL, \
    TARGET_ORIGINAL_SONG, \
    TARGET_MOVIE_LINK, \
    TARGET_REQUEST_NUMBER, \
    TARGET_PUBLISH, \
    )

# 動画リンクの種類.
TARGET_MOVIE_LINK_OFFICIAL = u'公'
TARGET_MOVIE_LINK_KARAOKE  = u'カラ'
TARGET_MOVIE_LINK_OTHER    = u'他'

TARGET_TABLE_LINKS = ( \
    TARGET_MOVIE_LINK_OFFICIAL, \
    TARGET_MOVIE_LINK_KARAOKE, \
    TARGET_MOVIE_LINK_OTHER, \
    )

# 列データで特殊なパースが必要なものを定義.
# デフォルト.
def parse_item_default( item ):
    return item.text_content()

# 動画リンク.
def parse_item_links( item ):
    data = {}
    links = item.xpath( 'a' )
    for link in links:
        name = link.text_content()
        validate_warning_with_msg( name in TARGET_TABLE_LINKS, WARNING_CODE_NEW_TABLE_LINK_FOUND, u'新しいリンク{0}'.format( name ) )
        validate( 'href' in link.attrib, ERROR_CODE_A_TAG_HAS_NO_LINK )
        data[name] = link.attrib['href']
    return data

# 日付.
def parse_item_date( item ):
    return item.text_content()

# 列名とパース関数の対応.
TARGET_TABLE_ITEM_PARSER = {
     TARGET_MOVIE_LINK: parse_item_links, \
     TARGET_PUBLISH: parse_item_date, \
}


# データベースラベル名.
DATA_LABEL_CIRCLE              = u'circle'
DATA_LABEL_VOCAL               = u'vocal'
DATA_LABEL_ALBUM               = u'album'
DATA_LABEL_SONG                = u'song'
DATA_LABEL_ORIGINAL            = u'original'
DATA_LABEL_ORIGINAL_SONG       = u'original_song'
DATA_LABEL_REQUEST_NUMBER      = u'request'
DATA_LABEL_PUBLISH             = u'publish'
DATA_LABEL_MOVIE_LINK_OFFICIAL = u'movie_link_official'
DATA_LABEL_MOVIE_LINK_KARAOKE  = u'movie_link_karaoke'
DATA_LABEL_MOVIE_LINK_OTHER    = u'movie_link_other'

# ユニークキー.
DATA_LABLE_UNIQUE_KEYS = [ \
    DATA_LABEL_CIRCLE, \
    DATA_LABEL_VOCAL, \
    DATA_LABEL_ALBUM, \
    DATA_LABEL_SONG, \
    DATA_LABEL_ORIGINAL, \
    DATA_LABEL_ORIGINAL_SONG, \
    DATA_LABEL_REQUEST_NUMBER, \
    DATA_LABEL_PUBLISH, \
#    DATA_LABEL_MOVIE_LINK_OFFICIAL, \
#    DATA_LABEL_MOVIE_LINK_KARAOKE, \
#    DATA_LABEL_MOVIE_LINK_OTHER, \
    ]

# 取得データとデータラベルの対応.
TARGET_TO_DATA_LABLE_TABLE = { \
    TARGET_CIRCLE:         DATA_LABEL_CIRCLE,\
    TARGET_VOCAL:          DATA_LABEL_VOCAL,\
    TARGET_ALBUM:          DATA_LABEL_ALBUM,\
    TARGET_SONG:           DATA_LABEL_SONG,\
    TARGET_ORIGINAL:       DATA_LABEL_ORIGINAL,\
    TARGET_ORIGINAL_SONG:  DATA_LABEL_ORIGINAL_SONG,\
    TARGET_REQUEST_NUMBER: DATA_LABEL_REQUEST_NUMBER,\
    TARGET_PUBLISH:        DATA_LABEL_PUBLISH,\
}

# レコードの検査.
def validate_record( record ):
    v1 = all( map( (lambda x: x in record), TARGET_RECORD_LABELS ) )
    v2 = all( map( (lambda x: x in TARGET_RECORD_LABELS), record ) )
    return all( [v1, v2] )

# レコードの正規化.
def formalize_record( record ):
    new = {}
    for name in TARGET_RECORD_LABELS:
        if name in TARGET_TO_DATA_LABLE_TABLE:
            new[TARGET_TO_DATA_LABLE_TABLE[name]]=record[name]

    links = record[TARGET_MOVIE_LINK]
    if TARGET_MOVIE_LINK_OFFICIAL in links:
        new[DATA_LABEL_MOVIE_LINK_OFFICIAL] = links[TARGET_MOVIE_LINK_OFFICIAL]
    if TARGET_MOVIE_LINK_KARAOKE in links:
        new[DATA_LABEL_MOVIE_LINK_KARAOKE] = links[TARGET_MOVIE_LINK_KARAOKE]
    if TARGET_MOVIE_LINK_OTHER in links:
        new[DATA_LABEL_MOVIE_LINK_OTHER] = links[TARGET_MOVIE_LINK_OTHER]
    return new

# レコードの保存.
def save_record( record ):
    scraperwiki.sqlite.save( unique_keys=DATA_LABLE_UNIQUE_KEYS, data=record )
    return True



# エラー処理のユーティリティ.
ERROR_CODE_UNDEFINED                = 0
ERROR_CODE_NOT_FOUND_TABLE          = 10
ERROR_CODE_NOT_CORRESPONDE_COUNT    = 11
ERROR_CODE_NO_CIRCLE_RECORD         = 12
ERROR_CODE_UNDIFINED_HEADER_FOUND   = 13
ERROR_CODE_A_TAG_HAS_NO_LINK        = 14
ERROR_CODE_INVALID_RECORD_FOUND     = 15
ERROR_CODE_FAILED_TO_SAVE           = 16

WARNING_CODE_NEW_TABLE_ROW_FOUND    = 20
WARNING_CODE_NEW_TABLE_LINK_FOUND   = 21
WARNING_CODE_NOT_FOUND_LINK_ROW     = 22

ERROR_TABLES = ( \
    ( ERROR_CODE_UNDEFINED                , u'エラーの詳細を記述します.' ), \
    ( ERROR_CODE_NOT_FOUND_TABLE          , u'サークルのリストがwikiから見つかりませんでした.' ), \
    ( ERROR_CODE_NOT_CORRESPONDE_COUNT    , u'サークルの数とテーブルの数が一致していません.' ), \
    ( ERROR_CODE_NO_CIRCLE_RECORD         , u'サークルのテーブルの中身がありません.' ), \
    ( ERROR_CODE_A_TAG_HAS_NO_LINK        , u'aタグがhref属性を持っていませんでした.' ), \
    ( ERROR_CODE_INVALID_RECORD_FOUND     , u'妥当でないレコードが見つかりました.' ), \
    ( ERROR_CODE_FAILED_TO_SAVE           , u'レコードの保存に失敗しました.' ), \
    ( WARNING_CODE_NEW_TABLE_ROW_FOUND    , u'新しいテーブル列を発見しました.' ), \
    ( WARNING_CODE_NEW_TABLE_LINK_FOUND   , u'新しい動画リンクの種類を発見しました.' ), \
    ( WARNING_CODE_NOT_FOUND_LINK_ROW     , u'動画リンクの列がありません.' ), \
    )


def error( error_code ):
    e = [(code,description) for (code,description) in ERROR_TABLES if code==error_code]
    if ( len( e ) > 0 ):
        (code,desc) = e[0]
        print (u'error: ' + desc).encode( ENCODING )
        sys.exit( code )
    else:
        print u'error: 未定義のエラーが発生しました.'.encode( ENCODING )
        sys.exit( 1 )

def warning( error_code ):
    e = [(code,description) for (code,description) in ERROR_TABLES if code==error_code]
    if ( len( e ) > 0 ):
        (code,desc) = e[0]
        print (u'warning: ' + desc).encode( ENCODING )
    else:
        print u'warning: 未定義の警告が発生しました.'.encode( ENCODING )
    

def validate( exp, code ):
    if ( not exp ):
        error( code )

def validate_with_msg( exp, code, msg ):
    if ( not exp ):
        print msg
        error( code )

def validate_warning( exp, code ):
    if ( not exp ):
        warning( code )

def validate_warning_with_msg( exp, code, msg ):
    if ( not exp ):
        print msg
        warning( code )


# スクラップ処理.
def scrap( url ):
    # ソースを取得.
    html = scraperwiki.scrape( url )
    root = lxml.html.fromstring( html.decode( TARGET_ENCODING ) )
    circles = root.xpath( TARGET_XPATH_CIRCLE )
    tables = root.xpath( TARGET_XPATH_TABLES )
    
    validate( len( circles ) > 0 and len( tables ) > 0, ERROR_CODE_NOT_FOUND_TABLE )
    validate( len( circles ) == len( tables ), ERROR_CODE_NOT_CORRESPONDE_COUNT )
    
    # サークル単位のテーブル処理.
    for (circle,tables) in zip(circles,tables):
        # テーブルのヘッダ情報を処理.
        lines = tables.xpath( 'tr' )
        line_count = len( lines )
        validate( line_count > 1, ERROR_CODE_NO_CIRCLE_RECORD )
    
        name_to_index_table = {}
        index_to_name_table = {}
        header_rows = lines[0].xpath( 'td' )
        row_count = len( header_rows )
        for x in range( row_count ):
            item = header_rows[x]
            name = item.text_content()
            name_to_index_table[name] = x
            index_to_name_table[x] = name
    
        # テーブルのレコード読み取り.
        prev_record = {}
        rowspans_count = row_count * [0]
        for y in range( 1, line_count ):
            rows = lines[y].xpath( 'td' )
            record = {TARGET_CIRCLE: circle.text_content()}
            x = 0
            for i in range( row_count ):
                name = index_to_name_table[i]
                if rowspans_count[i] > 0:
                    record[name] = prev_record[name]
                else:
                    item = rows[x]
                    if 'rowspan' in item.attrib:
                        rowspans_count[i] = int( item.attrib['rowspan'] )
                    if name in TARGET_TABLE_ITEM_PARSER:
                        f = TARGET_TABLE_ITEM_PARSER[name]
                        record[name] = f( item )
                    else:
                        record[name] = parse_item_default( item )
                    x += 1
            validate_with_msg( validate_record( record ), ERROR_CODE_INVALID_RECORD_FOUND, record )
            prev_record = record
            formalized_record = formalize_record( record )
            validate( save_record( formalized_record ), ERROR_CODE_FAILED_TO_SAVE )
            rowspans_count = map( (lambda n: n-1), rowspans_count )

# main
map( scrap, TARGET_URLS )