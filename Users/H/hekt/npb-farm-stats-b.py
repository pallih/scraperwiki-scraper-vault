import scraperwiki
import lxml.html
import datetime

YEAR = '2013'

STATS = ['bats', 'name', 'g', 'pa', 'ab', 'r', 'h', 'dbl', 'tpl', 'hr', 'tb',
         'rbi', 'sb', 'cs', 'sh', 'sf', 'bb', 'ibb', 'hbp', 'so', 'gd']
STATS_LENGTH = len(STATS)
EASTS = ['f', 'g', 'e', 's', 'l', 'db', 'm']
WESTS = ['d', 'h', 't', 'bs', 'c']

BASE_URL = "http://bis.npb.or.jp/%s/stats/idb2_%s.html"

def main():
    def f(league):
        grand_total = {}
        for team in league:
            result, total = scrape(team)
            for d in result:
                d.update(calcStats(d))
                scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                                        data=d)
            grand_total = calcTotal(grand_total, total)
        grand_total.update(calcStats(grand_total))
        return grand_total

    east_total = f(EASTS)
    west_total = f(WESTS)
    east_total.update({'team': 'league', 'bats': None, 'name': 'east',
                       'year': YEAR})
    west_total.update({'team': 'league', 'bats': None, 'name': 'west',
                       'year': YEAR})
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=east_total)
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=west_total)


def calcStats(data):
    h = float(data['h'])                # hits
    ab = float(data['ab'])              # at bats
    dbl = float(data['dbl'])            # doules
    tpl = float(data['tpl'])            # triples
    hr = float(data['hr'])              # homeruns
    tb = float(data['tb'])              # total bases
    bb = float(data['bb'])              # bases on balls
    ibb = float(data['ibb'])            # intentional bbs
    hbp = float(data['hbp'])            # hit by pitches
    sh = float(data['sh'])              # sacrifice hits
    sf = float(data['sf'])              # sacrifice flies
    sb = float(data['sb'])              # stolen bases
    cs = float(data['cs'])              # caught stealing
    so = float(data['so'])              # strike outs
    gd = float(data['gd'])              # ground doubles
    sgl = h - dbl - tpl - hr            # singles
    
    avg = h / ab \
          if ab else None
    slg = tb / ab \
          if ab else None
    obp_a = h + bb + hbp
    obp_b = ab + bb + hbp + sf
    obp = obp_a / obp_b \
          if obp_b else None
    ops = slg + obp \
          if (slg is not None and obp is not None) else None
    noi = (obp + slg / 3) * 1000 \
          if (slg is not None and obp is not None) else None
    gpa = (obp * 1.8 + slg) / 4 \
          if (slg is not None and obp is not None) else None

    rc_a = h + bb + hbp - cs - gd
    rc_b = tb + 0.26 * (bb + hbp) + 0.53 * (sh + sf) + 0.64 * sb - 0.03 * so
    rc_c = ab + bb + hbp + sf + sh
    rc = (2.4 * rc_c + rc_a) * (3 * rc_c + rc_b) / (9 * rc_c) - 0.9 * rc_c\
         if rc_c else None
    rc27_a = ab - h + cs + sh + sf + gd
    rc27 = rc / rc27_a * 27 \
           if rc27_a else None

    xr = 0.50 * sgl + 0.72 * dbl + 1.04 * tpl + 1.44 * hr + \
         0.34 * (bb + hbp) + 0.25 * ibb + 0.18 * sb - 0.32 * cs - \
         0.09 * (ab - h - so) - 0.37 * gd + 0.37 * sf + 0.04 * sh
    xr27_a = rc27_a
    xr27 = xr / xr27_a * 27 \
           if xr27_a else None

    babip_a = h - hr
    babip_b = ab + sf - hr - so
    babip = babip_a / babip_b \
            if babip_b else None

    isop = slg - avg \
           if (avg is not None and slg is not None) else None
    isod = obp - avg \
           if (avg is not None and obp is not None) else None

    sbp = sb / (sb + cs) * 100 \
          if (sb or cs) else None

    def avgJust(n):
        if n is None:
            return None
        return str(n)[1:5].ljust(4, '0') if n < 1 else \
               str(n)[0:5].ljust(5, '0')
               
    def rcJust(n):
        if n is None:
            return None
        nn = round(n, 1)
        idx = str(nn).index('.')
        return str(nn)[:idx] + str(nn)[idx:].ljust(2, '0')

    avg = avgJust(avg)
    slg = avgJust(slg)
    obp = avgJust(obp)
    ops = avgJust(ops)
    gpa = avgJust(gpa)
    noi = str(round(noi, 1)) if noi else None
    rc = rcJust(rc)
    rc27 = rcJust(rc27)
    xr = rcJust(xr)
    xr27 = rcJust(xr27)
    babip = avgJust(babip)
    isop = avgJust(isop)
    isod = avgJust(isod)
    sbp = str(round(sbp, 1)) if sbp else None

    return {'avg': avg, 'slg': slg, 'obp': obp, 'ops': ops, 'noi': noi,
            'gpa': gpa, 'rc': rc, 'rc27': rc27, 'xr': xr, 'xr27': xr27,
            'babip': babip, 'isop': isop, 'isod': isod, 'sbp': sbp}


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
            for i in range(2, STATS_LENGTH):
                contents[i] = int(contents[i])
            
            data = zipdict(STATS, contents)
            data.update({'team': team, 'year': YEAR})
            data['bats'] = 'S' if data['bats'] == '+' else \
                           'L' if data['bats'] == '*' else \
                           'R'
            
            total = calcTotal(total, data)
            result.append(data)

    return result, total

def calcTotal(total, current):
    if total:
        for k in STATS[2:]:
            total[k] = total[k] + current[k]
    else:
        for k in STATS[2:]:
            total[k] = current[k]
    return total


def zipdict(ks, vs):
    return dict(zip(ks, vs))

main()
import scraperwiki
import lxml.html
import datetime

YEAR = '2013'

STATS = ['bats', 'name', 'g', 'pa', 'ab', 'r', 'h', 'dbl', 'tpl', 'hr', 'tb',
         'rbi', 'sb', 'cs', 'sh', 'sf', 'bb', 'ibb', 'hbp', 'so', 'gd']
STATS_LENGTH = len(STATS)
EASTS = ['f', 'g', 'e', 's', 'l', 'db', 'm']
WESTS = ['d', 'h', 't', 'bs', 'c']

BASE_URL = "http://bis.npb.or.jp/%s/stats/idb2_%s.html"

def main():
    def f(league):
        grand_total = {}
        for team in league:
            result, total = scrape(team)
            for d in result:
                d.update(calcStats(d))
                scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                                        data=d)
            grand_total = calcTotal(grand_total, total)
        grand_total.update(calcStats(grand_total))
        return grand_total

    east_total = f(EASTS)
    west_total = f(WESTS)
    east_total.update({'team': 'league', 'bats': None, 'name': 'east',
                       'year': YEAR})
    west_total.update({'team': 'league', 'bats': None, 'name': 'west',
                       'year': YEAR})
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=east_total)
    scraperwiki.sqlite.save(unique_keys=['name', 'team', 'year'],
                            data=west_total)


def calcStats(data):
    h = float(data['h'])                # hits
    ab = float(data['ab'])              # at bats
    dbl = float(data['dbl'])            # doules
    tpl = float(data['tpl'])            # triples
    hr = float(data['hr'])              # homeruns
    tb = float(data['tb'])              # total bases
    bb = float(data['bb'])              # bases on balls
    ibb = float(data['ibb'])            # intentional bbs
    hbp = float(data['hbp'])            # hit by pitches
    sh = float(data['sh'])              # sacrifice hits
    sf = float(data['sf'])              # sacrifice flies
    sb = float(data['sb'])              # stolen bases
    cs = float(data['cs'])              # caught stealing
    so = float(data['so'])              # strike outs
    gd = float(data['gd'])              # ground doubles
    sgl = h - dbl - tpl - hr            # singles
    
    avg = h / ab \
          if ab else None
    slg = tb / ab \
          if ab else None
    obp_a = h + bb + hbp
    obp_b = ab + bb + hbp + sf
    obp = obp_a / obp_b \
          if obp_b else None
    ops = slg + obp \
          if (slg is not None and obp is not None) else None
    noi = (obp + slg / 3) * 1000 \
          if (slg is not None and obp is not None) else None
    gpa = (obp * 1.8 + slg) / 4 \
          if (slg is not None and obp is not None) else None

    rc_a = h + bb + hbp - cs - gd
    rc_b = tb + 0.26 * (bb + hbp) + 0.53 * (sh + sf) + 0.64 * sb - 0.03 * so
    rc_c = ab + bb + hbp + sf + sh
    rc = (2.4 * rc_c + rc_a) * (3 * rc_c + rc_b) / (9 * rc_c) - 0.9 * rc_c\
         if rc_c else None
    rc27_a = ab - h + cs + sh + sf + gd
    rc27 = rc / rc27_a * 27 \
           if rc27_a else None

    xr = 0.50 * sgl + 0.72 * dbl + 1.04 * tpl + 1.44 * hr + \
         0.34 * (bb + hbp) + 0.25 * ibb + 0.18 * sb - 0.32 * cs - \
         0.09 * (ab - h - so) - 0.37 * gd + 0.37 * sf + 0.04 * sh
    xr27_a = rc27_a
    xr27 = xr / xr27_a * 27 \
           if xr27_a else None

    babip_a = h - hr
    babip_b = ab + sf - hr - so
    babip = babip_a / babip_b \
            if babip_b else None

    isop = slg - avg \
           if (avg is not None and slg is not None) else None
    isod = obp - avg \
           if (avg is not None and obp is not None) else None

    sbp = sb / (sb + cs) * 100 \
          if (sb or cs) else None

    def avgJust(n):
        if n is None:
            return None
        return str(n)[1:5].ljust(4, '0') if n < 1 else \
               str(n)[0:5].ljust(5, '0')
               
    def rcJust(n):
        if n is None:
            return None
        nn = round(n, 1)
        idx = str(nn).index('.')
        return str(nn)[:idx] + str(nn)[idx:].ljust(2, '0')

    avg = avgJust(avg)
    slg = avgJust(slg)
    obp = avgJust(obp)
    ops = avgJust(ops)
    gpa = avgJust(gpa)
    noi = str(round(noi, 1)) if noi else None
    rc = rcJust(rc)
    rc27 = rcJust(rc27)
    xr = rcJust(xr)
    xr27 = rcJust(xr27)
    babip = avgJust(babip)
    isop = avgJust(isop)
    isod = avgJust(isod)
    sbp = str(round(sbp, 1)) if sbp else None

    return {'avg': avg, 'slg': slg, 'obp': obp, 'ops': ops, 'noi': noi,
            'gpa': gpa, 'rc': rc, 'rc27': rc27, 'xr': xr, 'xr27': xr27,
            'babip': babip, 'isop': isop, 'isod': isod, 'sbp': sbp}


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
            for i in range(2, STATS_LENGTH):
                contents[i] = int(contents[i])
            
            data = zipdict(STATS, contents)
            data.update({'team': team, 'year': YEAR})
            data['bats'] = 'S' if data['bats'] == '+' else \
                           'L' if data['bats'] == '*' else \
                           'R'
            
            total = calcTotal(total, data)
            result.append(data)

    return result, total

def calcTotal(total, current):
    if total:
        for k in STATS[2:]:
            total[k] = total[k] + current[k]
    else:
        for k in STATS[2:]:
            total[k] = current[k]
    return total


def zipdict(ks, vs):
    return dict(zip(ks, vs))

main()
