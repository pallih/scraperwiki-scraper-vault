# coding: utf-8
import scraperwiki
import re, urlparse, datetime
import requests
from bs4 import BeautifulSoup as BS

BASE = 'http://www1.kaiho.mlit.go.jp'
DATA_URL = 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsonlist&name=kaiho-wabun&query=select%20id%20from%20swdata'
history = requests.get(DATA_URL).json().get('data')
if history == None:
    history = []

TYPES = [u'日本航行警報', 'NAVAREA', 'NAVTEX', u'地域航行警報', u'地域航行警報']
'''
OFFICES = ['',
    ['', '函館', '室蘭', '釧路', '根室', '紋別', '稚内', '留萌', '小樽'],
    ['', '酒田', '秋田', '青森', '八戸', '釜石', '宮城', '福島'],
    ['', '茨城', '銚子', '千葉', '東京', '横浜', '横須賀', '下田', '清水'],
    ['', '名古屋', '四日市', '鳥羽', '尾鷲'],
    ['', '田辺', '大阪', '神戸', '徳島', '高知', '和歌山', '姫路'],
    ['', '玉野', '水島', '尾道', '高松', '今治', '呉', '広島', '徳山', '松山', '宇和島'],
    ['', '仙崎', '大分', '門司', '若松', '福岡', '唐津', '対馬', '佐世保', '長崎', '三池'],
    ['', '浜田', '境', '舞鶴', '敦賀'],
    ['', '金沢', '七尾', '伏木', '新潟'],
    ['', '熊本', '串木野', '鹿児島', '宮崎', '奄美'],
    ['十一本部', '石垣', '中城', '那覇']
]


group(1): 種別 (0: 日本航行警報, 1: NAVAREA, 2: NAVTEX, 3: 地域航行警報(本部), 4: 地域航行警報(その他)
group(2): 管区番号（地域航行警報）
group(3): 部署番号（地域航行警報）
group(4): 年（下2桁）
group(5): 番号
'''
re_id = re.compile(r'(\d)-(\d{0,2})(\d{0,2})(\d{2})(\d{4})')

s = requests.Session()

r = s.get(BASE + '/TUHO/tuho/cgi/skat/map.cgi?1&ALL&0')
r.encoding = 'EUC-JP'
soup = BS(r.text)


for tr in [cb.findParent('tr') for cb in soup('input', type='checkbox')]:
    id = tr.td.input["value"]
    if not [id] in history:
        data = {'id': id,
            'type': int(re_id.match(id).group(1)),
            'year': 2000 + int(re_id.match(id).group(4)),
            'number': int(re_id.match(id).group(5)),
            'subtype': tr('td')[-2].text.replace(' ', '').replace(u'　',''), 
            'subject': tr.a.text,
            'url': urlparse.urljoin(BASE, tr.a['href'])}

        r = s.get(data['url'])
        r.encoding = 'EUC-JP'

        data['type_name'] = TYPES[data['type']]

        header = data['type_name']
        if data['type'] in (3, 4):
            data['rcg'] = int(re_id.match(id).group(2))
            if data['type'] == 4:
                data['office'] = int(re_id.match(id).group(3))
                data['office_name'] = tr('td')[2].text
            else:
                data['office'] = 0
                data['office_name'] = u'本部'
            header += u' 第%(rcg)d管区%(office_name)s' % data
        header += u' %(number)04d %(subtype)s' % data
        
        data['title'] = u'【%s】%s' % (header, data['subject'])
        
        soup = BS(r.text)
        data['body'] = ''.join([col for col in soup('strong')[-1].next.find_all_next(text=True)])

        data['date_scraped'] =  datetime.datetime.now()
    
        scraperwiki.sqlite.save(unique_keys=['url'], data=data) 
