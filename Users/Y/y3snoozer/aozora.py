# coding: utf-8

import scraperwiki
import zipfile
import urllib2
import StringIO
import csv
import datetime
import time

def column_name(label=None):
    c = {
        u'作品ID': 'book_id',
        u'作品名': 'book_title',
        u'作品名読み': 'book_yomi',
        u'ソート用読み': 'book_sort',
        u'副題': 'book_sub_title',
        u'副題読み': 'book_sub_yomi',
        u'原題': 'book_original_title',
        u'初出': 'first_appearance',
        u'分類番号': 'sort_code',
        u'文字遣い種別': 'orthography',
        u'作品著作権フラグ': 'book_copyright_flag',
        u'公開日': 'release_date',
        u'最終更新日': 'last_update',
        u'図書カードURL': 'bookcard_url',
        u'人物ID': 'person_id',
        u'姓': 'person_sur_name',
        u'名': 'person_given_name',
        u'姓読み': 'person_sur_yomi',
        u'名読み': 'person_given_yomi',
        u'姓読みソート用': 'person_sur_sort',
        u'名読みソート用': 'person_given_sort',
        u'姓ローマ字': 'person_sur_romaji',
        u'名ローマ字': 'person_given_romaji',
        u'役割フラグ': 'person_role_flag',
        u'生年月日': 'person_birthday',
        u'没年月日': 'person_deathday',
        u'人物著作権フラグ': 'person_copyright_flag',
        u'底本名1': 'original_title_1',
        u'底本出版社名1': 'original_publisher_1',
        u'底本初版発行年1': 'original_firstprinting_date_1',
        u'入力に使用した版1': 'original_edition_for_input_1',
        u'校正に使用した版1': 'original_edition_for_proof_1',
        u'底本の親本名1': 'original_book_title_1',
        u'底本の親本出版社名1': 'original_book_publisher_1',
        u'底本の親本初版発行年1': 'original_book_firstprinting_date_1',
        u'底本名2': 'original_title_2',
        u'底本出版社名2': 'original_publisher_2',
        u'底本初版発行年2': 'original_firstprinting_date_2',
        u'入力に使用した版2': 'original_edition_for_input_2',
        u'校正に使用した版2': 'original_edition_for_proof_2',
        u'底本の親本名2': 'original_book_title_2',
        u'底本の親本出版社名2': 'original_book_publisher_2',
        u'底本の親本初版発行年2': 'original_book_firstprinting_date_2',
        u'入力者': 'keyboarder',
        u'校正者': 'proofreader',
        u'テキストファイルURL': 'text_url',
        u'テキストファイル最終更新日': 'text_last_update',
        u'テキストファイル符号化方式': 'text_encoding',
        u'テキストファイル文字集合': 'text_charset',
        u'テキストファイル修正回数': 'text_modified_count',
        u'XHTML/HTMLファイルURL': 'xhtml_url',
        u'XHTML/HTMLファイル最終更新日': 'xhtml_last_update',
        u'XHTML/HTMLファイル符号化方式': 'xhtml_encoding',
        u'XHTML/HTMLファイル文字集合': 'xhtml_charset',
        u'XHTML/HTMLファイル修正回数': 'xhtml_modified_count',
    }
    if label:
        return c[label]
    return c

url = 'http://www.aozora.gr.jp/index_pages/list_person_all_extended.zip'
filename = 'list_person_all_extended.csv'

int_properties = ['text_modified_count', 'xhtml_modified_count']

book_columns = [
    'book_id', 'book_title', 'book_yomi', 'book_sort',
    'book_sub_title', 'book_sub_yomi', 'book_original_title',
    'first_appearance', 'sort_code', 'orthography',
    'book_copyright_flag', 'release_date', 'last_update',
    'bookcard_url', 'keyboarder', 'proofreader',
    'text_url', 'text_last_update', 'text_encoding', 'text_charset', 'text_modified_count',
    'xhtml_url', 'xhtml_last_update', 'xhtml_encoding', 'xhtml_charset', 'xhtml_modified_count']
person_columns = [
    'person_id', 'person_sur_name', 'person_given_name', 'person_sur_yomi', 'person_given_yomi',
    'person_sur_sort', 'person_given_sort', 'person_sur_romaji', 'person_given_romaji',
    'person_birthday', 'person_deathday', 'person_copyright_flag']
author_columns = ['person_id', 'person_role_flag', 'book_id']
original_1_columns = [
    'original_title_1', 'original_publisher_1', 'original_firstprinting_date_1',
    'original_edition_for_input_1', 'original_edition_for_proof_1', 'original_book_title_1',
    'original_book_publisher_1', 'original_book_firstprinting_date_1']
original_2_columns = [
    'original_title_2', 'original_publisher_2', 'original_firstprinting_date_2',
    'original_edition_for_input_2', 'original_edition_for_proof_2', 'original_book_title_2',
    'original_book_publisher_2', 'original_book_firstprinting_date_2']

remotehandle = urllib2.urlopen(url) 
zipdata = StringIO.StringIO(remotehandle.read()) 
remotehandle.close() 
archive = zipfile.ZipFile(zipdata)
csvdata = archive.read(filename)
csvdata_unicode = csvdata.decode('cp932')
csvdata_utf8 = csvdata_unicode.encode('utf8').split('\r\n')
reader = csv.reader(csvdata_utf8)

label = []
label_flag = False
author_count = {}
#for n, row in enumerate(reader):
for row in reader:
    if not label_flag:
        for col in row:
            label.append(unicode(col, 'utf8'))
        label_flag = True
        continue
    bookdata = {}
    persondata = {}
    authordata = {}
    original_1_data = {}
    original_2_data = {}
    for i, col in enumerate(row):
        coldata = unicode(col, 'utf8')
        colname = column_name(label[i])
        if colname in int_properties:
            if col: coldata = int(col)
            else: coldata = None
        if colname in book_columns:
            bookdata[colname] = coldata
        if colname in person_columns:
            persondata[colname] = coldata
        if colname in author_columns:
            authordata[colname] = coldata
        if colname in original_1_columns and coldata:
            original_1_data[colname[:-2]] = coldata
        if colname in original_2_columns and coldata:
            original_2_data[colname[:-2]] = coldata

    if bookdata:
        scraperwiki.sqlite.save(unique_keys=['book_id'], data=bookdata, table_name='books')
        if original_1_data:
            original_1_data['book_id'] = bookdata['book_id']
            original_1_data['uid'] = bookdata['book_id']+'_1'
            scraperwiki.sqlite.save(unique_keys=['uid'], data=original_1_data, table_name='originals')
        if original_2_data:
            original_2_data['book_id'] = bookdata['book_id']
            original_2_data['uid'] = bookdata['book_id']+'_2'
            scraperwiki.sqlite.save(unique_keys=['uid'], data=original_2_data, table_name='originals')
    if persondata:
        persondata['person_full_name'] = persondata['person_sur_name']+persondata['person_given_name']
        persondata['person_full_yomi'] = persondata['person_sur_yomi']+persondata['person_given_yomi']
        scraperwiki.sqlite.save(unique_keys=['person_id'], data=persondata, table_name='people')
    if authordata:
        scraperwiki.sqlite.save(unique_keys=['book_id', 'person_id'], data=authordata, table_name='authors')
#    if n >= 100: break# coding: utf-8

import scraperwiki
import zipfile
import urllib2
import StringIO
import csv
import datetime
import time

def column_name(label=None):
    c = {
        u'作品ID': 'book_id',
        u'作品名': 'book_title',
        u'作品名読み': 'book_yomi',
        u'ソート用読み': 'book_sort',
        u'副題': 'book_sub_title',
        u'副題読み': 'book_sub_yomi',
        u'原題': 'book_original_title',
        u'初出': 'first_appearance',
        u'分類番号': 'sort_code',
        u'文字遣い種別': 'orthography',
        u'作品著作権フラグ': 'book_copyright_flag',
        u'公開日': 'release_date',
        u'最終更新日': 'last_update',
        u'図書カードURL': 'bookcard_url',
        u'人物ID': 'person_id',
        u'姓': 'person_sur_name',
        u'名': 'person_given_name',
        u'姓読み': 'person_sur_yomi',
        u'名読み': 'person_given_yomi',
        u'姓読みソート用': 'person_sur_sort',
        u'名読みソート用': 'person_given_sort',
        u'姓ローマ字': 'person_sur_romaji',
        u'名ローマ字': 'person_given_romaji',
        u'役割フラグ': 'person_role_flag',
        u'生年月日': 'person_birthday',
        u'没年月日': 'person_deathday',
        u'人物著作権フラグ': 'person_copyright_flag',
        u'底本名1': 'original_title_1',
        u'底本出版社名1': 'original_publisher_1',
        u'底本初版発行年1': 'original_firstprinting_date_1',
        u'入力に使用した版1': 'original_edition_for_input_1',
        u'校正に使用した版1': 'original_edition_for_proof_1',
        u'底本の親本名1': 'original_book_title_1',
        u'底本の親本出版社名1': 'original_book_publisher_1',
        u'底本の親本初版発行年1': 'original_book_firstprinting_date_1',
        u'底本名2': 'original_title_2',
        u'底本出版社名2': 'original_publisher_2',
        u'底本初版発行年2': 'original_firstprinting_date_2',
        u'入力に使用した版2': 'original_edition_for_input_2',
        u'校正に使用した版2': 'original_edition_for_proof_2',
        u'底本の親本名2': 'original_book_title_2',
        u'底本の親本出版社名2': 'original_book_publisher_2',
        u'底本の親本初版発行年2': 'original_book_firstprinting_date_2',
        u'入力者': 'keyboarder',
        u'校正者': 'proofreader',
        u'テキストファイルURL': 'text_url',
        u'テキストファイル最終更新日': 'text_last_update',
        u'テキストファイル符号化方式': 'text_encoding',
        u'テキストファイル文字集合': 'text_charset',
        u'テキストファイル修正回数': 'text_modified_count',
        u'XHTML/HTMLファイルURL': 'xhtml_url',
        u'XHTML/HTMLファイル最終更新日': 'xhtml_last_update',
        u'XHTML/HTMLファイル符号化方式': 'xhtml_encoding',
        u'XHTML/HTMLファイル文字集合': 'xhtml_charset',
        u'XHTML/HTMLファイル修正回数': 'xhtml_modified_count',
    }
    if label:
        return c[label]
    return c

url = 'http://www.aozora.gr.jp/index_pages/list_person_all_extended.zip'
filename = 'list_person_all_extended.csv'

int_properties = ['text_modified_count', 'xhtml_modified_count']

book_columns = [
    'book_id', 'book_title', 'book_yomi', 'book_sort',
    'book_sub_title', 'book_sub_yomi', 'book_original_title',
    'first_appearance', 'sort_code', 'orthography',
    'book_copyright_flag', 'release_date', 'last_update',
    'bookcard_url', 'keyboarder', 'proofreader',
    'text_url', 'text_last_update', 'text_encoding', 'text_charset', 'text_modified_count',
    'xhtml_url', 'xhtml_last_update', 'xhtml_encoding', 'xhtml_charset', 'xhtml_modified_count']
person_columns = [
    'person_id', 'person_sur_name', 'person_given_name', 'person_sur_yomi', 'person_given_yomi',
    'person_sur_sort', 'person_given_sort', 'person_sur_romaji', 'person_given_romaji',
    'person_birthday', 'person_deathday', 'person_copyright_flag']
author_columns = ['person_id', 'person_role_flag', 'book_id']
original_1_columns = [
    'original_title_1', 'original_publisher_1', 'original_firstprinting_date_1',
    'original_edition_for_input_1', 'original_edition_for_proof_1', 'original_book_title_1',
    'original_book_publisher_1', 'original_book_firstprinting_date_1']
original_2_columns = [
    'original_title_2', 'original_publisher_2', 'original_firstprinting_date_2',
    'original_edition_for_input_2', 'original_edition_for_proof_2', 'original_book_title_2',
    'original_book_publisher_2', 'original_book_firstprinting_date_2']

remotehandle = urllib2.urlopen(url) 
zipdata = StringIO.StringIO(remotehandle.read()) 
remotehandle.close() 
archive = zipfile.ZipFile(zipdata)
csvdata = archive.read(filename)
csvdata_unicode = csvdata.decode('cp932')
csvdata_utf8 = csvdata_unicode.encode('utf8').split('\r\n')
reader = csv.reader(csvdata_utf8)

label = []
label_flag = False
author_count = {}
#for n, row in enumerate(reader):
for row in reader:
    if not label_flag:
        for col in row:
            label.append(unicode(col, 'utf8'))
        label_flag = True
        continue
    bookdata = {}
    persondata = {}
    authordata = {}
    original_1_data = {}
    original_2_data = {}
    for i, col in enumerate(row):
        coldata = unicode(col, 'utf8')
        colname = column_name(label[i])
        if colname in int_properties:
            if col: coldata = int(col)
            else: coldata = None
        if colname in book_columns:
            bookdata[colname] = coldata
        if colname in person_columns:
            persondata[colname] = coldata
        if colname in author_columns:
            authordata[colname] = coldata
        if colname in original_1_columns and coldata:
            original_1_data[colname[:-2]] = coldata
        if colname in original_2_columns and coldata:
            original_2_data[colname[:-2]] = coldata

    if bookdata:
        scraperwiki.sqlite.save(unique_keys=['book_id'], data=bookdata, table_name='books')
        if original_1_data:
            original_1_data['book_id'] = bookdata['book_id']
            original_1_data['uid'] = bookdata['book_id']+'_1'
            scraperwiki.sqlite.save(unique_keys=['uid'], data=original_1_data, table_name='originals')
        if original_2_data:
            original_2_data['book_id'] = bookdata['book_id']
            original_2_data['uid'] = bookdata['book_id']+'_2'
            scraperwiki.sqlite.save(unique_keys=['uid'], data=original_2_data, table_name='originals')
    if persondata:
        persondata['person_full_name'] = persondata['person_sur_name']+persondata['person_given_name']
        persondata['person_full_yomi'] = persondata['person_sur_yomi']+persondata['person_given_yomi']
        scraperwiki.sqlite.save(unique_keys=['person_id'], data=persondata, table_name='people')
    if authordata:
        scraperwiki.sqlite.save(unique_keys=['book_id', 'person_id'], data=authordata, table_name='authors')
#    if n >= 100: break