# Value tyres Fitting Stations In Wales

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

url = 'http://www.valuetyres.co.uk/fittingsearch.php?searchtype=region&region=15'

print '<h2>Map Of Fitting Stations In Wales</h2>'
print '<div>test</div>'
html = scraperwiki.scrape(url)

soup = BeautifulSoup(html)

hrefs= soup.findAll('a') 

for href in hrefs:
    try:
        if href['class'] == 'companyaddress':
            AddressArray = str(href).split('<br />')

            print AddressArray[len(AddressArray) - 2]
            
    except Exception as e:
        a = 1 + 2


#the preview doesn't support java script
#also this would work cus of api keys

#print "<script type='text/javascript'>";
#print "var localSearch = new GlocalSearch();";
#print "var userCentre;";
#print "if (GBrowserIsCompatible())";
#print  "{";
#print "var map = new GMap2(document.getElementById('map_canvas'));";
#print "map.setCenter(new GLatLng(50,50), 10);  map.addControl(new GSmallMapControl()); map.addControl(new GMapTypeControl());";
#print "var baseIcon = new GIcon(G_DEFAULT_ICON);";
#print "baseIcon.shadow = 'http://www.google.com/mapfiles/shadow50.png';";
#print "baseIcon.iconSize = new GSize(45, 34);";
#print  "baseIcon.shadowSize = new GSize(45, 34);";
#print "baseIcon.iconAnchor = new GPoint(45, 34);";
#print "baseIcon.infoWindowAnchor = new GPoint(45, 34);";
#print "baseIcon.imageMap = [0,0, 44,0, 44,33, 0,33];";

#print "}"
#print "}";
#print "</script>";

#print "function createMarker(latlng, number, fsid, imageurl, info)";#
#print "{";
#print "var letteredIcon = new GIcon(baseIcon);";
#print "letteredIcon.image = imageurl;";
#print "markerOptions = { icon:letteredIcon };";
#print "var marker = new GMarker(latlng,markerOptions);";
#print "marker.value = number;";
#print "GEvent.addListener(marker,'click', function()";
#print map + "{";
#print "var myHtml = '<b>' + fsid + '</b><br/>' + info;";
#print "map.openInfoWindowHtml(latlng, myHtml);";
#print " });";
#print "return marker;";
#print "}";

#print "localSearch.setSearchCompleteCallback(null,function()";
#print "{";
#print "if (localSearch.results[0])";
#print "{";
#print  "var resultLat = localSearch.results[0].lat;";
#print "var resultLng = localSearch.results[0].lng;";
#print  "var point = new GLatLng(resultLat, resultLng);";
#print  "userCentre = point;";
#print "map.addOverlay(createMarker(point,0,'Home','https://www.tyretraders.com/images/home.png', ' This is the geographical point of the postcode you entered.'));";
#print "}";
#print  "else";
#print "{";
#print "alert('Postcode not found!');";
#print "}";
#print "}";
#print ");";
#print "localSearch.execute('" + postcode.Text + "', 'UK');";
#
                #foreach item on map
#                    print "var localSearch" + I + " = new GlocalSearch();";
#                    print "localSearch" + I + ".setSearchCompleteCallback(null,function()";
#                    print "{";
#                    print "if (localSearch" + I + ".results[0])";
#                    print "{";
#                    print "var resultLat = localSearch" + I + ".results[0].lat;";
#                    print "var resultLng = localSearch" + I + ".results[0].lng;";
#                    print "var garpoint" + I + " = new GLatLng(resultLat, resultLng);";
#                    print "var num = " + row["Distance"].ToString() + ";";
#                   print "map.addOverlay(createMarker(garpoint" + I + "," + I + ",'" + row["FittingCentreID"].ToString() +"','https://www.tyretraders.com/images/tire.gif', 'Approx Distance: ' + ((userCentre.distanceFrom(garpoint" + I + ")) / 1600).toFixed(2) + ' Miles<br /> <a href=\"findFittingStation.aspx?postcode=" + postcode.Text + "&selectedfs=" + row["FittingCentreID"].ToString() + "\">View More Info On The Garage</a>'));";
#                    print "}";
#                    print "else";
#                    print "{";
#                    print "alert('We seem to be having some trouble finding the post code of one of our fitting partners. For more information on this garage please contact us on 01215688000 with the garage reference: " + row["FittingCentreID"].ToString() + "');";
#                    print "}";
#                    print  "}";
#                    print ");";
#                    print  "localSearch" + I + ".execute('" + row["PostCode"].ToString() + "', 'UK');";
                    
                    
                    

#            print "}";
#            print "</script>";# Value tyres Fitting Stations In Wales

import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

url = 'http://www.valuetyres.co.uk/fittingsearch.php?searchtype=region&region=15'

print '<h2>Map Of Fitting Stations In Wales</h2>'
print '<div>test</div>'
html = scraperwiki.scrape(url)

soup = BeautifulSoup(html)

hrefs= soup.findAll('a') 

for href in hrefs:
    try:
        if href['class'] == 'companyaddress':
            AddressArray = str(href).split('<br />')

            print AddressArray[len(AddressArray) - 2]
            
    except Exception as e:
        a = 1 + 2


#the preview doesn't support java script
#also this would work cus of api keys

#print "<script type='text/javascript'>";
#print "var localSearch = new GlocalSearch();";
#print "var userCentre;";
#print "if (GBrowserIsCompatible())";
#print  "{";
#print "var map = new GMap2(document.getElementById('map_canvas'));";
#print "map.setCenter(new GLatLng(50,50), 10);  map.addControl(new GSmallMapControl()); map.addControl(new GMapTypeControl());";
#print "var baseIcon = new GIcon(G_DEFAULT_ICON);";
#print "baseIcon.shadow = 'http://www.google.com/mapfiles/shadow50.png';";
#print "baseIcon.iconSize = new GSize(45, 34);";
#print  "baseIcon.shadowSize = new GSize(45, 34);";
#print "baseIcon.iconAnchor = new GPoint(45, 34);";
#print "baseIcon.infoWindowAnchor = new GPoint(45, 34);";
#print "baseIcon.imageMap = [0,0, 44,0, 44,33, 0,33];";

#print "}"
#print "}";
#print "</script>";

#print "function createMarker(latlng, number, fsid, imageurl, info)";#
#print "{";
#print "var letteredIcon = new GIcon(baseIcon);";
#print "letteredIcon.image = imageurl;";
#print "markerOptions = { icon:letteredIcon };";
#print "var marker = new GMarker(latlng,markerOptions);";
#print "marker.value = number;";
#print "GEvent.addListener(marker,'click', function()";
#print map + "{";
#print "var myHtml = '<b>' + fsid + '</b><br/>' + info;";
#print "map.openInfoWindowHtml(latlng, myHtml);";
#print " });";
#print "return marker;";
#print "}";

#print "localSearch.setSearchCompleteCallback(null,function()";
#print "{";
#print "if (localSearch.results[0])";
#print "{";
#print  "var resultLat = localSearch.results[0].lat;";
#print "var resultLng = localSearch.results[0].lng;";
#print  "var point = new GLatLng(resultLat, resultLng);";
#print  "userCentre = point;";
#print "map.addOverlay(createMarker(point,0,'Home','https://www.tyretraders.com/images/home.png', ' This is the geographical point of the postcode you entered.'));";
#print "}";
#print  "else";
#print "{";
#print "alert('Postcode not found!');";
#print "}";
#print "}";
#print ");";
#print "localSearch.execute('" + postcode.Text + "', 'UK');";
#
                #foreach item on map
#                    print "var localSearch" + I + " = new GlocalSearch();";
#                    print "localSearch" + I + ".setSearchCompleteCallback(null,function()";
#                    print "{";
#                    print "if (localSearch" + I + ".results[0])";
#                    print "{";
#                    print "var resultLat = localSearch" + I + ".results[0].lat;";
#                    print "var resultLng = localSearch" + I + ".results[0].lng;";
#                    print "var garpoint" + I + " = new GLatLng(resultLat, resultLng);";
#                    print "var num = " + row["Distance"].ToString() + ";";
#                   print "map.addOverlay(createMarker(garpoint" + I + "," + I + ",'" + row["FittingCentreID"].ToString() +"','https://www.tyretraders.com/images/tire.gif', 'Approx Distance: ' + ((userCentre.distanceFrom(garpoint" + I + ")) / 1600).toFixed(2) + ' Miles<br /> <a href=\"findFittingStation.aspx?postcode=" + postcode.Text + "&selectedfs=" + row["FittingCentreID"].ToString() + "\">View More Info On The Garage</a>'));";
#                    print "}";
#                    print "else";
#                    print "{";
#                    print "alert('We seem to be having some trouble finding the post code of one of our fitting partners. For more information on this garage please contact us on 01215688000 with the garage reference: " + row["FittingCentreID"].ToString() + "');";
#                    print "}";
#                    print  "}";
#                    print ");";
#                    print  "localSearch" + I + ".execute('" + row["PostCode"].ToString() + "', 'UK');";
                    
                    
                    

#            print "}";
#            print "</script>";