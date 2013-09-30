# Blank Ruby
require 'nokogiri'
require 'net/http'
require 'uri'
require 'mechanize'

  # Farmer's markets is type 3, searchType 2 = Restaurants which accept foodstamps
  # searchType 1 = Places which give cash for EBT
  # searchType 4 = Everything (including groceries, restaurants, and farmers markets - if you select this option, you
  # can filter out Restaurants and farmers markets because they are returned fields yes/no
  # First get the farmers markets from the California database
  pagey = ScraperWiki.scrape("http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip?city=San+Francisco&searchType=3&count=50")
  fsData = Nokogiri::HTML(pagey)
  whodoc = fsData.xpath("//div[@id='printReady']//tr[@class='RowOdd']")
  $items = whodoc.length
  $i = 0;
  while $i < $items
    ta = whodoc[$i];
    tarr = ta.xpath("td")
    ScraperWiki.save(['retailer', 'streetaddress', 'city', 'state', 'zipcode'], {'retailer' => tarr[0].text, 'streetaddress' => tarr[1].text, 'city' => tarr[2].text, 'state' => tarr[3].text, 'zipcode' => tarr[4].text});
    $i +=1;
  end
  # Now get the San Fran farmer's markets from the USDA database. The USDA page is more intricate, lets use Mechanize
  agent = Mechanize.new{|a| a.log = Logger.new(STDERR) }
  agent.get("http://search.ams.usda.gov/farmersmarkets/Accessible.aspx")
  form = agent.page.forms.first
  detailsearch = form.buttons[0]
  form.texts[0].value = "94114" # This is the heart of San-Fran somewhere in Noe Valley. Thus a radius search of 10 miles should be 
  form.fields[9].option_with(:text => '10').tick #This is the milage selector - option 1 (2nd option) is 10 miles
  #form.fields[10].option_with(:text => 'California').tick
  form.checkbox_with(:value => 'SNAP').checked = true # checks off the checkbox to find Farmers markets accepting SNAP
  form.hiddens[0].value='SNAP' # make sure the checkbox filter is set so that it is run
  # This checkbox filter usually is set when you click on a checkbox, but mechanize does not seem to offer a click
  # option for checkbox elements, so I had to hack this a bit and see the javascript code that is usually activated
  # when the checkbox is clicked. Anyways, so the JS code will set this checkbox filter value when a checkbox is clicked
  listings = form.click_button(detailsearch) # should submit the form using the detail search butto
  divtabs = listings.search('//*[(@id = "ctl00_CenterContent_htmlOut")]') # Get the table with the results
  labels = divtabs.search('font') #labels for each listing
  tables = divtabs.search('table') # each detailed listing has two tables
# now iterate through
  tds = tables[0].search('td')
tables[0].search('td').text

  address = tds[3].text
    


  
  



# Blank Ruby
require 'nokogiri'
require 'net/http'
require 'uri'
require 'mechanize'

  # Farmer's markets is type 3, searchType 2 = Restaurants which accept foodstamps
  # searchType 1 = Places which give cash for EBT
  # searchType 4 = Everything (including groceries, restaurants, and farmers markets - if you select this option, you
  # can filter out Restaurants and farmers markets because they are returned fields yes/no
  # First get the farmers markets from the California database
  pagey = ScraperWiki.scrape("http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip?city=San+Francisco&searchType=3&count=50")
  fsData = Nokogiri::HTML(pagey)
  whodoc = fsData.xpath("//div[@id='printReady']//tr[@class='RowOdd']")
  $items = whodoc.length
  $i = 0;
  while $i < $items
    ta = whodoc[$i];
    tarr = ta.xpath("td")
    ScraperWiki.save(['retailer', 'streetaddress', 'city', 'state', 'zipcode'], {'retailer' => tarr[0].text, 'streetaddress' => tarr[1].text, 'city' => tarr[2].text, 'state' => tarr[3].text, 'zipcode' => tarr[4].text});
    $i +=1;
  end
  # Now get the San Fran farmer's markets from the USDA database. The USDA page is more intricate, lets use Mechanize
  agent = Mechanize.new{|a| a.log = Logger.new(STDERR) }
  agent.get("http://search.ams.usda.gov/farmersmarkets/Accessible.aspx")
  form = agent.page.forms.first
  detailsearch = form.buttons[0]
  form.texts[0].value = "94114" # This is the heart of San-Fran somewhere in Noe Valley. Thus a radius search of 10 miles should be 
  form.fields[9].option_with(:text => '10').tick #This is the milage selector - option 1 (2nd option) is 10 miles
  #form.fields[10].option_with(:text => 'California').tick
  form.checkbox_with(:value => 'SNAP').checked = true # checks off the checkbox to find Farmers markets accepting SNAP
  form.hiddens[0].value='SNAP' # make sure the checkbox filter is set so that it is run
  # This checkbox filter usually is set when you click on a checkbox, but mechanize does not seem to offer a click
  # option for checkbox elements, so I had to hack this a bit and see the javascript code that is usually activated
  # when the checkbox is clicked. Anyways, so the JS code will set this checkbox filter value when a checkbox is clicked
  listings = form.click_button(detailsearch) # should submit the form using the detail search butto
  divtabs = listings.search('//*[(@id = "ctl00_CenterContent_htmlOut")]') # Get the table with the results
  labels = divtabs.search('font') #labels for each listing
  tables = divtabs.search('table') # each detailed listing has two tables
# now iterate through
  tds = tables[0].search('td')
tables[0].search('td').text

  address = tds[3].text
    


  
  



