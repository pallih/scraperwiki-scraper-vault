import scraperwiki
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re, csv

def get_basketball_soup(team, year):
    """
    This function grabs the "soup" for the given team and year
    and returns the BeautifulSoup object
    """
    url = "http://www.basketball-reference.com/teams/%s/%s_games.html"% (team,year)
    print url
    try:
        request = urllib2.Request(url)
    except urllib2.HTTPError:
        return None

    try:
        response = urllib2.urlopen(request)
    except:
        return None
    
    the_page = response.read()
    try:
        soup = BeautifulSoup(the_page)
    except:
        the_page = re.sub('<\/scr', '',the_page)
        soup = BeautifulSoup(the_page)
    return soup

def process_soup(soup):
    """
    This goes through the BeautifulSoup object for a given
    team/year and returns a list of lists that can then
    be written to the .csv output.

    """
    if soup == None:
        return

    games = soup.findAll('tr')

    stats = []
    for gamerow in games:
        cells = [i for i in gamerow.findChildren('td')]
        if len(cells) == 0:
            continue
        if cells[0].string == "G":
            continue
                
        gamenum = cells[0].string
        
        try:
            gamedate = cells[1].firstText().string
        except:
            gamedate = cells[1].string

        home = cells[2].string != "@"
        opp = cells[3].get('csk')[:3]
        winloss = cells[4].string
        pf = cells[6].string
        pa = cells[7].string
        wins = cells[8].string
        losses = cells[9].string
        streak = cells[10].string
        notes = cells[11].string
        if notes == None:
            notes = ""

        stats.append([gamenum, gamedate, home, opp, winloss,
                      pf, pa, wins, losses, streak, notes])
            
    return stats


if __name__ == '__main__':


    startyear = 1970
    endyear = 2011
    outfile = 'basketball_games.csv'



    teams = ['BAL','ATL','BUF','CAP','CHA','CHH','CHI','CIN','CLE','DAL',
             'DEN','DET','GSW','HOU','IND','KCK','KCO','LAC','LAL','MEM',
             'MIA','MIL','MIN','NJN','NOH','NOJ','NOK','NYK','NYN','OKC',
             'ORL','PHI','PHO','POR','SAC','SAS','SDC','SDR','SEA','SFW',
             'TOR','UTA','VAN','WAS','WSB']

    fout = csv.writer(open(outfile,'w'))
    
    # write header
    fout.writerow(["gamenum","date", "homegame", "opp", "winloss", "pf", "pa", "wins", "losses", "streak", "notes", "team","year"])
    
    
    for team in teams:
        for year in xrange(startyear, endyear):
            print team, year
            
            soup = get_basketball_soup(team, year)
            if soup == None:
                # no team for that year
                continue
                
            stats = process_soup(soup)

            # add the team and year info
            if stats != 0:            
                for game in stats:
                    game.extend([team, year])
                    fout.writerow(game)
    del(fout)import scraperwiki
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
import re, csv

def get_basketball_soup(team, year):
    """
    This function grabs the "soup" for the given team and year
    and returns the BeautifulSoup object
    """
    url = "http://www.basketball-reference.com/teams/%s/%s_games.html"% (team,year)
    print url
    try:
        request = urllib2.Request(url)
    except urllib2.HTTPError:
        return None

    try:
        response = urllib2.urlopen(request)
    except:
        return None
    
    the_page = response.read()
    try:
        soup = BeautifulSoup(the_page)
    except:
        the_page = re.sub('<\/scr', '',the_page)
        soup = BeautifulSoup(the_page)
    return soup

def process_soup(soup):
    """
    This goes through the BeautifulSoup object for a given
    team/year and returns a list of lists that can then
    be written to the .csv output.

    """
    if soup == None:
        return

    games = soup.findAll('tr')

    stats = []
    for gamerow in games:
        cells = [i for i in gamerow.findChildren('td')]
        if len(cells) == 0:
            continue
        if cells[0].string == "G":
            continue
                
        gamenum = cells[0].string
        
        try:
            gamedate = cells[1].firstText().string
        except:
            gamedate = cells[1].string

        home = cells[2].string != "@"
        opp = cells[3].get('csk')[:3]
        winloss = cells[4].string
        pf = cells[6].string
        pa = cells[7].string
        wins = cells[8].string
        losses = cells[9].string
        streak = cells[10].string
        notes = cells[11].string
        if notes == None:
            notes = ""

        stats.append([gamenum, gamedate, home, opp, winloss,
                      pf, pa, wins, losses, streak, notes])
            
    return stats


if __name__ == '__main__':


    startyear = 1970
    endyear = 2011
    outfile = 'basketball_games.csv'



    teams = ['BAL','ATL','BUF','CAP','CHA','CHH','CHI','CIN','CLE','DAL',
             'DEN','DET','GSW','HOU','IND','KCK','KCO','LAC','LAL','MEM',
             'MIA','MIL','MIN','NJN','NOH','NOJ','NOK','NYK','NYN','OKC',
             'ORL','PHI','PHO','POR','SAC','SAS','SDC','SDR','SEA','SFW',
             'TOR','UTA','VAN','WAS','WSB']

    fout = csv.writer(open(outfile,'w'))
    
    # write header
    fout.writerow(["gamenum","date", "homegame", "opp", "winloss", "pf", "pa", "wins", "losses", "streak", "notes", "team","year"])
    
    
    for team in teams:
        for year in xrange(startyear, endyear):
            print team, year
            
            soup = get_basketball_soup(team, year)
            if soup == None:
                # no team for that year
                continue
                
            stats = process_soup(soup)

            # add the team and year info
            if stats != 0:            
                for game in stats:
                    game.extend([team, year])
                    fout.writerow(game)
    del(fout)