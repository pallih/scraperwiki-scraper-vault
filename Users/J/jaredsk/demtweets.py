import scraperwiki
import lxml.html


handles = ['SenatorCarper',
                'CarperforDE',
                'keithspanarelli',
                'chriscoons',
                'coons4delaware',
                'JohnCarneyDE',
                'John_Carney',
                'GovernorMarkell',
                'WeBackJack',
                'Matt_Denn',
                'MitchCraneforDE',
                'PaulGallagher20',
                'Counihan4Senate',
                'AndrewStaton',
                'BryanTownsendDE',
                'NicolePoore12',
                'DWilliams4Mayor',
                'CharlesPotterJr',
                'DebraHeffernan',
                'BeckyWalkerDE',
                'DelawareFirstNT',
                'RepLonghurst',
                'PBaumbachDE',
                'cbbock',
                'DarrylScott',
                'KevinWade2012',
                'tomkovach',
                'RoseIzzo2012',
                'JeffCragg2012',
                'SherValenzuela1',
                'jvh2012',
                'GregLavelle302',
                'GlenUrquhart',
                'DEConservative',
                'Lawson4Senate',
                'ColinBonini',
                'MatthewOpaliski',
                'EricBodie',
                'NManolakos']
handles2 = ['jkobos']
tweets = []
for item in handles:   
    html = lxml.html.fromstring(scraperwiki.scrape("http://www.twitter.com/" + item))
    time = html.cssselect("small.time a")
    senttweets = html.cssselect("p[class='js-tweet-text']")
    for bar in range(len(senttweets)):
        c = senttweets[bar].text_content()
        t = time[bar].attrib["title"]
        tweets.append(c)
        scraperwiki.sqlite.save(unique_keys=["text"],data={"sender":item,"text":c,"time":t})




import scraperwiki
import lxml.html


handles = ['SenatorCarper',
                'CarperforDE',
                'keithspanarelli',
                'chriscoons',
                'coons4delaware',
                'JohnCarneyDE',
                'John_Carney',
                'GovernorMarkell',
                'WeBackJack',
                'Matt_Denn',
                'MitchCraneforDE',
                'PaulGallagher20',
                'Counihan4Senate',
                'AndrewStaton',
                'BryanTownsendDE',
                'NicolePoore12',
                'DWilliams4Mayor',
                'CharlesPotterJr',
                'DebraHeffernan',
                'BeckyWalkerDE',
                'DelawareFirstNT',
                'RepLonghurst',
                'PBaumbachDE',
                'cbbock',
                'DarrylScott',
                'KevinWade2012',
                'tomkovach',
                'RoseIzzo2012',
                'JeffCragg2012',
                'SherValenzuela1',
                'jvh2012',
                'GregLavelle302',
                'GlenUrquhart',
                'DEConservative',
                'Lawson4Senate',
                'ColinBonini',
                'MatthewOpaliski',
                'EricBodie',
                'NManolakos']
handles2 = ['jkobos']
tweets = []
for item in handles:   
    html = lxml.html.fromstring(scraperwiki.scrape("http://www.twitter.com/" + item))
    time = html.cssselect("small.time a")
    senttweets = html.cssselect("p[class='js-tweet-text']")
    for bar in range(len(senttweets)):
        c = senttweets[bar].text_content()
        t = time[bar].attrib["title"]
        tweets.append(c)
        scraperwiki.sqlite.save(unique_keys=["text"],data={"sender":item,"text":c,"time":t})




