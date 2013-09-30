import scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import datetime
import json

url = "http://wiki.lesswrong.com/wiki/Less_Wrong/All_articles"
#http://wiki.lesswrong.com/wiki/Less_Wrong/Article_summaries

#count links in text? +wikilinks, +lwlinks (seq?), +outlinks, 
#prevlinks (followup to), relto (related to), refto (refers to links)

# broken links results pad in http://piratepad.net/bATb1G8s4A

posts = lxml.html.parse(url).getroot().find_class("wikitable")[0].findall('tr')[2:]
nonseq = []

i=0

for j,post in enumerate(posts):
    article = {}
    article['author'] = post.findall('td')[2].find('a').text if post.findall('td')[2].find('a') is not None else ""
    article['title'] = post.findall('td')[0].find('a').text if post.findall('td')[2].find('a') is not None else ""
    if (article['author'] == 'Eliezer_Yudkowsky') and (article['title'][:18] != "Rationality Quotes"):
        i += 1
        article['id'] = j
        article['number'] = i
        article['url'] = post.findall('td')[0].find('a').attrib['href']
        #print str(i) + ' url:' + article['url']

        apiurl = "http://sharedcount.com/api/?url=%s" % (article['url'])
        metadata = json.loads(urllib2.urlopen(apiurl).read())
        #print apiurl
    
        article['twitter'] = metadata.get('Twitter', 0)
        article['buzz'] = metadata.get('Buzz', 0)
        article['digg'] = metadata.get('Digg', 0)
        article['delicious'] = metadata.get('Delicious', 0)
        article['stumbleupon'] = metadata.get('StumbleUpon', 0)
        if metadata['Facebook'] is not None:
            article['fb click cnt'] = metadata['Facebook'].get('click_count', 0)
            article['fb shar cnt'] = metadata['Facebook'].get('share_count', 0)
            article['fb like cnt'] = metadata['Facebook'].get('like_count', 0)
            article['fb comm cnt'] = metadata['Facebook'].get('comment_count', 0)
            article['fb totl cnt'] = metadata['Facebook'].get('total_count', 0)
            article['fb comm fid'] = metadata['Facebook'].get('comments_fbid', 0)
            article['fb cbox cnt'] = metadata['Facebook'].get('commentsbox_count', 0)
        
        article_tree = lxml.html.parse(article['url']).getroot() #uncaught potential IOError

        tries = 0

        vote_tree = article_tree.find_class('votes')

        while ((article_tree is None) or (not vote_tree)) and (tries<5):
            tries += 1
            print 'trying again, tries: %s' % tries
            article_tree = lxml.html.parse(article['url']).getroot()

        if tries<6:
            # sum of votes
            try:
                article['votes'] = int(article_tree.find_class('votes')[1].text)
            except IndexError:
                print "Error: ", lxml.html.tostring(article_tree)
                break
            
            # wordcount
            try:
                article['wordcount'] = len(unicode.split( article_tree.find_class("content")[0].text_content() ))
            except TypeError: 
                article['wordcount'] = len(str.split( article_tree.find_class("content")[0].text_content() ))

            # charcount
            #try:
                
            
            # comments
            try: 
                article['comments'] = int(article_tree.get_element_by_id('comments').find('h2').text[10:-1])
            except KeyError: 
                article['comments'] = 0
            
            # posted datetime
            dtime = datetime.datetime(*time.strptime(article_tree.find_class('date')[0].text,'%d %B %Y %I:%M%p')[:6])
    
            article['wlinks'] = 0
            article['elinks'] = 0
            article['slinks'] = 0

            # links -- wiki (wlinks), sequences (slinks), external (elinks)
            links = article_tree.find_class("content")[0].findall('.//a')
            for link in links: 
                try:
                    ltarg = link.attrib['href']

                    if ltarg[:31] == 'http://wiki.lesswrong.com/wiki/':
                        article['wlinks'] += 1
                    elif (ltarg[:23] == 'http://lesswrong.com/lw/') or (ltarg[:4] == '/lw/'):
                        article['slinks'] += 1  #ideally this would be crosschecked with the list of sequence posts
                    elif ltarg[:30] == 'http://www.overcomingbias.com/':
                        oburl = urlparse.urlparse(ltarg)
                        if oburl[5] != '':
                            frag = oburl[5]
                            try:
                                realtarg = urllib2.urlopen(oburl[0] + '://' + oburl[1] + oburl[2]).geturl()

                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                if ltarg != (realtarg + "#" + frag):
                                    print " which resolves to " + realtarg + "#" + frag

                                if frag == 'more':
                                    print 'The browser is directed to display the article below the summary fold'
                                print ' \n'
                            except urllib2.HTTPError, e:
                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                print 'Error code: ', e.code
                                print ' \n'
                        else:
                            try:
                                realtarg = urllib2.urlopen(oburl[0] + '://' + oburl[1] + oburl[2]).geturl()
                                if ltarg != realtarg:
                                    article['slinks'] += 1
                                else:
                                    article['elinks'] += 1
                            except urllib2.HTTPError, e:
                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                print 'Error code: ', e.code
                                print ' \n'
                    else:
                        article['elinks'] += 1
                except KeyError: pass
    
            # relevant to, followup to, etc.
            #st = article_tree.find_class("content")[0].find('div/div')
            #st = st.findall('p')
            #if st and (st[0].find('strong') is not None):
            #        print lxml.html.tostring(st[0])

            # get first par, cound text chars and link chars. over a certain density, print out.

        scraperwiki.sqlite.save(unique_keys=['id'], data=article, date=dtime)

        if article['title'] == "Practical Advice Backed By Deep Theories":
            break
import scraperwiki
import urllib2, urlparse
import lxml.etree, lxml.html
import re
import time
import datetime
import json

url = "http://wiki.lesswrong.com/wiki/Less_Wrong/All_articles"
#http://wiki.lesswrong.com/wiki/Less_Wrong/Article_summaries

#count links in text? +wikilinks, +lwlinks (seq?), +outlinks, 
#prevlinks (followup to), relto (related to), refto (refers to links)

# broken links results pad in http://piratepad.net/bATb1G8s4A

posts = lxml.html.parse(url).getroot().find_class("wikitable")[0].findall('tr')[2:]
nonseq = []

i=0

for j,post in enumerate(posts):
    article = {}
    article['author'] = post.findall('td')[2].find('a').text if post.findall('td')[2].find('a') is not None else ""
    article['title'] = post.findall('td')[0].find('a').text if post.findall('td')[2].find('a') is not None else ""
    if (article['author'] == 'Eliezer_Yudkowsky') and (article['title'][:18] != "Rationality Quotes"):
        i += 1
        article['id'] = j
        article['number'] = i
        article['url'] = post.findall('td')[0].find('a').attrib['href']
        #print str(i) + ' url:' + article['url']

        apiurl = "http://sharedcount.com/api/?url=%s" % (article['url'])
        metadata = json.loads(urllib2.urlopen(apiurl).read())
        #print apiurl
    
        article['twitter'] = metadata.get('Twitter', 0)
        article['buzz'] = metadata.get('Buzz', 0)
        article['digg'] = metadata.get('Digg', 0)
        article['delicious'] = metadata.get('Delicious', 0)
        article['stumbleupon'] = metadata.get('StumbleUpon', 0)
        if metadata['Facebook'] is not None:
            article['fb click cnt'] = metadata['Facebook'].get('click_count', 0)
            article['fb shar cnt'] = metadata['Facebook'].get('share_count', 0)
            article['fb like cnt'] = metadata['Facebook'].get('like_count', 0)
            article['fb comm cnt'] = metadata['Facebook'].get('comment_count', 0)
            article['fb totl cnt'] = metadata['Facebook'].get('total_count', 0)
            article['fb comm fid'] = metadata['Facebook'].get('comments_fbid', 0)
            article['fb cbox cnt'] = metadata['Facebook'].get('commentsbox_count', 0)
        
        article_tree = lxml.html.parse(article['url']).getroot() #uncaught potential IOError

        tries = 0

        vote_tree = article_tree.find_class('votes')

        while ((article_tree is None) or (not vote_tree)) and (tries<5):
            tries += 1
            print 'trying again, tries: %s' % tries
            article_tree = lxml.html.parse(article['url']).getroot()

        if tries<6:
            # sum of votes
            try:
                article['votes'] = int(article_tree.find_class('votes')[1].text)
            except IndexError:
                print "Error: ", lxml.html.tostring(article_tree)
                break
            
            # wordcount
            try:
                article['wordcount'] = len(unicode.split( article_tree.find_class("content")[0].text_content() ))
            except TypeError: 
                article['wordcount'] = len(str.split( article_tree.find_class("content")[0].text_content() ))

            # charcount
            #try:
                
            
            # comments
            try: 
                article['comments'] = int(article_tree.get_element_by_id('comments').find('h2').text[10:-1])
            except KeyError: 
                article['comments'] = 0
            
            # posted datetime
            dtime = datetime.datetime(*time.strptime(article_tree.find_class('date')[0].text,'%d %B %Y %I:%M%p')[:6])
    
            article['wlinks'] = 0
            article['elinks'] = 0
            article['slinks'] = 0

            # links -- wiki (wlinks), sequences (slinks), external (elinks)
            links = article_tree.find_class("content")[0].findall('.//a')
            for link in links: 
                try:
                    ltarg = link.attrib['href']

                    if ltarg[:31] == 'http://wiki.lesswrong.com/wiki/':
                        article['wlinks'] += 1
                    elif (ltarg[:23] == 'http://lesswrong.com/lw/') or (ltarg[:4] == '/lw/'):
                        article['slinks'] += 1  #ideally this would be crosschecked with the list of sequence posts
                    elif ltarg[:30] == 'http://www.overcomingbias.com/':
                        oburl = urlparse.urlparse(ltarg)
                        if oburl[5] != '':
                            frag = oburl[5]
                            try:
                                realtarg = urllib2.urlopen(oburl[0] + '://' + oburl[1] + oburl[2]).geturl()

                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                if ltarg != (realtarg + "#" + frag):
                                    print " which resolves to " + realtarg + "#" + frag

                                if frag == 'more':
                                    print 'The browser is directed to display the article below the summary fold'
                                print ' \n'
                            except urllib2.HTTPError, e:
                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                print 'Error code: ', e.code
                                print ' \n'
                        else:
                            try:
                                realtarg = urllib2.urlopen(oburl[0] + '://' + oburl[1] + oburl[2]).geturl()
                                if ltarg != realtarg:
                                    article['slinks'] += 1
                                else:
                                    article['elinks'] += 1
                            except urllib2.HTTPError, e:
                                print "Article '" + article['title'] + "'"
                                print " at " + article['url']
                                print " links to " + ltarg
                                print 'Error code: ', e.code
                                print ' \n'
                    else:
                        article['elinks'] += 1
                except KeyError: pass
    
            # relevant to, followup to, etc.
            #st = article_tree.find_class("content")[0].find('div/div')
            #st = st.findall('p')
            #if st and (st[0].find('strong') is not None):
            #        print lxml.html.tostring(st[0])

            # get first par, cound text chars and link chars. over a certain density, print out.

        scraperwiki.sqlite.save(unique_keys=['id'], data=article, date=dtime)

        if article['title'] == "Practical Advice Backed By Deep Theories":
            break
