import scraperwiki
from BeautifulSoup import BeautifulSoup
from pytz import timezone
from datetime import datetime
television = {
    'rai 1':'http://www.staseraintv.com/programmi_stasera_rai1.html',
    'rai 2':'http://www.staseraintv.com/programmi_stasera_rai2.html',
    'rai 3':'http://www.staseraintv.com/programmi_stasera_rai3.html',
    'rai 4':'http://www.staseraintv.com/programmi_stasera_rai4.html',
    'rai 5':'http://www.staseraintv.com/programmi_stasera_rai5.html',
    'rai premium':'http://www.staseraintv.com/programmi_stasera_rai_premium.html',
    'rai movie':'http://www.staseraintv.com/programmi_stasera_rai_sat_cinema.html',
    'rai sport 1':'http://www.staseraintv.com/programmi_stasera_rai_sport_1.html',
    'canale 5':'http://www.staseraintv.com/programmi_stasera_canale5.html',
    'rete 4':'http://www.staseraintv.com/programmi_stasera_rete4.html',
    'iris':'http://www.staseraintv.com/programmi_stasera_iris.html',
    'la 5':'http://www.staseraintv.com/programmi_stasera_la5.html',
    'mediaset extra':'http://www.staseraintv.com/programmi_stasera_mediaset_extra.html',
    'sportitalia':'http://www.staseraintv.com/programmi_stasera_sportitalia.html',
    'cielo':'http://www.staseraintv.com/programmi_stasera_cielo.html',
    'italia 1':'http://www.staseraintv.com/programmi_stasera_italia1.html',
    'italia 2':'http://www.staseraintv.com/programmi_stasera_italia2.html',
    'mtv':'http://www.staseraintv.com/programmi_stasera_mtv.html',
    'la 7':'http://www.staseraintv.com/programmi_stasera_la7.html',
    'la 7D':'http://www.staseraintv.com/programmi_stasera_la7d.html'

}
day = datetime.now(timezone('Europe/Rome')).strftime('%Y-%m-%d')
sourcedata = 'italian_tv_schedules'
for tv in television.keys():
    html = scraperwiki.scrape(television[tv])
    soup = BeautifulSoup(html)
    tds = soup.findAll('table')[4].findAll('tr')[0].findAll('td')
    schedule_table = tds[len(tds)-1].findAll('small')
    schedule = schedule_table[len(schedule_table)-1]
    for s in schedule:
        v = str(s).replace('\r\n','')
        if (v.find(' - ') > 1):
            info = v.split(' - ')
            if (len(info) > 2):
                what = ""
                for i in range(len(info)):
                    if (i > 1):
                        what += " - " + info[i]
                    else:
                        if (i == 1):
                            what += info[i]
            else:
                what = info[1]
            begin = str(info[0])
            begin = begin.split(">")
            bi = 0
            if len(begin) == 2:
                bi = 1   
            begin = str(begin[bi])
            id = tv + " " + str(begin[bi]) + " " + str(day)
            (hour,minutes) = begin.split(':')
            data = {
                'id' : id,
                'tv' : tv,
                'day' : day,
                'begin' : begin,
                'hour': int(hour),
                'minutes': int(minutes),
                'gender' : "",
                'what' :  what
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=data,table_name='tvschedules')

