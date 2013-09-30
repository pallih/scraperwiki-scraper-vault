import scraperwiki
import urlparse
import lxml.html
import re

def get_lotto_page(year):
    base_url = 'http://www.lottery.co.uk/results/lotto/archive-%s.asp'
    url = base_url % year
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    draw_links = root.cssselect("div.main table div.floatLeft a")
    for link in draw_links:
        url = 'http://www.lottery.co.uk' + link.attrib.get('href')
        get_lotto_data(url)

def get_lotto_data(draw_url):
    html = scraperwiki.scrape(draw_url)
    root = lxml.html.fromstring(html)
    
    record = {}
    
    first_table = root.cssselect("table")[0] 

    #Get draw number
    draw_num = first_table.cssselect("th strong")[1].tail
    record['Draw number'] = draw_num
    
    #Get the date
    date = first_table.cssselect("th strong")[0].tail
    record['Date of draw'] = date 
    
    #Get the balls
    balls_html = first_table.cssselect("tbody table tr")[0]
    balls = [ball.text for ball in balls_html.cssselect("td")]
    bonus = balls[6]
    balls = balls[0:6]
    record['Balls drawn'] = balls
    record['Bonus ball'] = [bonus]
    
    #Get the prizes
    second_table = root.cssselect("table")[2] 
    combos = ["6", "5+", "5", "4", "3"]
    prize_table = second_table.cssselect("tbody tr")
    winner_numbers = []
    prize = []

    r = re.compile(r"\s+|,", re.MULTILINE)
    for i in range(5):
        winner_numbers += [r.sub("",prize_table[i].cssselect("td")[2].text)]
        prize += [r.sub("",prize_table[i].cssselect("td")[1].text)]
    record['Number of winners'] = dict(zip(combos,winner_numbers))
    record['Prize per winner'] = dict(zip(combos,prize))
    
    #Save record
    scraperwiki.sqlite.save(["Draw number"], record)


for i in range(2012, 1993, -1):
    print "Starting year " + str(i)
    get_lotto_page(i)import scraperwiki
import urlparse
import lxml.html
import re

def get_lotto_page(year):
    base_url = 'http://www.lottery.co.uk/results/lotto/archive-%s.asp'
    url = base_url % year
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    draw_links = root.cssselect("div.main table div.floatLeft a")
    for link in draw_links:
        url = 'http://www.lottery.co.uk' + link.attrib.get('href')
        get_lotto_data(url)

def get_lotto_data(draw_url):
    html = scraperwiki.scrape(draw_url)
    root = lxml.html.fromstring(html)
    
    record = {}
    
    first_table = root.cssselect("table")[0] 

    #Get draw number
    draw_num = first_table.cssselect("th strong")[1].tail
    record['Draw number'] = draw_num
    
    #Get the date
    date = first_table.cssselect("th strong")[0].tail
    record['Date of draw'] = date 
    
    #Get the balls
    balls_html = first_table.cssselect("tbody table tr")[0]
    balls = [ball.text for ball in balls_html.cssselect("td")]
    bonus = balls[6]
    balls = balls[0:6]
    record['Balls drawn'] = balls
    record['Bonus ball'] = [bonus]
    
    #Get the prizes
    second_table = root.cssselect("table")[2] 
    combos = ["6", "5+", "5", "4", "3"]
    prize_table = second_table.cssselect("tbody tr")
    winner_numbers = []
    prize = []

    r = re.compile(r"\s+|,", re.MULTILINE)
    for i in range(5):
        winner_numbers += [r.sub("",prize_table[i].cssselect("td")[2].text)]
        prize += [r.sub("",prize_table[i].cssselect("td")[1].text)]
    record['Number of winners'] = dict(zip(combos,winner_numbers))
    record['Prize per winner'] = dict(zip(combos,prize))
    
    #Save record
    scraperwiki.sqlite.save(["Draw number"], record)


for i in range(2012, 1993, -1):
    print "Starting year " + str(i)
    get_lotto_page(i)