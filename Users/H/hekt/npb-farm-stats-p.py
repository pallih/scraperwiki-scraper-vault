import scraperwiki
import lxml.html
import datetime

YEAR = '2013'

SCRAPE_STATS = ['throws', 'name', 'g', 'w', 'l', 'sv', 'cg', 'sho', 'zbc', 'wpct', 'bf', 'ip1', 'ip2', 'h', 'hr', 'bb', 'ibb', 'hbp', 'so', 'wp', 'bk', 'r', 'er']
SCRAPE_STATS_LENGTH = len(SCRAPE_STATS)
EASTS = ['f', 'g', 'e', 's', 'l', 'db', 'm']
WESTS = ['d', 'h', 't', 'bs', 'c']

BASE_URL = "http://bis.npb.or.jp/%s/stats/idp2_%s.html"

def main():
    def do(league):
        grand_total = {}
        stats = []
        for team in league:
            result, total = scrape(team)
            stats += (result)
            grand_total = calcTotal(grand_total, total)
        for s in stats:
            s.update(calcStats(s, grand_total))
            scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                                    data=s)
        grand_total.update(calcStats(grand_total, grand_total))
        return grand_total

    east_total = do(EASTS)
    west_total = do(WESTS)
    east_total.update({'team': 'league', 'name': 'east', 'year': YEAR})
    west_total.update({'team': 'league', 'name': 'west', 'year': YEAR})
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=east_total)
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=west_total)


def calcStats(data, league_data):
    g = float(data['g'])                # games
    w = float(data['w'])                # wins
    l = float(data['l'])                # losses
    sv = float(data['sv'])              # saves
    bf = float(data['bf'])              # batsmen faced
    h = float(data['h'])                # hits
    hr = float(data['hr'])              # homeruns
    bb = float(data['bb'])              # bases on balls
    ibb = float(data['ibb'])            # intentional bbs
    hbp = float(data['hbp'])            # hit by pitch
    so = float(data['so'])              # strikeouts
    wp = float(data['wp'])              # wild pitches
    bk = float(data['bk'])              # balks
    r = float(data['r'])                # runs
    er = float(data['er'])              # earned runs

    l_hr = float(league_data['hr'])     # league hr
    l_bb = float(league_data['bb'])     # league bb
    l_ibb = float(league_data['ibb'])   # league ibb
    l_hbp = float(league_data['hbp'])   # league hbp
    l_so = float(league_data['so'])     # league so
    l_er = float(league_data['er'])     # league er

    l_outs = float(league_data['ip1']) * 3 + float(league_data['ip2'])
    l_era = l_er * 3 * 3 / l_outs \
            if l_outs else None

    wpct = w / (w + l) if (w or l) else None
    ip = float(data['ip1']) + float(data['ip2']) / 10
    outs = float(data['ip1']) * 3 + float(data['ip2'])

    era = er * 9 * 3 / outs \
          if outs else None
    whip = (h + bb) * 3 / outs \
           if outs else None

    fip_a = l_era - (13 * l_hr + 3 * (l_bb + l_hbp - l_ibb) - 2 * l_so) * 3 / \
            l_outs \
            if l_outs else None
    fip = (13 * hr + 3 * (bb + hbp - ibb)) * 3 / outs + fip_a \
          if outs else None

    lobp_a = h + bb + hbp - 1.4 * hr
    lobp = ((h + bb + hbp - r) / lobp_a) * 100 if lobp_a else None
    kbb = so / bb if bb else None
    k9 = so * 9 * 3 / outs if outs else None
    bb9 = bb * 9 * 3 / outs if outs else None
    hr9 = hr * 9 * 3 / outs if outs else None
    ipg = outs / 3 / g if g else None
    babip_a = bf - bb - hbp - hr - so
    babip = (h - hr) / babip_a if babip_a else None

    def eraJust(n):
        if n is None:
            return None
        nn = round(n, 2)
        idx = str(nn).index('.')
        return str(nn)[:idx] + str(nn)[idx:].ljust(3, '0')
    def babipJust(n):
        if n is None:
            return None
        return str(n)[1:5].ljust(4, '0') if n < 1 else \
               str(n)[0:5].ljust(5, '0')

    ip = str(ip)
    era = eraJust(era)
    whip = eraJust(whip)
    fip = eraJust(fip)
    lobp = str(round(lobp, 1)) if lobp else lobp
    kbb = eraJust(kbb)
    k9 = eraJust(k9)
    bb9 = eraJust(bb9)
    hr9 = eraJust(hr9)
    ipg = eraJust(ipg)
    babip = babipJust(babip)
    wpct = babipJust(wpct)
    
    return {'wpct': wpct, 'ip': ip, 'era': era, 'whip': whip, 'fip': fip, 'lobp': lobp, 'kbb': kbb, 'k9': k9, 'bb9': bb9, 'hr9': hr9, 'ipg': ipg, 'babip': babip}


def scrape(team):
    url = BASE_URL % (YEAR, team)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    trs = root.cssselect("div#stdivmaintbl tr.ststats")

    total = {}
    result = []

    for tr in trs:
        if tr.cssselect("td.stplayer"):
            tds = tr.cssselect("td")
            contents = map(lambda x: x.text_content(), tds)
            for i in range(2, SCRAPE_STATS_LENGTH):
                if contents[i].find('.') != -1:
                    contents[i] = float(contents[i])
                elif contents[i] == '----' or contents[i] == '+':
                    contents[i] = 0
                elif contents[i]:
                    contents[i] = int(contents[i])
                else:
                    contents[i] = 0

            data = zipdict(SCRAPE_STATS, contents)
            data['ip2'] = data['ip2'] * 10 if data['ip2'] else data['ip2']
            data['throws'] = 'S' if data['throws'] == '+' else \
                             'L' if data['throws'] == '*' else \
                             'R'
            data.update({'team': team, 'year': YEAR})
            
            total = calcTotal(total, data)
            result.append(data)

    return result, total

def calcTotal(total, current):
    if total:
        for k in SCRAPE_STATS[2:]:
            total[k] = total[k] + current[k]
    else:
        for k in SCRAPE_STATS[2:]:
            total[k] = current[k]
    return total


def zipdict(ks, vs):
    return dict(zip(ks, vs))

main()
