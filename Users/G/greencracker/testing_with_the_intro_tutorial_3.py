import scraperwiki
html = scraperwiki.scrape("http://www.gaepd.org/pls/enfo/epdorders.i_orders")
import lxml.html
root = lxml.html.fromstring(html)


for td in root.cssselect("table"): #read backwards: "find every table that is in the website and consider its <td>   tags
    tds = td.cssselect("td") #those <td> tags you are considering, let's call them collectively "tds." Here, there happen to be 18 <td>s in each table
    data = { 
      'dateposted' : tds[13].text_content(),
      'settlement' : tds[11].text_content(),
      'requirement' : tds[9].text_content(),
      'cause' : tds[7].text_content(),
      'facility' : tds[1].text_content(),
      'location' : tds[3].text_content(),
      'order_number' : tds[5].text_content(), 
      


    }
    print data #optional boilerplate
    scraperwiki.sqlite.save(unique_keys=['order_number'], data=data)#"computer, that column we called 'agenda' will have unique values. the total table we are creating will be called 'schedule'.
#data=data, idunno, is boilerplate
#then somehow, this goes back up to line 7 and starts over, but this time grabbs the second <tr> on the website. The three cells in the second row get assigned to the columns you called 'agenda' 'meeting_time' and 'place'. 


import scraperwiki
html = scraperwiki.scrape("http://www.gaepd.org/pls/enfo/epdorders.i_orders")
import lxml.html
root = lxml.html.fromstring(html)


for td in root.cssselect("table"): #read backwards: "find every table that is in the website and consider its <td>   tags
    tds = td.cssselect("td") #those <td> tags you are considering, let's call them collectively "tds." Here, there happen to be 18 <td>s in each table
    data = { 
      'dateposted' : tds[13].text_content(),
      'settlement' : tds[11].text_content(),
      'requirement' : tds[9].text_content(),
      'cause' : tds[7].text_content(),
      'facility' : tds[1].text_content(),
      'location' : tds[3].text_content(),
      'order_number' : tds[5].text_content(), 
      


    }
    print data #optional boilerplate
    scraperwiki.sqlite.save(unique_keys=['order_number'], data=data)#"computer, that column we called 'agenda' will have unique values. the total table we are creating will be called 'schedule'.
#data=data, idunno, is boilerplate
#then somehow, this goes back up to line 7 and starts over, but this time grabbs the second <tr> on the website. The three cells in the second row get assigned to the columns you called 'agenda' 'meeting_time' and 'place'. 


