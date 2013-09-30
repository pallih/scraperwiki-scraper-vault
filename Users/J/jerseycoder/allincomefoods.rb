# Blank Ruby
require 'nokogiri'
require "net/http"
require "uri"

# Farmer's Markets (searchType 3) in San Francisco which accept foodstamps
# searchType 2 = Restaurants which accept foodstamps
# searchType 1 = Places which give cash for EBT
# searchType 4 = Everything (including groceries, restaurants, and farmers markets - if you select this option, you
# can filter out Restaurants and farmers markets because they are returned fields yes/no

# This baseUrl would get passed in from Rails based on the address sent via SMS from the user
# presumably, the user is supplying both a street address and city name
# first, we geolocate the user and determine what zipcode they are in:

# this incoming format will have to be done somewhere since presumably the address information submitted by the user via SMS
# will not be in perfect get parameter query format
incomingstreetaddy= URI.escape("85 2nd st", Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"));
incomingcity=URI.escape("San Francisco", Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"));
incomingst="ca";

def get_geo_and_zip_from_address(staddress,stcity, st)
  #using a free USC geocoder (limit 2500 hits before you need to register)
  geocoder = "http://webgis.usc.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V02_95.aspx?apiKey=a8dbf3d653e345b8b67792e55b263d15&&format=XML&census=false&notStore=false&version=2.95&verbose=true&"
  staddress= "streetAddress=" + staddress;
  stcity = "&city=" + stcity;
  st = "&state="+ st;   
     request = geocoder + staddress + stcity + st
  puts(request + "\n")
     url = URI.parse(request)
     resp = Net::HTTP.get_response(url)
     #puts(resp.body)
      array = []
     #parse result if result received properly
     if resp.is_a?(Net::HTTPSuccess)
      #puts("Got here \n")
       #parse the XML
       parse = Nokogiri::XML(resp.body)
      status = parse.xpath("//QueryStatusCodeValue").text;
      # puts(status)
       #check if request went well
       if status == "200"
        # return zip and lat long if request successful
          lat = parse.xpath("//OutputGeocode//Latitude").text;
          long = parse.xpath("//OutputGeocode/Longitude").text;
          zip = parse.xpath("//ReferenceFeature/Zip").text;
       # puts("lat: " + lat + " long: " + long + " zip: " + zip + "\n")
           infohash = { 'lat' => lat, 'long' => long, 'zip' => zip  }
         end 
         # puts("infohash: " + infohash["zip"]);    
         return infohash
       end
   end

# set the return from the function (which is an array) to an array called usergeo
usergeo = get_geo_and_zip_from_address(incomingstreetaddy,incomingcity,incomingst)

baseUrl = "http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip?zip=" + usergeo["zip"];
puts(baseUrl);
next_link = " ";
next_url = baseUrl;

while next_link
  pagey = ScraperWiki.scrape(next_url)
  fsData = Nokogiri::HTML(pagey)
  whodoc = fsData.xpath("//div[@id='printReady']//tr[@class='RowOdd']")
  $items = whodoc.length
  $i = 0;
  while $i < $items
    ta = whodoc[$i];
    tarr = ta.xpath("td")
    retailergeo = get_geo_and_zip_from_address(URI.escape(tarr[1].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")),URI.escape(tarr[2].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")), URI.escape(tarr[3].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")));
    ScraperWiki.save(['retailer', 'streetaddress', 'city', 'state', 'zipcode', 'restaurant', 'farmmkt', 'lat', 'long'], {'retailer' => tarr[0].text, 'streetaddress' => tarr[1].text, 'city' => tarr[2].text, 'state' => tarr[3].text, 'zipcode' => tarr[4].text, 'restaurant' => tarr[5].text, 'farmmkt' => tarr[6].text, 'lat' => retailergeo["lat"], 'long' => retailergeo["long"]});
    $i +=1;
  end
# This gets you the contents of the href call which is javascript which contains the next page num. Now we need to regexp it
    next_link = fsData.xpath("//a[text()='>>']//@href").text
    txt = next_link
# Regexp code generated using http://txt2re.com/
    re1='.*?'  # Non-greedy match on filler
    re2='(\\d+)'  # Integer Number 1
    re=(re1+re2)
    m=Regexp.new(re,Regexp::IGNORECASE);
    if m.match(txt)
      int1=m.match(txt)[1];
      puts ""<<int1<<""<< "\n";
# code to iterate through scraping each next page....
      next_url = baseUrl + "&startIndex=" + int1;
      puts next_url;
    else
      next_link = false;
    end
end



# Blank Ruby
require 'nokogiri'
require "net/http"
require "uri"

# Farmer's Markets (searchType 3) in San Francisco which accept foodstamps
# searchType 2 = Restaurants which accept foodstamps
# searchType 1 = Places which give cash for EBT
# searchType 4 = Everything (including groceries, restaurants, and farmers markets - if you select this option, you
# can filter out Restaurants and farmers markets because they are returned fields yes/no

# This baseUrl would get passed in from Rails based on the address sent via SMS from the user
# presumably, the user is supplying both a street address and city name
# first, we geolocate the user and determine what zipcode they are in:

# this incoming format will have to be done somewhere since presumably the address information submitted by the user via SMS
# will not be in perfect get parameter query format
incomingstreetaddy= URI.escape("85 2nd st", Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"));
incomingcity=URI.escape("San Francisco", Regexp.new("[^#{URI::PATTERN::UNRESERVED}]"));
incomingst="ca";

def get_geo_and_zip_from_address(staddress,stcity, st)
  #using a free USC geocoder (limit 2500 hits before you need to register)
  geocoder = "http://webgis.usc.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V02_95.aspx?apiKey=a8dbf3d653e345b8b67792e55b263d15&&format=XML&census=false&notStore=false&version=2.95&verbose=true&"
  staddress= "streetAddress=" + staddress;
  stcity = "&city=" + stcity;
  st = "&state="+ st;   
     request = geocoder + staddress + stcity + st
  puts(request + "\n")
     url = URI.parse(request)
     resp = Net::HTTP.get_response(url)
     #puts(resp.body)
      array = []
     #parse result if result received properly
     if resp.is_a?(Net::HTTPSuccess)
      #puts("Got here \n")
       #parse the XML
       parse = Nokogiri::XML(resp.body)
      status = parse.xpath("//QueryStatusCodeValue").text;
      # puts(status)
       #check if request went well
       if status == "200"
        # return zip and lat long if request successful
          lat = parse.xpath("//OutputGeocode//Latitude").text;
          long = parse.xpath("//OutputGeocode/Longitude").text;
          zip = parse.xpath("//ReferenceFeature/Zip").text;
       # puts("lat: " + lat + " long: " + long + " zip: " + zip + "\n")
           infohash = { 'lat' => lat, 'long' => long, 'zip' => zip  }
         end 
         # puts("infohash: " + infohash["zip"]);    
         return infohash
       end
   end

# set the return from the function (which is an array) to an array called usergeo
usergeo = get_geo_and_zip_from_address(incomingstreetaddy,incomingcity,incomingst)

baseUrl = "http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip?zip=" + usergeo["zip"];
puts(baseUrl);
next_link = " ";
next_url = baseUrl;

while next_link
  pagey = ScraperWiki.scrape(next_url)
  fsData = Nokogiri::HTML(pagey)
  whodoc = fsData.xpath("//div[@id='printReady']//tr[@class='RowOdd']")
  $items = whodoc.length
  $i = 0;
  while $i < $items
    ta = whodoc[$i];
    tarr = ta.xpath("td")
    retailergeo = get_geo_and_zip_from_address(URI.escape(tarr[1].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")),URI.escape(tarr[2].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")), URI.escape(tarr[3].text, Regexp.new("[^#{URI::PATTERN::UNRESERVED}]")));
    ScraperWiki.save(['retailer', 'streetaddress', 'city', 'state', 'zipcode', 'restaurant', 'farmmkt', 'lat', 'long'], {'retailer' => tarr[0].text, 'streetaddress' => tarr[1].text, 'city' => tarr[2].text, 'state' => tarr[3].text, 'zipcode' => tarr[4].text, 'restaurant' => tarr[5].text, 'farmmkt' => tarr[6].text, 'lat' => retailergeo["lat"], 'long' => retailergeo["long"]});
    $i +=1;
  end
# This gets you the contents of the href call which is javascript which contains the next page num. Now we need to regexp it
    next_link = fsData.xpath("//a[text()='>>']//@href").text
    txt = next_link
# Regexp code generated using http://txt2re.com/
    re1='.*?'  # Non-greedy match on filler
    re2='(\\d+)'  # Integer Number 1
    re=(re1+re2)
    m=Regexp.new(re,Regexp::IGNORECASE);
    if m.match(txt)
      int1=m.match(txt)[1];
      puts ""<<int1<<""<< "\n";
# code to iterate through scraping each next page....
      next_url = baseUrl + "&startIndex=" + int1;
      puts next_url;
    else
      next_link = false;
    end
end



