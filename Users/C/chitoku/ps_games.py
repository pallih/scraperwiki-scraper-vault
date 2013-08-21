import scraperwiki           
import lxml.html

list_url ="http://us.playstation.com/ps-products/BrowseGames?MaxReleaseDateValue=1&MinReleaseDateValue=6&sortOrder=rDatenf&console=ps3&recordsOnPage=2000"

def parse_title_page(url):

    entry = {}
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect("div[id='content'] h1"):
        entry["title"] = el.text
    
    for el in root.cssselect("img.cover"):
        entry["cover_img"] = el.attrib['src']
    
    count = 0
    attribute = ['genre', 'publisher', 'platform', 'release_date', 'players', 'max_online_players', '3d', 'esrb_img', 'esrb_comment']
    for el in root.cssselect("dl"):
        for header in el.cssselect("dd"):
            if count < 7:
                entry[attribute[count]] = header.text
                count += 1
            else:
                entry['esrb_img'] = header.cssselect("img").pop(0).attrib['src']
                esrb_comment = ""
                for li in header.cssselect("li"):
                    esrb_comment += li.text + ","
                entry['esrb_comment'] = esrb_comment 
    
    for el in root.cssselect("div[id='playstationmove']"):
        html =  lxml.html.tostring(el)
        line_required    = html.find("Required Accessories") 
        line_compatible  = html.find("Compatible Accessories") 
        line_move_motion     = html.find("ps_move_motion_controller_img.png")
        line_move_navigation = html.find("ps_move_navigation_img.png")
        line_eye             = html.find("ps_move_eye_img.png")
        line_shooter         = html.find("sharp_shooter.png")
    
        if line_required != -1 :
            if line_required < line_move_motion :
                entry['p_move_motion'] = 2 # Required
            if line_required < line_move_navigation :
                entry['p_move_navigation'] = 2 # Required
            if line_required < line_eye :
                entry['p_eye'] = 2 # Required
            if line_required < line_shooter:
                entry['p_shooter'] = 2 # Required
    
        if line_compatible != -1 :
            if line_compatible < line_move_motion :
                entry['p_move_motion'] = 1 # Compatible
            if line_compatible < line_move_navigation :
                entry['p_move_navigation'] = 1 # Compatible
            if line_compatible < line_eye :
                entry['p_eye'] = 1 # Compatible
            if line_compatible < line_shooter:
                entry['p_shooter'] = 1 # Compatible
    
    entry['url'] = url
    
    return entry


###########################################################
#                      Main routine                       #
###########################################################

#scraperwiki.sqlite.execute("drop table if exists titles")

#scraperwiki.sqlite.execute("CREATE TABLE `titles` (`title` text, `cover_img` text, `genre` text, `publisher` text, `platform` text, `release_date` text, `players` text, `max_online_players` text, `3d` text, `esrb_img` text, `esrb_comment` text, `p_move_motion` INTEGER, `p_move_navigation` INTEGER, `p_eye` INTEGER, `p_shooter` INTEGER, `url` text)")

html = scraperwiki.scrape(list_url)
root = lxml.html.fromstring(html)

for el in root.cssselect("h6 a"):
    print el.attrib['href']
    entry = parse_title_page(el.attrib['href'])
    scraperwiki.sqlite.save(["url"], entry, "titles")   
