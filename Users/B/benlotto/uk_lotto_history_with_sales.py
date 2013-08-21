import scraperwiki
import lxml.html
import re
import time

def get_lotto_data(draw_number):
    #from h1756 import html
    base_url = "http://lottery.merseyworld.com/archive/Lott00%s.html"
    draw_url = base_url % draw_number
    html = scraperwiki.scrape(draw_url)
    root = lxml.html.fromstring(html)
    #root  = lxml.html.parse(draw_url).getroot()
    record = {}
    
    #Get draw number
    record['Draw number'] = draw_number
    
    #Get the date
    date = root.cssselect("body h3 a")[0].tail
    r = re.compile("(^.*on\s)|(:\s*$)")
    record['Date of draw'] = r.sub("",date)
    
    #Get the balls
    balls_html = root.cssselect("body p img")[1]
    balls_text = re.search(r'alt="([^"]+)"', lxml.html.tostring(balls_html), re.M|re.I).group(1)
    balls = [b[0]+b[1] for b in re.findall("(?:\A|[^(])(?:0(\d)|(\d{2}))", balls_text)]
    b = re.findall("\(0(\d)\)|\((\d{2})\)", balls_text)[0]
    bonus = [b[0]+b[1]]
    record['Balls drawn'] = balls
    record['Bonus ball'] = bonus
    
    #Get the prizes
    prize_table = root.cssselect("pre b")[0].tail
    prizes = re.findall("\xa3([\d,]+)\s+([\d,]+).*%", prize_table, re.M|re.I)
    combos = ["6", "5+", "5", "4", "3"]
    r = re.compile(",")
    winner_numbers = [int(r.sub("",p[1])) for p in prizes]
    prize = [int(r.sub("",p[0])) for p in prizes]
    record['Number of winners'] = dict(zip(combos,winner_numbers))
    record['Prize per winner'] = dict(zip(combos,prize))
    
    print record
    
    #Get sales
    sales_table = root.cssselect("pre font")[0].tail
    sales = re.findall("\xa3([\d,]+)", sales_table)[0]
    sales = int(r.sub("",sales))
    record['Sales'] = sales
    
    #Save record
    scraperwiki.sqlite.save(["Draw number"], record)
    #return record

for i in range(9,0,-1):
  get_lotto_data(i)
  time.sleep(30)

"""
record = {'Number of winners': {'3': 1073695, '5': 2139, '4': 76731, '5+': 39, '6': 7}, 'Bonus ball': ['10'], 'Prize per winner': {'3': 10, '5': 528, '4': 32, '5+': 46349, '6': 839254}, 'Balls drawn': ['3', '5', '14', '22', '30', '44'], 'Draw number': 1, 'Date of draw': 'Saturday 19th November 1994'}
record['Sales'] = 22004123

scraperwiki.sqlite.save(["Draw number"], record)
"""