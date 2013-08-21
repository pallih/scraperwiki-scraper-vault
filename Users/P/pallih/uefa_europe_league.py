import scraperwiki
import lxml.html
import re

#referee_regex = re.compile(".+ee:(.*\)).*Stadium: (.*\))")
referee_regex = re.compile(".+ee:(.*) – .*Stadium: (.*\))")
match_detail_regex = re.compile("md_(\-?\d+)_(\-?\d+)")

baseurl = 'http://www.uefa.com/uefaeuropaleague/season=%s/matches/all/index.html' #to get the number of matches each year
real_baseurl = 'http://www.uefa.com/uefaeuropaleague/season=%s/matches/library/fixtures/day=%s/session=%s/_matchesbydate.html' # this is the content - it's populated by javascript in a browser - we do not have that luxury so we need to call it directly

years = range(1971,2012) #2000 does not include a link to full time info

match_date_xpath = '//table[starts-with(@class,"tdate")]'
match_detail_xpath = '//tbody[starts-with(@class,"tb")]'

def process(url,season,internal_matchday):
    html = scraperwiki.scrape(url)
    html = html.decode('utf-8') #convert to unicode before lxml gets it since the encoding declaration is missing in the html
    root = lxml.html.fromstring(html)
    matches = root.xpath (match_detail_xpath)
    for match in matches:
        record = {}
        record['matchday'] = root.xpath('//h3')[0].text
        record['season'] = season
        record['internal_matchday'] = internal_matchday
        #trs = match.xpath('//tr[@class="sup"]') #info and url
        record['stage'] = match.xpath('tr[@class="sup"]//span[@class="rname"]')[0].text_content()
        try: # one or two cancels
            record['match_detail_url'] = 'http://www.uefa.com' + match.xpath('tr[@class="sup"]//span[contains(@class,"report")]/a')[0].attrib['href']
        except:
            pass
        record['home_team'] = match.xpath('tr[@class=" match_res"]//td[contains(@class,"home")]')[0].text_content()
        record['away_team'] = match.xpath('tr[@class=" match_res"]//td[contains(@class,"away")]')[0].text_content()
        try:
            record['aggregate'] = match.xpath('tr[@class="reasonwin"]//span[contains(@class,"rwa")]')[0].text_content()
        except:
            pass
        try: 
            record['aggregate_notes'] = match.xpath('tr[@class="reasonwin"]//span[contains(@class,"woag")]')[0].text_content()
        except:
            pass

        record['home_team_url'] = 'http://www.uefa.com' + match.xpath('tr[@class=" match_res"]//td[contains(@class,"home")]/a')[0].attrib['href']
        record['away_team_url'] = 'http://www.uefa.com' + match.xpath('tr[@class=" match_res"]//td[contains(@class,"away")]/a')[0].attrib['href']
        record['score'] = match.xpath('tr[@class=" match_res"]//td[contains(@class,"score")]')[0].text_content()
        ref_stadium = re.split(u"\u2013", match.xpath('tr[@class="referee_stadium"]')[0].text_content())
        #print repr(match.xpath('tr[@class="referee_stadium"]')[0][0].text)
        try:
            #record['referee'] = ref_stadium[0].lstrip('Referee: ').strip()
            record['referee'] = ref_stadium[0].replace('Referee: ','').strip()
        except:
            pass
        try:
            #record['stadium'] = ref_stadium[1].lstrip('Stadium: ').strip()
            record['stadium'] = ref_stadium[1].replace('Stadium: ','').strip()
        except:
            pass
        
        #print record
        scraperwiki.sqlite.save(unique_keys=['matchday', 'season', 'score', 'home_team', 'away_team'], data=record, verbose=1)


def scrape(url, season):
    html = scraperwiki.scrape(url)
    html = html.decode('utf-8')
    #print html
    root = lxml.html.fromstring(html)
    matchdays = root.xpath (match_date_xpath)
    number_matchdays = len(matchdays)
    for m in matchdays:
        r = match_detail_regex.search(str(m.attrib['id']))
        url = real_baseurl % (season, r.groups()[0], r.groups()[1])
        process(url, season,r.groups()[1])  
    


for year in years:
    url = baseurl % (year)
    print year
    scrape(url, year)


