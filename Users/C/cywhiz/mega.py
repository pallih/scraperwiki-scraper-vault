import mechanize


b = mechanize.Browser()
b.set_handle_robots(False)



#b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.open('http://ca.megabus.com/JourneyResults.aspx?originCode=145&destinationCode=95&outboundDepartureDate=07%2f02%2f2013&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundWheelchairStowed=0&inboundWheelchairSeated=0&inboundWheelchairStowed=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=TRYMEGABUS&withReturn=0')
b.select_form(name="form1")

b.form.find_control(name='ScriptManager1_HiddenField').readonly = False
#b.form.find_control(name='__EVENTTARGET').readonly = False
#b.form.find_control(name='__EVENTARGUMENT').readonly = False
b.form.find_control(name='__VIEWSTATE').readonly = False



b.form['ScriptManager1_HiddenField'] = ''
#b.form['__EVENTTARGET'] = ''
#b.form['__EVENTARGUMENT'] = ''
b.form['__VIEWSTATE'] = ''
print b.submit().read()


import mechanize


b = mechanize.Browser()
b.set_handle_robots(False)



#b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.open('http://ca.megabus.com/JourneyResults.aspx?originCode=145&destinationCode=95&outboundDepartureDate=07%2f02%2f2013&inboundDepartureDate=&passengerCount=1&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundWheelchairStowed=0&inboundWheelchairSeated=0&inboundWheelchairStowed=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=TRYMEGABUS&withReturn=0')
b.select_form(name="form1")

b.form.find_control(name='ScriptManager1_HiddenField').readonly = False
#b.form.find_control(name='__EVENTTARGET').readonly = False
#b.form.find_control(name='__EVENTARGUMENT').readonly = False
b.form.find_control(name='__VIEWSTATE').readonly = False



b.form['ScriptManager1_HiddenField'] = ''
#b.form['__EVENTTARGET'] = ''
#b.form['__EVENTARGUMENT'] = ''
b.form['__VIEWSTATE'] = ''
print b.submit().read()


