import scraperwiki
import urllib2

def get_html(url, proxy):
    proxy_handler = urllib2.ProxyHandler({'http':proxy})
    opener = urllib2.build_opener(proxy_handler)
    f = opener.open(url)
    return f.read()

def test_proxies():
    requestcount = 0
    requestlimit = 2
    currentproxy = 0
    scraperwiki.sqlite.attach("prx")
    proxies = scraperwiki.sqlite.select("* from prx.swdata where (port='80' or port='8080') and (type='A' or type='HA') and rsp > 0 order by rsp ASC")
    starting_url = 'http://proxyipchecker.com/check-my-proxy-ip.html'
    postcodes = [1,2,3,4,5,6,7,8,9,10]
    for postcode in postcodes:
        if requestcount == requestlimit:
            if currentproxy >= len(proxies)-1:
                currentproxy = 0
                requestcount = 0
            else:
                currentproxy = currentproxy + 1
                requestcount  = 0
        url = starting_url
        print(proxies[currentproxy]['adr'])
        print(get_html(url, proxies[currentproxy]['adr']))
        requestcount = requestcount + 1

print(get_html('http://proxyipchecker.com/check-my-proxy-ip.html', 'http://203.142.64.106:80'))
import scraperwiki
import urllib2

def get_html(url, proxy):
    proxy_handler = urllib2.ProxyHandler({'http':proxy})
    opener = urllib2.build_opener(proxy_handler)
    f = opener.open(url)
    return f.read()

def test_proxies():
    requestcount = 0
    requestlimit = 2
    currentproxy = 0
    scraperwiki.sqlite.attach("prx")
    proxies = scraperwiki.sqlite.select("* from prx.swdata where (port='80' or port='8080') and (type='A' or type='HA') and rsp > 0 order by rsp ASC")
    starting_url = 'http://proxyipchecker.com/check-my-proxy-ip.html'
    postcodes = [1,2,3,4,5,6,7,8,9,10]
    for postcode in postcodes:
        if requestcount == requestlimit:
            if currentproxy >= len(proxies)-1:
                currentproxy = 0
                requestcount = 0
            else:
                currentproxy = currentproxy + 1
                requestcount  = 0
        url = starting_url
        print(proxies[currentproxy]['adr'])
        print(get_html(url, proxies[currentproxy]['adr']))
        requestcount = requestcount + 1

print(get_html('http://proxyipchecker.com/check-my-proxy-ip.html', 'http://203.142.64.106:80'))
