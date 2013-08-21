require 'mechanize'

BASE_URL = 'http://www.flyscoot.com/index.php/en/'

starting_url = BASE_URL
@br = Mechanize.new do |browser|
  browser.user_agent_alias = 'Linux Firefox'
end
page = @br.get(starting_url)
form = page.forms[1]

form.fields[2].value = 'SYD'
form.fields[3].value = 'SIN'
form.fields[4].value = '12/22/2012'
form.fields[5].value = 'SIN'
form.fields[6].value = 'SYD'
form.fields[7].value = '1/6/2013'

page = form.submit()

scraped = Time.now

page.parser.xpath("//ul[@class='day_cell']/li").each do |flight|

  data = {

    'scrapedate' => scraped,
    'flightdate' => Date.new(flight.xpath("@year").text.to_i, flight.xpath("@month").text.to_i, flight.xpath("@day").text.to_i),
    'flightprice' => flight.xpath("div/strong/span").text.to_i

  }

  if data['flightdate'] >= Date.new(2012,12,21) and data['flightdate'] <= Date.new(2013,1,5)

    ScraperWiki.save_sqlite(unique_keys=["scrapedate","flightdate"], data=data)

  end 

end

