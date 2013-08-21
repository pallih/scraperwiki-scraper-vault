# -*- coding: utf-8 -*
from BeautifulSoup import BeautifulSoup,NavigableString
import urllib2,urllib,sys,re


# - Skilgreinum fasta

start_url = 'http://www.ksi.is/mot/motalisti/leikskyrsla/?Leikur='
user_agent = 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
headers = { 'User-Agent' : user_agent }
headerdata =''

# - Dictionary til að geyma grunnupplýsingar um leikinn
info = {}

# - Listi til að lista með leikmönnum byrjunarlið heimaliðs 
byrjun_heimalid = []

# - Listi til að lista með leikmönnum byrjunarlið heimaliðs 
byrjun_utilid = []

# - Definition til að extracta streng ef við vitum tákn til beggja hliða
def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]


# - Sækjum leikskyrslu og vinnum úr henni

def scrape_leikur(numer):
    url = start_url + numer
    
    #Saekjum med urllib2

    req = urllib2.Request(url, headerdata, headers)
    response = urllib2.urlopen(req)
    html = response.read()

    soup = BeautifulSoup(html)
    soup.prettify()

    
    # - Fyrst eru hér upplýsingar um lið - úrslit - dagsetningu og tíma - það er allt innan <ul> með class=metadata
    
    metadata = soup.find('ul', {'class':'metadata'})

    # - Svo vinnum við okkur áfram með regex og split æfingum - eflaust má gera þetta hraðar en ég er bara ekki klárari en þetta :)

    mot = re.sub('M.+:','',metadata.contents[1].text)
    lid = extract(metadata.contents[3].text, "Leikur:","&nbsp;")
    urslit = extract(metadata.contents[3].text, "&nbsp;","&nbsp;")
    heimalid = lid.split(' - ')[0]
    utilid = lid.split(' - ')[1]
    timasetningar = metadata.contents[5].text.split('-')
    leikdagur = re.sub('Leikdagur:','',timasetningar[0])
    timi = re.sub('&nbsp;','',timasetningar[1])
    stadur = re.sub('&nbsp;','',timasetningar[2])
    ahorfendur = re.sub('&nbsp;\xc1horfendur:','',timasetningar[3])
    
    # - Setjum allt í dictionary-ið

    info['mot'] = mot
    info['leiknumer'] = numer
    info['ahorfendur'] = ahorfendur
    info['stadur'] = stadur
    info['leikdagur'] = leikdagur
    info['timi'] = timi
    info['lid'] = lid
    info['source_url'] = url
    info['heimalid'] = heimalid
    info['utilid'] = utilid
    info['urslit'] = urslit
    
    # - Nú er allt fyrsta efnið komið í dictionary-ið. Við getum nálgast það þar auðveldlega (u fyrir framan streng gefur til kynna utf-8 í python)
    
    #print u'Þann ' + info['leikdagur'] + 'klukkan' + info['timi'] + u' mættust ' + info['heimalid'] + ' og ' + info['utilid'] + u'. Leikurinn fór ' + info['urslit']

     # - o.s.frv. Athuga að þetta er ekki mjög efficient leið til að joina strengi, sbr: http://skymind.com/~ocrow/python_string/

    # - Svo höldum við áfram. Næst eru leikmenn í byrjunarliði - við getum gefið okkur að þeir eru alltaf 11 í hvoru liði (reikna ég með!)

    adal_efni = soup.find('table', {'width':'570'})
    # - Þetta er súperleim, en ég nenni ekki að gera þetta öðruvísi for now
    byrjunarlid = extract(str(adal_efni),"Byrjunarlið</th></tr>",'<tr><td>&nbsp;</td></tr><tr><th>&nbsp;</th><th colspan="7" width="100%">Varamenn</th></tr>')
    print adal_efni
    byrjunarlid = BeautifulSoup(byrjunarlid)
    trs = byrjunarlid.findAll('tr')
    for tr in trs:
        # - Heimalið 
        heimalid_nr =  re.sub('&nbsp;','',tr.contents[1].text)
        heimalid_nafn = re.sub('&nbsp;','',tr.contents[3].text)
        heimalid_leikmadur_info_url = 'http://www.ksi.is/mot/motalisti' + re.sub('\..','',tr.a['href'])
        heimalid_leikmadur = [heimalid_nr,heimalid_nafn,heimalid_leikmadur_info_url]
        byrjun_heimalid.append(heimalid_leikmadur)
        
        # - Útilið
        utilid_nr =  re.sub('&nbsp;','',tr.contents[7].text)
        utilid_nafn = re.sub('&nbsp;','',tr.contents[9].text)
        utilid_leikmadur_info_url = 'http://www.ksi.is/mot/motalisti' + re.sub('\..','',tr.a.findNext('a')['href'])
        utilid_leikmadur = [utilid_nr,utilid_nafn,utilid_leikmadur_info_url]
        byrjun_utilid.append(utilid_leikmadur)
        
        # - Þá erum við komnir með tvo lista af byrjunarliðum, hver með númeri, nafni og slóð á nánara info (uppá framtíðina ...)        

    print byrjun_heimalid
    print byrjun_utilid
        
        # - Og getum nálgast það svona t.d.

    #for t in byrjun_heimalid:
    #    print 'nr: ' + t[0] + ', nafn: ' + t[1] + u', slóð: ' + t[2]

scrape_leikur("229446")