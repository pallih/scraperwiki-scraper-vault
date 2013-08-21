import scraperwiki
scraperwiki.sqlite.attach("ie_pres_events_details")

data = scraperwiki.sqlite.select(           
    '''* from ie_pres_events_details.swdata 
    order by DATE desc limit 10'''
    
)
time = '' 
place = ''

#for d in data:
   # time = d["TIME_PLACE"].split("/(")

#    d["time"], d["place"] = d["TIME_PLACE"].split("/(")[2] 
#[2] #.strip().split(" ")


#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")https://scraperwiki.com/views/oshawa_events_calendar_ical/edit/


print "<table>"
print "<tr><th>DATE</th><th>TIME</th><th>PLACE</th><th>DETAILS</th>"
for d in data:
  print "<tr>"
  print "<td>", d["DATE"], "</td>"
  print "<td>", d["TIME_PLACE"].split("/("), "</td>"

  print "<td>", d["DETAILS"], "</td>"
  print "</tr>"
print "</table>"import scraperwiki
scraperwiki.sqlite.attach("ie_pres_events_details")

data = scraperwiki.sqlite.select(           
    '''* from ie_pres_events_details.swdata 
    order by DATE desc limit 10'''
    
)
time = '' 
place = ''

#for d in data:
   # time = d["TIME_PLACE"].split("/(")

#    d["time"], d["place"] = d["TIME_PLACE"].split("/(")[2] 
#[2] #.strip().split(" ")


#state, zipcode = addr.split("&nbsp;")[2].split(",")[1].strip().split(" ")https://scraperwiki.com/views/oshawa_events_calendar_ical/edit/


print "<table>"
print "<tr><th>DATE</th><th>TIME</th><th>PLACE</th><th>DETAILS</th>"
for d in data:
  print "<tr>"
  print "<td>", d["DATE"], "</td>"
  print "<td>", d["TIME_PLACE"].split("/("), "</td>"

  print "<td>", d["DETAILS"], "</td>"
  print "</tr>"
print "</table>"