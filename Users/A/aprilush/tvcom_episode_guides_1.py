import scraperwiki
import lxml.html
import dateutil.parser         
import datetime

def get_info(link):
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    
    info = {}
    
    name = root.cssselect("h1[itemprop='name']")[0].text
    info['name']=name
    
    seasons = []
    current_season = 0
    div = root.cssselect("div[class='m episode_list  _standard_module all_expanded']")[0]
    for season_el in div.cssselect("li[class~='season']"):  
        season_no = season_el.get('data-season')
        if season_no > current_season:
            current_season = season_no
        season = {}
        season["number"] = season_no
        if season_el.get('class').find("toggled") > 0:
            episode_list = []
            for ep in season_el.cssselect("li[class~='episode']"):
                title_el = ep.cssselect("a[class='title']")[0]
                title = title_el.text
                url = "www.tv.com" + title_el.get('href')
                info_el = ep.cssselect("div[class='ep_info']")[0]
                ep_no = info_el.text.strip().split()[1]
                date_el = ep.cssselect("div[class='date']")[0]
                when = dateutil.parser.parse(date_el.text, dayfirst=False).date()
                desc_el = ep.cssselect("div[class='description']")[0]
                descr = desc_el.text_content()
                episode = {}
                episode['season'] = season_no
                episode['number'] = ep_no
                episode['title'] = title
                episode['date'] = when
                episode['url'] = url
                episode['description'] = descr
                episode_list.append(episode)
            season['episodes'] = episode_list
        seasons.append(season)
    info['seasons'] = seasons
    return info    


def get_prev_episodes(infos, how_many):
    today = datetime.date.today()
    out = []
    for info in infos:
        found = 0
        show = info['name']
        for season in info['seasons']:
            if 'episodes' in season:
                for ep in season['episodes']:
                    if found < how_many:
                        if ep['date'] < today:
                            out.append([show,ep])
                            found = found+1
    return out


def double_digits(n):
    if int(n)<10:
        s = "0"+str(n)
        return s
    else:
        return str(n)

def make_html(infos):
    date = datetime.date.today()
    episodes = get_prev_episodes(infos, 1)
    html = "<html><body><table border='1'>"
    for [show, prev] in episodes:
        html += "<tr><td>"+show+"</td><td>s"+double_digits(prev['season'])+"e"+double_digits(prev['number'])+" </td><td><a href='"+prev['url']+"'>"+prev['title']+"</a></td><td>"+str(prev['date'])+"</td><td>"+prev['description'][0:80]+"</td></tr>"
    html += "</table></body></html>"
    return html


links = ["http://www.tv.com/shows/ncis/episodes/", "http://www.tv.com/shows/ncis-los-angeles/episodes", "http://www.tv.com/shows/nikita/episodes/", "http://www.tv.com/shows/bones/episodes/", "http://www.tv.com/shows/the-mentalist/episodes/", "http://www.tv.com/shows/hawaii-five-0/episodes/", "http://www.tv.com/shows/covert-affairs/episodes/", "http://www.tv.com/shows/fringe/episodes/", "http://www.tv.com/shows/blue-bloods/episodes/"]

infos = []
for link in links:
    infos.append(get_info(link))
print make_html(infos)


import scraperwiki
import lxml.html
import dateutil.parser         
import datetime

def get_info(link):
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    
    info = {}
    
    name = root.cssselect("h1[itemprop='name']")[0].text
    info['name']=name
    
    seasons = []
    current_season = 0
    div = root.cssselect("div[class='m episode_list  _standard_module all_expanded']")[0]
    for season_el in div.cssselect("li[class~='season']"):  
        season_no = season_el.get('data-season')
        if season_no > current_season:
            current_season = season_no
        season = {}
        season["number"] = season_no
        if season_el.get('class').find("toggled") > 0:
            episode_list = []
            for ep in season_el.cssselect("li[class~='episode']"):
                title_el = ep.cssselect("a[class='title']")[0]
                title = title_el.text
                url = "www.tv.com" + title_el.get('href')
                info_el = ep.cssselect("div[class='ep_info']")[0]
                ep_no = info_el.text.strip().split()[1]
                date_el = ep.cssselect("div[class='date']")[0]
                when = dateutil.parser.parse(date_el.text, dayfirst=False).date()
                desc_el = ep.cssselect("div[class='description']")[0]
                descr = desc_el.text_content()
                episode = {}
                episode['season'] = season_no
                episode['number'] = ep_no
                episode['title'] = title
                episode['date'] = when
                episode['url'] = url
                episode['description'] = descr
                episode_list.append(episode)
            season['episodes'] = episode_list
        seasons.append(season)
    info['seasons'] = seasons
    return info    


def get_prev_episodes(infos, how_many):
    today = datetime.date.today()
    out = []
    for info in infos:
        found = 0
        show = info['name']
        for season in info['seasons']:
            if 'episodes' in season:
                for ep in season['episodes']:
                    if found < how_many:
                        if ep['date'] < today:
                            out.append([show,ep])
                            found = found+1
    return out


def double_digits(n):
    if int(n)<10:
        s = "0"+str(n)
        return s
    else:
        return str(n)

def make_html(infos):
    date = datetime.date.today()
    episodes = get_prev_episodes(infos, 1)
    html = "<html><body><table border='1'>"
    for [show, prev] in episodes:
        html += "<tr><td>"+show+"</td><td>s"+double_digits(prev['season'])+"e"+double_digits(prev['number'])+" </td><td><a href='"+prev['url']+"'>"+prev['title']+"</a></td><td>"+str(prev['date'])+"</td><td>"+prev['description'][0:80]+"</td></tr>"
    html += "</table></body></html>"
    return html


links = ["http://www.tv.com/shows/ncis/episodes/", "http://www.tv.com/shows/ncis-los-angeles/episodes", "http://www.tv.com/shows/nikita/episodes/", "http://www.tv.com/shows/bones/episodes/", "http://www.tv.com/shows/the-mentalist/episodes/", "http://www.tv.com/shows/hawaii-five-0/episodes/", "http://www.tv.com/shows/covert-affairs/episodes/", "http://www.tv.com/shows/fringe/episodes/", "http://www.tv.com/shows/blue-bloods/episodes/"]

infos = []
for link in links:
    infos.append(get_info(link))
print make_html(infos)


