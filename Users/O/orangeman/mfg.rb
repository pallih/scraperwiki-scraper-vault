require "nokogiri"

page = Nokogiri::HTML(ScraperWiki.scrape("http://m.mitfahrgelegenheit.de/searches/search_national?url=searches/search_national&form_type=1&mode=national&page=1&country_from=1&country_to=1&type=b&city_from=30&city_to=134&date=date&day=01&month=08&year=2011&tolerance=0&radius_from=0&radius_to=0&returnride=&limit=10"))


page.search(".list tr")[1..-2].each do |tr|

  details = tr.next.text.match(/(.+?) \| (\d*:\d*)?.*?(\d*)(,|$)/)
  
  if details

    r = tr.search(".city a")

    ride = {
      'orig' => r[0].text,
      'dest' => r[1].text,
      'date' => details[1],
      'time' => details[2],
      'cash' => details[3],
      'url' => tr.search(".icon @href")
    }
    #puts ride.to_json
    ScraperWiki.save_sqlite(unique_keys=['url'], data=ride)
  end
end

require "nokogiri"

page = Nokogiri::HTML(ScraperWiki.scrape("http://m.mitfahrgelegenheit.de/searches/search_national?url=searches/search_national&form_type=1&mode=national&page=1&country_from=1&country_to=1&type=b&city_from=30&city_to=134&date=date&day=01&month=08&year=2011&tolerance=0&radius_from=0&radius_to=0&returnride=&limit=10"))


page.search(".list tr")[1..-2].each do |tr|

  details = tr.next.text.match(/(.+?) \| (\d*:\d*)?.*?(\d*)(,|$)/)
  
  if details

    r = tr.search(".city a")

    ride = {
      'orig' => r[0].text,
      'dest' => r[1].text,
      'date' => details[1],
      'time' => details[2],
      'cash' => details[3],
      'url' => tr.search(".icon @href")
    }
    #puts ride.to_json
    ScraperWiki.save_sqlite(unique_keys=['url'], data=ride)
  end
end

