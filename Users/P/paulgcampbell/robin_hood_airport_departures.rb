require 'nokogiri'           


html = ScraperWiki.scrape("http://www.robinhoodairport.com/flight-information/arrivals.html")           


doc = Nokogiri::HTML(html)

i = 0
for v in doc.search("#topdepartures > div > table > tr")
  cells = v.search('td')

  # A particularly shady way of figuring out the date... Brittle!
  date = Time.now.localtime.strftime("%Y-%m-%d")
  if (i > 5) & (cells[2].inner_html.to_i < 12)
    date = (DateTime.now+ 1).strftime("%Y-%m-%d")
  end

  data = {
    'flight_number' => cells[0].inner_html,
    'destination' => cells[1].inner_html,
    'scheduled_departure_time' => cells[2].inner_html,
    'estimated_departure_time'  => cells[3].inner_html,
    'status' => cells[4].inner_html,
    'date' => date
  }
  ScraperWiki.save_sqlite(unique_keys=['flight_number'], data=data)

i = i +1
end
