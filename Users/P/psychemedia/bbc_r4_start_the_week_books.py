import scraperwiki, simplejson, re,urllib

url='http://www.bbc.co.uk/programmes/b006r9xr/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

def getProgDetails(pid):
    purl='http://www.bbc.co.uk/programmes/'+pid+'.json'
    details=simplejson.load(urllib.urlopen(purl))
    print details
    p=details['programme']
    #supp=p['supporting_content_items'][0]['content']
    pid=p['pid']
    prog=p['parent']['programme']['title']
    record={'series':prog,'title':p['short_synopsis'],'pid':pid, 'progPid':pid,'meddesc':p['medium_synopsis'],'longdesc':p['long_synopsis']}
    scraperwiki.sqlite.save(["pid"], record)

    for supp in p['supporting_content_items']:
        pid2=pid+'_'+supp['title']
        record={'series':prog,'title':supp['title'],'pid':pid2, 'progPid':pid,'longdesc':supp['content']}
        scraperwiki.sqlite.save(["pid"], record)

done=['b011zm16', 'b011tz8f', 'b011p723', 'b011j458', 'b0118cxv', 'b01132kh', 'b010y34w', 'b010t3p0', 'b010m19r', 'b010dhcp', 'b0105vth', 'b00zzqy9', 'b00zs806', 'b00zlcp3', 'b00zdbhz', 'b00z58b0', 'b00yy8xf', 'b00yqg7v', 'b00yhynw', 'b00y5d57', 'b00y288b', 'b00xpj0w', 'b00xhb23', 'b00x8hdz', 'b00wr5rr', 'b00wp012', 'b00wlbsq', 'b00wdf42', 'b00w77g4', 'b00w14h4', 'b00vw20v', 'b00vrcwm', 'b00vkpk4', 'b00vhf1s', 'b00vcmp7', 'b00v6hts', 'b00v1mtz', 'b00txgs3', 'b00tt49v', 'b00sx2bx', 'b00stlrh', 'b00srhrz', 'b00snqfn', 'b00slpn0', 'b00sj4vn', 'b00sfw4b', 'b00scgxw', 'b00s91s2', 'b00s5nt5', 'b00s2v8n', 'b00s090v', 'b00rxdr8', 'b00rrhyd', 'b00rlzdz', 'b00rdvr0', 'b00r9y85', 'b00r4tf8', 'b00qzvdf', 'b00qts53', 'b00qp09n', 'b00qgvzt', 'b00qbt26', 'b00q2w7y', 'b00pxj6d', 'b00pqfjh', 'b00pfp8j', 'b00pbw1n', 'b00p87qw', 'b00p50f5', 'b00p1nm0', 'b00ny7k0', 'b00ntlyg', 'b00npjnj', 'b00njkl6', 'b00ndwc2', 'b00n7ymb', 'b00n4z9q', 'b00n03zb', 'b00lny46', 'b00ljqf3', 'b00lg31l', 'b00lb26r', 'b00l53x4', 'b00kwr5d', 'b00kslkl', 'b00knpc9', 'b00kj2dw', 'b00kcr2n', 'b00k89pp', 'b00k3n07', 'b00jwxz0', 'b00jr4qt', 'b00jlzxd', 'b00jh4f5', 'b00jcdb7', 'b00j67mh', 'b00j3v39', 'b00hzd79', 'b00htgdn', 'b00hpdp1', 'b00hhthl', 'b00hbs58', 'b00h62pk', 'b00gvggf', 'b00gqzvw', 'b00gkz10', 'b0128l6y', 'b0122szw', 'b00g4frd', 'b00g2vb3', 'b00fz0w8', 'b00fsxxl', 'b00fpx7g', 'b00fkw8j', 'b00fgpt3', 'b00f9k6l', 'b00f6mhc', 'b00f3f14', 'b00dz7s7', 'b00dv01n', 'b00dqlhg', 'b00chlgz', 'b00cdc5f', 'b00c7r2n', 'b00c4qx8', 'b00c0l02', 'b00bylpj', 'b00bvlly', 'b00bfn8s', 'b00bbhpn', 'b00b70yk', 'b00b0j1s', 'b009xmmw']

for d in data:
    p = d['programme']
    if p['pid'] not in done:
        print 'Fetching prog',p['pid'],p
        getProgDetails(p['pid'])
        done.append(p['pid'])    
        print 'Done:',done   
print 'ok...'import scraperwiki, simplejson, re,urllib

url='http://www.bbc.co.uk/programmes/b006r9xr/episodes/player.json'

data=simplejson.load(urllib.urlopen(url))['episodes']

def getProgDetails(pid):
    purl='http://www.bbc.co.uk/programmes/'+pid+'.json'
    details=simplejson.load(urllib.urlopen(purl))
    print details
    p=details['programme']
    #supp=p['supporting_content_items'][0]['content']
    pid=p['pid']
    prog=p['parent']['programme']['title']
    record={'series':prog,'title':p['short_synopsis'],'pid':pid, 'progPid':pid,'meddesc':p['medium_synopsis'],'longdesc':p['long_synopsis']}
    scraperwiki.sqlite.save(["pid"], record)

    for supp in p['supporting_content_items']:
        pid2=pid+'_'+supp['title']
        record={'series':prog,'title':supp['title'],'pid':pid2, 'progPid':pid,'longdesc':supp['content']}
        scraperwiki.sqlite.save(["pid"], record)

done=['b011zm16', 'b011tz8f', 'b011p723', 'b011j458', 'b0118cxv', 'b01132kh', 'b010y34w', 'b010t3p0', 'b010m19r', 'b010dhcp', 'b0105vth', 'b00zzqy9', 'b00zs806', 'b00zlcp3', 'b00zdbhz', 'b00z58b0', 'b00yy8xf', 'b00yqg7v', 'b00yhynw', 'b00y5d57', 'b00y288b', 'b00xpj0w', 'b00xhb23', 'b00x8hdz', 'b00wr5rr', 'b00wp012', 'b00wlbsq', 'b00wdf42', 'b00w77g4', 'b00w14h4', 'b00vw20v', 'b00vrcwm', 'b00vkpk4', 'b00vhf1s', 'b00vcmp7', 'b00v6hts', 'b00v1mtz', 'b00txgs3', 'b00tt49v', 'b00sx2bx', 'b00stlrh', 'b00srhrz', 'b00snqfn', 'b00slpn0', 'b00sj4vn', 'b00sfw4b', 'b00scgxw', 'b00s91s2', 'b00s5nt5', 'b00s2v8n', 'b00s090v', 'b00rxdr8', 'b00rrhyd', 'b00rlzdz', 'b00rdvr0', 'b00r9y85', 'b00r4tf8', 'b00qzvdf', 'b00qts53', 'b00qp09n', 'b00qgvzt', 'b00qbt26', 'b00q2w7y', 'b00pxj6d', 'b00pqfjh', 'b00pfp8j', 'b00pbw1n', 'b00p87qw', 'b00p50f5', 'b00p1nm0', 'b00ny7k0', 'b00ntlyg', 'b00npjnj', 'b00njkl6', 'b00ndwc2', 'b00n7ymb', 'b00n4z9q', 'b00n03zb', 'b00lny46', 'b00ljqf3', 'b00lg31l', 'b00lb26r', 'b00l53x4', 'b00kwr5d', 'b00kslkl', 'b00knpc9', 'b00kj2dw', 'b00kcr2n', 'b00k89pp', 'b00k3n07', 'b00jwxz0', 'b00jr4qt', 'b00jlzxd', 'b00jh4f5', 'b00jcdb7', 'b00j67mh', 'b00j3v39', 'b00hzd79', 'b00htgdn', 'b00hpdp1', 'b00hhthl', 'b00hbs58', 'b00h62pk', 'b00gvggf', 'b00gqzvw', 'b00gkz10', 'b0128l6y', 'b0122szw', 'b00g4frd', 'b00g2vb3', 'b00fz0w8', 'b00fsxxl', 'b00fpx7g', 'b00fkw8j', 'b00fgpt3', 'b00f9k6l', 'b00f6mhc', 'b00f3f14', 'b00dz7s7', 'b00dv01n', 'b00dqlhg', 'b00chlgz', 'b00cdc5f', 'b00c7r2n', 'b00c4qx8', 'b00c0l02', 'b00bylpj', 'b00bvlly', 'b00bfn8s', 'b00bbhpn', 'b00b70yk', 'b00b0j1s', 'b009xmmw']

for d in data:
    p = d['programme']
    if p['pid'] not in done:
        print 'Fetching prog',p['pid'],p
        getProgDetails(p['pid'])
        done.append(p['pid'])    
        print 'Done:',done   
print 'ok...'