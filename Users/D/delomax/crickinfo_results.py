import scraperwiki
from BeautifulSoup import BeautifulSoup
import re

URL = 'http://www.espncricinfo.com/ci/engine/current/match/scores/recent.html'

def main():
    print("Scraping %s" % URL)
    html = scraperwiki.scrape(URL)
    soup = BeautifulSoup(html)

    for match in find_match(soup):
        match_type = match.findPreviousSibling("p", attrs = {"class":'potMatchSeriesHeading'})
        a_tag = match.findChild('a', attrs = {'href':re.compile(r'^/.+/engine/match/\d+\.html$'),'class':'potMatchLink'})
        score = match.findNextSibling("p", attrs = {"class":'potMatchText mat_scores'})
        result = score.findNextSibling("p", attrs = {"class":'potMatchText mat_status'})
        (home_team, away_team, venue) = extract_teams_venue(a_tag.text);        
        scraperwiki.sqlite.save(unique_keys=[], data = {
            'match type':match_type.text, 
            'match':a_tag.text, 
            'score':score.text,
            'result':result.text,
            'away team':away_team,
            'home team':home_team,
            'venue':venue})

    
def find_match(soup):
    return soup.findAll('p', attrs = {'class':'potMatchHeading'})

def extract_teams_venue(match_str):
    my_re = re.compile(r'^(.+) v (.+) at (.+)$')
    match = my_re.match(match_str)
    if match:
        return match.groups()
    
main()