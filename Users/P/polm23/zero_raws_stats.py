import scraperwiki
import lxml.html
import re

for offset in range(1,21):
    html = scraperwiki.scrape('http://nyaa.eu/?page=search&cats=0_0&filter=0&term=zero+raws&offset=' + str(offset))
    #print html
    root = lxml.html.fromstring(html)
    for row in root.cssselect('.tlistrow'):
        name = row.cssselect('.tlistname')
        name_text = unicode(name[0].text_content())
        if not name_text[0] == '[': continue
        if re.search(r'Vol\.', name_text): 
            #print re.search(r'Vol\.', name_text).groups()
            continue #Don't want compilations
        #print "NAME::" + name[0].text_content()
        downloads = int(row.cssselect('.tlistdn')[0].text_content())
        name_data = re.findall('\[([^\]]*)\]',name_text)
        group = name_data[0]
        #print name_data
        quality_match = re.findall(r'\((.*)\)\.m..$',name_text)
        quality = quality_match[0] if len(quality_match) > 0 else None
        title_match = re.findall(r'\] (.*) - ', name_text)
        show_title = title_match[0] if len(title_match) > 0 else None
        episode_match = re.findall(r' - v?([0-9][0-9]) \(', name_text)
        episode_num = int(episode_match[0]) if len(episode_match) > 0 else None
        if len(title_match) == 0:
            pass
            #print "FAILED::" + name_text
        if show_title and episode_num:
            episode = {
                'group': group,
                'title': show_title,
                'episode': episode_num,
                'quality': str(quality),
                'downloads': downloads
            }
            scraperwiki.sqlite.save(unique_keys=['group','title','episode','quality'],data=episode)
    
            #print str(downloads) + "||" + str(show_title) + "||" + str(episode_num) + "||" + group + "||" + str(quality)import scraperwiki
import lxml.html
import re

for offset in range(1,21):
    html = scraperwiki.scrape('http://nyaa.eu/?page=search&cats=0_0&filter=0&term=zero+raws&offset=' + str(offset))
    #print html
    root = lxml.html.fromstring(html)
    for row in root.cssselect('.tlistrow'):
        name = row.cssselect('.tlistname')
        name_text = unicode(name[0].text_content())
        if not name_text[0] == '[': continue
        if re.search(r'Vol\.', name_text): 
            #print re.search(r'Vol\.', name_text).groups()
            continue #Don't want compilations
        #print "NAME::" + name[0].text_content()
        downloads = int(row.cssselect('.tlistdn')[0].text_content())
        name_data = re.findall('\[([^\]]*)\]',name_text)
        group = name_data[0]
        #print name_data
        quality_match = re.findall(r'\((.*)\)\.m..$',name_text)
        quality = quality_match[0] if len(quality_match) > 0 else None
        title_match = re.findall(r'\] (.*) - ', name_text)
        show_title = title_match[0] if len(title_match) > 0 else None
        episode_match = re.findall(r' - v?([0-9][0-9]) \(', name_text)
        episode_num = int(episode_match[0]) if len(episode_match) > 0 else None
        if len(title_match) == 0:
            pass
            #print "FAILED::" + name_text
        if show_title and episode_num:
            episode = {
                'group': group,
                'title': show_title,
                'episode': episode_num,
                'quality': str(quality),
                'downloads': downloads
            }
            scraperwiki.sqlite.save(unique_keys=['group','title','episode','quality'],data=episode)
    
            #print str(downloads) + "||" + str(show_title) + "||" + str(episode_num) + "||" + group + "||" + str(quality)