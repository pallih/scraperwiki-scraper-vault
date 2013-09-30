import scraperwiki
import lxml.html
import dateutil.parser         
import datetime

def get_info(link):
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    
    info = []
    
    name = root.cssselect("h1[itemprop='name']")[0].text
    info.append({'name':name})
    
    current_season = 0
    for div in root.cssselect("div[class='m episode_list  _standard_module all_expanded']"):
        for season in div.cssselect("li[class~='season']"):  
            season_no = season.get('data-season')
            if season_no > current_season:
                current_season = season_no
            if season.get('class').find("toggled") > 0:
                episode_list = []
                for ep in season.cssselect("li[class~='episode']"):
                    title_el = ep.cssselect("a[class='title']")[0]
                    title = title_el.text
                    url = "www.tv.com" + title_el.get('href')
                    info_el = ep.cssselect("div[class='ep_info']")[0]
                    ep_no = info_el.text.strip().split()[1]
                    date_el = ep.cssselect("div[class='date']")[0]
                    when = dateutil.parser.parse(date_el.text, dayfirst=False).date()
                    desc_el = ep.cssselect("div[class='description']")[0]
                    descr = desc_el.text_content()
                    episode = {'season':season_no, 'number':ep_no, 'title':title, 'date':when, 'url':url, 'description':descr}
                    episode_list.append(episode)
            info.append({season_no: episode_list})
    return info    

links = ["http://www.tv.com/shows/ncis/episodes/", "http://www.tv.com/shows/ncis-los-angeles/episodes", "http://www.tv.com/shows/nikita/episodes/", "http://www.tv.com/shows/bones/episodes/", "http://www.tv.com/shows/the-mentalist/episodes/", "http://www.tv.com/shows/hawaii-five-0/episodes/", "http://www.tv.com/shows/covert-affairs/episodes/", "http://www.tv.com/shows/fringe/episodes/", "http://www.tv.com/shows/blue-bloods/episodes/"]

for link in links:
    print repr(get_info(link))
import scraperwiki
import lxml.html
import dateutil.parser         
import datetime

def get_info(link):
    html = scraperwiki.scrape(link)
    root = lxml.html.fromstring(html)
    
    info = []
    
    name = root.cssselect("h1[itemprop='name']")[0].text
    info.append({'name':name})
    
    current_season = 0
    for div in root.cssselect("div[class='m episode_list  _standard_module all_expanded']"):
        for season in div.cssselect("li[class~='season']"):  
            season_no = season.get('data-season')
            if season_no > current_season:
                current_season = season_no
            if season.get('class').find("toggled") > 0:
                episode_list = []
                for ep in season.cssselect("li[class~='episode']"):
                    title_el = ep.cssselect("a[class='title']")[0]
                    title = title_el.text
                    url = "www.tv.com" + title_el.get('href')
                    info_el = ep.cssselect("div[class='ep_info']")[0]
                    ep_no = info_el.text.strip().split()[1]
                    date_el = ep.cssselect("div[class='date']")[0]
                    when = dateutil.parser.parse(date_el.text, dayfirst=False).date()
                    desc_el = ep.cssselect("div[class='description']")[0]
                    descr = desc_el.text_content()
                    episode = {'season':season_no, 'number':ep_no, 'title':title, 'date':when, 'url':url, 'description':descr}
                    episode_list.append(episode)
            info.append({season_no: episode_list})
    return info    

links = ["http://www.tv.com/shows/ncis/episodes/", "http://www.tv.com/shows/ncis-los-angeles/episodes", "http://www.tv.com/shows/nikita/episodes/", "http://www.tv.com/shows/bones/episodes/", "http://www.tv.com/shows/the-mentalist/episodes/", "http://www.tv.com/shows/hawaii-five-0/episodes/", "http://www.tv.com/shows/covert-affairs/episodes/", "http://www.tv.com/shows/fringe/episodes/", "http://www.tv.com/shows/blue-bloods/episodes/"]

for link in links:
    print repr(get_info(link))
