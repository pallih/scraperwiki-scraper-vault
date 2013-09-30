import scraperwiki, re, time
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup as Soup
from urllib import urlopen
from urlparse import parse_qsl

url = "http://mwis.ru/index/page/1/type/"
port_re = re.compile('(.*?)document.write\(":"(.*?)\)')
time_re = re.compile('(\d+)')

#ip_string, port, proxy type, they checked at time, country

for page in xrange(1, 26):
    soup = Soup(urlopen(url % page))
    now = datetime.fromtimestamp(time.time())

    table = soup.find("table", "tablelist")
    
    script = soup.head.find(lambda tag: tag.name == 'script' and len(tag.attrs) == 1)

    #samair.ru use javascript to obfuscate the port numbers of proxies.
    #Every numeric digit is assigned to a variable(eg "k=0;d=8;") and document.write(":"+d+k) 
    #is later used to display the port number.
    #That they use semicolons as the separator is fortuitous
    port_nums = dict(parse_qsl(script.text))

    #The only rows with attributes is the header, any rows where the first cell has attributes or an anchor is an advert. All other rows are data
    for row in (r for r in table.findAll('tr')[1:] if not r.td.attrs and not r.td.a):
        ip_string, proxy_type, checked_at, country = (r.text for r in row.findAll('td'))

        match = port_re.match(ip_string)
        
        ip = match.group(1)
        port_string = match.group(2)

        port_chars = port_string.split('+')[1:]
        port = "".join([port_nums[char] for char in port_chars])

        mins_ago = time_re.search(checked_at).group(1)
        delta = timedelta(minutes=int(mins_ago))

        scraperwiki.sqlite.save(["ip", "port"], {"ip": ip, "port": port, "type": proxy_type, "checked_at": (now - delta).isoformat(), "country": country})
        
        
        import scraperwiki, re, time
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup as Soup
from urllib import urlopen
from urlparse import parse_qsl

url = "http://mwis.ru/index/page/1/type/"
port_re = re.compile('(.*?)document.write\(":"(.*?)\)')
time_re = re.compile('(\d+)')

#ip_string, port, proxy type, they checked at time, country

for page in xrange(1, 26):
    soup = Soup(urlopen(url % page))
    now = datetime.fromtimestamp(time.time())

    table = soup.find("table", "tablelist")
    
    script = soup.head.find(lambda tag: tag.name == 'script' and len(tag.attrs) == 1)

    #samair.ru use javascript to obfuscate the port numbers of proxies.
    #Every numeric digit is assigned to a variable(eg "k=0;d=8;") and document.write(":"+d+k) 
    #is later used to display the port number.
    #That they use semicolons as the separator is fortuitous
    port_nums = dict(parse_qsl(script.text))

    #The only rows with attributes is the header, any rows where the first cell has attributes or an anchor is an advert. All other rows are data
    for row in (r for r in table.findAll('tr')[1:] if not r.td.attrs and not r.td.a):
        ip_string, proxy_type, checked_at, country = (r.text for r in row.findAll('td'))

        match = port_re.match(ip_string)
        
        ip = match.group(1)
        port_string = match.group(2)

        port_chars = port_string.split('+')[1:]
        port = "".join([port_nums[char] for char in port_chars])

        mins_ago = time_re.search(checked_at).group(1)
        delta = timedelta(minutes=int(mins_ago))

        scraperwiki.sqlite.save(["ip", "port"], {"ip": ip, "port": port, "type": proxy_type, "checked_at": (now - delta).isoformat(), "country": country})
        
        
        