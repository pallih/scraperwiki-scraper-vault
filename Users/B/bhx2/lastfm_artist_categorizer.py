import scraperwiki
from urllib import quote
from lxml import etree
import dateutil.parser
import re

username = "bharathos"
api_key = "cefce313aa31d3612f8dbd35184a94fc"

artists_page = scraperwiki.scrape("http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&period=1month&api_key="+ api_key + "&user=" + username)
artists = etree.fromstring(artists_page).find("topartists").findall("artist")

artist_entries = []

for artist in artists:
    entry = {}
    entry['name'] = artist.find("name").text
    entry['playcount'] = int(artist.find("playcount").text)
    entry['url'] = artist.find("url").text
    entry['image'] = artist.findall("image")[-1].text
    entry['nationality'] = 'unknown'
    artist_entries.append(entry)

for artist in artist_entries:
    normalized_artist_name = quote(artist['name'].encode('utf-8'))
    artist_page = scraperwiki.scrape("http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&api_key=" + api_key + "&artist=" + normalized_artist_name)
    tags = etree.fromstring(artist_page).find("toptags").findall("tag")

    clean_tags_binary =   {"electronic":0, "indie":0, "alt":0, "pop":0, "rock":0, 
                    "experimental":0, "chill":0, "folk":0, "hip-hop":0, "dance":0,
                    "instrumental":0, "chiptune":0, "singer-songwriter":0, "jazz":0, "funk":0,
                    "ambient":0, "female-vocalist":0, "lo-fi":0, "progressive":0, "shoegaze":0, "house":0, "psychedelic":0, "dubstep":0}
    
    # if there are no tags don't bother saving it, just go on
    if len(tags) == 0:
        continue

    first_five_tags = tags[0:5] 

    clean_tags = []

    for tag in first_five_tags:
        tag = tag.find('name').text
        if re.match('electronic', tag, flags=re.IGNORECASE) and (len(clean_tags) == 0):
            clean_tags.append('electronic')    
        if re.match('indie', tag, flags=re.IGNORECASE) and (len(clean_tags) == 0):
            clean_tags.append('indie')
        if re.match('alt', tag, flags=re.IGNORECASE) and (len(clean_tags) == 0):
            clean_tags.append('alt')
        if re.search('pop', tag, flags=re.IGNORECASE) and (len(clean_tags) < 2):
            clean_tags.append('pop')
        if re.search('rock$', tag, flags=re.IGNORECASE) and (len(clean_tags) < 2):
            clean_tags.append('rock')
        if re.match('experiment', tag, flags=re.IGNORECASE):
            clean_tags.append('experimental')
        if re.match('chill', tag, flags=re.IGNORECASE):
            clean_tags.append('chill')
        if re.match('folk', tag, flags=re.IGNORECASE):
            clean_tags.append('folk')
        if re.search('hip-hop', tag, flags=re.IGNORECASE):
            clean_tags.append('hip-hop')
        if re.match('dance$', tag, flags=re.IGNORECASE):
            clean_tags.append('dance')
        if re.match('instrumental$', tag, flags=re.IGNORECASE):
            clean_tags.append('instrumental')
        if re.match('classical$', tag, flags=re.IGNORECASE):
            clean_tags.append('instrumental')
        if re.match('piano$', tag, flags=re.IGNORECASE):
            clean_tags.append('instrumental')
        if re.match('chiptune', tag, flags=re.IGNORECASE):
            clean_tags.append('chiptune')
        if re.match('singer-songwriter', tag, flags=re.IGNORECASE):
            clean_tags.append('singer-songwriter') 
        if re.match('jazz', tag, flags=re.IGNORECASE):
            clean_tags.append('jazz')
        if re.search('funk$', tag, flags=re.IGNORECASE):
            clean_tags.append('funk')
        if re.match('ambient', tag, flags=re.IGNORECASE):
            clean_tags.append('ambient')
        if re.match('female', tag, flags=re.IGNORECASE):
            clean_tags.append('female-vocalist')
        if re.search('lo-fi$', tag, flags=re.IGNORECASE):
            clean_tags.append('lo-fi')
        if re.match('progress', tag, flags=re.IGNORECASE):
            clean_tags.append('progressive')
        if re.match('shoegaze$', tag, flags=re.IGNORECASE):
            clean_tags.append('shoegaze')
        if re.match('house$', tag, flags=re.IGNORECASE):
            clean_tags.append('house')
        if re.search('psych', tag, flags=re.IGNORECASE):
            clean_tags.append('psychedelic')
        if re.match('dub', tag, flags=re.IGNORECASE):
            clean_tags.append('dubstep')

    for tag in clean_tags:
        clean_tags_binary[tag] = 1

    # Nationality Picker
    nationalities = ['american', 'canadian', 'dutch', 'german', 'british', 'scottish', 
                    'french', 'swedish', 'danish', 'icelandic', 'italian', 'brazilian', 
                    'australian', 'norwegian', 'irish', 'japanese', 'african', 'indian']
    
    found_nationality = False
    for tag_obj in tags:
        tag = tag_obj.find('name').text
        for nationality in nationalities:
            if  tag == nationality:
                artist['nationality'] = nationality
                found_nationality = True
                break
        if found_nationality:
            break
        
    scraperwiki.sqlite.save(unique_keys=['artist'], 
                            data={
                            "artist":artist['name'], 
                            "plays":artist['playcount'], 
                            "link":artist['url'], 
                            "image":artist['image'],
                            "nationality": artist['nationality'],
                            "electronic":clean_tags_binary['electronic'], "indie":clean_tags_binary['indie'],
                            "alt":clean_tags_binary['alt'], "pop":clean_tags_binary['pop'], "rock":clean_tags_binary['rock'],
                            "experimental":clean_tags_binary['experimental'], "chill":clean_tags_binary['chill'],
                            "folk":clean_tags_binary['folk'], "hip-hop":clean_tags_binary['hip-hop'], 
                            "dance":clean_tags_binary['dance'],"instrumental":clean_tags_binary['instrumental'], 
                            "chiptune":clean_tags_binary['chiptune'], "singer-songwriter":clean_tags_binary['singer-songwriter'], 
                            "jazz":clean_tags_binary['jazz'], "funk":clean_tags_binary['funk'], "ambient":clean_tags_binary['ambient'], 
                            "female-vocalist":clean_tags_binary['female-vocalist'], "lo-fi":clean_tags_binary['lo-fi'], 
                            "progressive":clean_tags_binary['progressive'], "shoegaze":clean_tags_binary['shoegaze'], 
                            "house":clean_tags_binary['house'], "psychedelic":clean_tags_binary['psychedelic'], "dubstep":clean_tags_binary['dubstep']
                            })
