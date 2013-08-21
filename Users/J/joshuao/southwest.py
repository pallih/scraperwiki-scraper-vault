import scraperwiki

# Blank Python
import re
import mechanize
import lxml.html
import time
import smtplib  

def sendEmail(message):
    server = 'smtp.gmail.com'
    port = 587
         
    sender = 'southwestalert@gmail.com'
    recipient = 'joshua@oskwarek.com'
    subject = 'Air Fare Drops Today'
    body = message
    print "1"        
    body = "<html><head></head><body><pre>" + body + "</pre></body></html>"
       
    headers = ["From: " + sender,
                   "Subject: " + subject,
                   "To: " + recipient,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
    headers = "\r\n".join(headers)
     
    
    # The actual mail send  
    print "2"
    server = smtplib.SMTP('smtp.gmail.com:587')  
    print "3"
    server.starttls()  
    print "4"
    server.login(sender,'happy1feet')  
    print "5"
    server.sendmail(sender, recipient, headers + "\r\n\r\n" + body)  
    print "6"
    server.quit()  

  

vtime = time.strftime( "%m/%d/%Y" )
print vtime
emailtxt = "Here is your list of fair drops: \r\n\r\n"
vdest = ""


response = mechanize.urlopen("http://m.southwest.com")
html = response.read()

#html = scraperwiki.scrape("http://m.southwest.com")
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):  
    if el.text.find('Air Reservations') <> -1:
        print el.text     
        print el.get('href')
        bookair = el.get('href')
        
response = mechanize.urlopen(bookair)
html = response.read()
#html = scraperwiki.scrape(bookair)
root = lxml.html.fromstring(html, )
for el in root.cssselect("a"):  
    if el.text.find('Book Air') <> -1:
        print el.text     
        print el.get('href')
        reserve = el.get('href')



def getMinPrice(from1,to1,month1,day1):
    global vdest
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(reserve)
    br.select_form(nr=0)
    print br.title()
    print br.geturl()
    
    br["listboxtriptype"] = ["0"]  # (the method here is __setitem__)
    br["listboxfrom"] = [from1]
    br["listboxto"] = [to1]
    br["listboxdepmon"] = [month1]
    br["listboxdepday"] = [day1]
    
    # Submit current form.  Browser calls .close() on the current response on
    # navigation, so this closes response1
    try:
        response2 = br.submit()
    except:
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(reserve)
        br.select_form(nr=0)
        print br.title()
        print br.geturl()
    
        br["listboxtriptype"] = ["0"]  # (the method here is __setitem__)
        br["listboxfrom"] = [from1]
        br["listboxto"] = [to1]
        br["listboxdepmon"] = [month1]
        br["listboxdepday"] = [day1]
        response2 = br.submit()           

        
    resp = response2.read()
    print resp
    p = re.compile('\$\d{1,3}')
    min = 5000
    for price in p.findall(resp):  
        if min > float(price.strip('$')):
         print float(price.strip('$'))
         min = float(price.strip('$'))

    root = lxml.html.fromstring(resp)
    vdest = root.cssselect("label.skHeader")[0].text_content()
    print vdest
    return min

def getPriceAndSave(from1,to1,month1,day1):
    global vdest
    global emailtxt
    minprice = getMinPrice(from1,to1,month1,day1)
    vmonth = str(int(month1) + 1)
    vday = str(int(day1) + 1)
    flightdate = vmonth + "/" + vday + "/2012"
    #record = {"c_pricedate" : vtime, "c_route" : vdest, "c_flightdate" : flightdate, "c_price" : minprice}    
    
    
    try:
        yesterdaysprice = scraperwiki.sqlite.select("c_price, c_lowestprice from prices where c_route = '" + vdest + "' and c_flightdate = '" + flightdate + "'")
        prevprice = yesterdaysprice[0]["c_price"]
        lowestprice = yesterdaysprice[0]["c_lowestprice"]
    except:
        prevprice = 5000
        lowestprice = 5000

    if minprice < lowestprice:
        print str(minprice) + " lower " + str(lowestprice)
        record = {"c_route" : vdest, "c_flightdate" : flightdate, "c_price" : minprice, "c_lowestprice" : minprice}    
    else:
        print str(minprice) + " higher " + str(lowestprice)
        record = {"c_route" : vdest, "c_flightdate" : flightdate, "c_price" : minprice, "c_lowestprice" : lowestprice}    

    emailtxt = emailtxt + vdest.rstrip('\r').rstrip('\n').rjust(50) + flightdate.rjust(12) + str(minprice).rjust(8) + str(lowestprice).rjust(8) + "\r"
    scraperwiki.sqlite.save(unique_keys=["c_route","c_flightdate"], data=record, table_name="Prices")

#JAX - BDL
getPriceAndSave("35","31","6","2")
getPriceAndSave("35","31","6","3")
getPriceAndSave("35","31","6","4")
getPriceAndSave("35","31","6","5")

#JAX - ALB
getPriceAndSave("35","1","6","2")
getPriceAndSave("35","1","6","3")
getPriceAndSave("35","1","6","4")
getPriceAndSave("35","1","6","5")

#BDL - LAX
getPriceAndSave("31","40","6","17")
getPriceAndSave("31","40","6","18")
getPriceAndSave("31","40","6","19")
getPriceAndSave("31","40","6","20")


#BDL - ONT
getPriceAndSave("31","44","6","17")
getPriceAndSave("31","44","6","18")
getPriceAndSave("31","44","6","19")
getPriceAndSave("31","44","6","20")


#BDL - SNA
getPriceAndSave("31","68","6","17")
getPriceAndSave("31","68","6","18")
getPriceAndSave("31","68","6","19")
getPriceAndSave("31","68","6","20")


#ALB - LAX
getPriceAndSave("1","40","6","17")
getPriceAndSave("1","40","6","18")
getPriceAndSave("1","40","6","19")
getPriceAndSave("1","40","6","20")


#ALB - ONT
getPriceAndSave("1","44","6","17")
getPriceAndSave("1","44","6","18")
getPriceAndSave("1","44","6","19")
getPriceAndSave("1","44","6","20")


#ALB - SNA
getPriceAndSave("1","68","6","17")
getPriceAndSave("1","68","6","18")
getPriceAndSave("1","68","6","19")
getPriceAndSave("1","68","6","20")


#JAX - LAX
getPriceAndSave("35","40","6","17")
getPriceAndSave("35","40","6","18")
getPriceAndSave("35","40","6","19")
getPriceAndSave("35","40","6","20")


#JAX - ONT
getPriceAndSave("35","67","6","17")
getPriceAndSave("35","67","6","18")
getPriceAndSave("35","67","6","19")


#JAX - SNA
getPriceAndSave("35","68","6","17")
getPriceAndSave("35","68","6","18")
getPriceAndSave("35","68","6","19")
getPriceAndSave("35","68","6","20")


#LAX - PHX
getPriceAndSave("35","68","6","17")
getPriceAndSave("35","68","6","18")
getPriceAndSave("35","68","6","19")
getPriceAndSave("35","68","6","20")


#ONT - PHX
getPriceAndSave("67","72","7","1")
getPriceAndSave("67","72","7","2")
getPriceAndSave("67","72","7","3")
getPriceAndSave("67","72","7","4")


#SNA - PHX
getPriceAndSave("68","72","7","1")
getPriceAndSave("68","72","7","2")
getPriceAndSave("68","72","7","3")
getPriceAndSave("68","72","7","4")


#PHX - BDL
getPriceAndSave("72","31","7","6")
getPriceAndSave("72","31","7","7")
getPriceAndSave("72","31","7","8")
getPriceAndSave("72","31","7","9")


#PHX - ALB
getPriceAndSave("72","1","7","6")
getPriceAndSave("72","1","7","7")
getPriceAndSave("72","1","7","8")
getPriceAndSave("72","1","7","9")


#PHX - JAX
getPriceAndSave("72","35","7","6")
getPriceAndSave("72","35","7","7")
getPriceAndSave("72","35","7","8")
getPriceAndSave("72","35","7","9")



print emailtxt
sendEmail(emailtxt)