import scrapemark, time, datetime, math
 
def dateToUnixtime(date):
    time_format = '%Y-%m-%d'
    return time.mktime(time.strptime(date, time_format))
 
def scrapeEpisodes(url):
    return scrapemark.scrape("""
        {*
        <td class="summary">"<b>{{ [episode].name }}</b>"</td>
        <span class="bday dtstart published updated">{{ [episode].date }}</span>
        *}
        """,
        url=url)
 
def episodeNumber(epn, maxn, series):
    epnr = epn%maxn
    if epnr == 0: epnr = maxn
    epnr = str(epnr).zfill(2)
 
    # The pilot was a double-episode
    if epn < 3 and series == 'SGA': epnr = '01E02'
 
    return 'E'+epnr
 
def seasonNumber(epn, maxn, pad = 0):
    return 'S'+str(int(math.ceil(float(epn) / maxn)) + pad).zfill(2)
 
episodes = []
 
SG1episodes = scrapeEpisodes('http://en.wikipedia.org/wiki/List_of_Stargate_SG-1_episodes')
 
i = 0
for episode in SG1episodes['episode']:
    timestamp = dateToUnixtime(episode['date'])
    i += 1
 
    # The SG-1 seasons got shorter after season 7...
    if i < 22:
        downloadname = 'Stargate.SG1.'+seasonNumber(i, 21)+episodeNumber(i, 21, 'SG-1')
    elif i < 155 and i > 21:
        downloadname = 'Stargate.SG1.'+seasonNumber(i-21, 22, 1)+episodeNumber(i-21, 22, 'SG-1')
    else:
        downloadname = 'Stargate.SG1.'+seasonNumber(i-154, 20, 7)+episodeNumber(i-154, 20, 'SG-1')
 
    episodes.append({'name' : episode['name'], 'airdate' : episode['date'], 'timestamp' : timestamp, 'downloadname' : downloadname})
 
SGAepisodes = scrapeEpisodes('http://en.wikipedia.org/wiki/List_of_Stargate_Atlantis_episodes')
 
i = 0
for episode in SGAepisodes['episode']:
    timestamp = dateToUnixtime(episode['date'])
    i += 1
    downloadname = 'Stargate.Atlantis.'+seasonNumber(i, 20)+episodeNumber(i, 20, 'SGA')
    episodes.append({'name' : episode['name'], 'airdate' : episode['date'], 'timestamp' : timestamp, 'downloadname' : downloadname})
 
episodes = sorted(episodes, key=lambda ep: ep['timestamp'])
 
i = 0
print '<table>'
print '<tr><td>#</td><td>Name</td><td>Download Name</td><td>Air date</td></tr>'
for episode in episodes:
    i += 1
    print '<tr><td>'+str(i)+'</td><td>'+episode['name']+'</td><td>'+episode['downloadname']+'</td><td>'+episode['airdate']+'</td></tr>'
print '</table>'
import scrapemark, time, datetime, math
 
def dateToUnixtime(date):
    time_format = '%Y-%m-%d'
    return time.mktime(time.strptime(date, time_format))
 
def scrapeEpisodes(url):
    return scrapemark.scrape("""
        {*
        <td class="summary">"<b>{{ [episode].name }}</b>"</td>
        <span class="bday dtstart published updated">{{ [episode].date }}</span>
        *}
        """,
        url=url)
 
def episodeNumber(epn, maxn, series):
    epnr = epn%maxn
    if epnr == 0: epnr = maxn
    epnr = str(epnr).zfill(2)
 
    # The pilot was a double-episode
    if epn < 3 and series == 'SGA': epnr = '01E02'
 
    return 'E'+epnr
 
def seasonNumber(epn, maxn, pad = 0):
    return 'S'+str(int(math.ceil(float(epn) / maxn)) + pad).zfill(2)
 
episodes = []
 
SG1episodes = scrapeEpisodes('http://en.wikipedia.org/wiki/List_of_Stargate_SG-1_episodes')
 
i = 0
for episode in SG1episodes['episode']:
    timestamp = dateToUnixtime(episode['date'])
    i += 1
 
    # The SG-1 seasons got shorter after season 7...
    if i < 22:
        downloadname = 'Stargate.SG1.'+seasonNumber(i, 21)+episodeNumber(i, 21, 'SG-1')
    elif i < 155 and i > 21:
        downloadname = 'Stargate.SG1.'+seasonNumber(i-21, 22, 1)+episodeNumber(i-21, 22, 'SG-1')
    else:
        downloadname = 'Stargate.SG1.'+seasonNumber(i-154, 20, 7)+episodeNumber(i-154, 20, 'SG-1')
 
    episodes.append({'name' : episode['name'], 'airdate' : episode['date'], 'timestamp' : timestamp, 'downloadname' : downloadname})
 
SGAepisodes = scrapeEpisodes('http://en.wikipedia.org/wiki/List_of_Stargate_Atlantis_episodes')
 
i = 0
for episode in SGAepisodes['episode']:
    timestamp = dateToUnixtime(episode['date'])
    i += 1
    downloadname = 'Stargate.Atlantis.'+seasonNumber(i, 20)+episodeNumber(i, 20, 'SGA')
    episodes.append({'name' : episode['name'], 'airdate' : episode['date'], 'timestamp' : timestamp, 'downloadname' : downloadname})
 
episodes = sorted(episodes, key=lambda ep: ep['timestamp'])
 
i = 0
print '<table>'
print '<tr><td>#</td><td>Name</td><td>Download Name</td><td>Air date</td></tr>'
for episode in episodes:
    i += 1
    print '<tr><td>'+str(i)+'</td><td>'+episode['name']+'</td><td>'+episode['downloadname']+'</td><td>'+episode['airdate']+'</td></tr>'
print '</table>'
