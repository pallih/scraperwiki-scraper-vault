require "open-uri"
require "json"

url ="http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=bbc_seasonal_foods&query=select%20*%20from%20%60swdata%60%20limit%20100"

foods = JSON.parse(open(url).read)

MONTH_KEYS = %w(jan feb mar apr may jun jul aug sep oct nov dec)

months = MONTH_KEYS.inject({}) do |h, m|
  h[m] = {now_in_season: [], last_chance: [], now_out_of_season: []}
  h
end

foods.each do |food|
  details = food["name"]
  months[food["comes_into_season"]][:now_in_season] << details if food["comes_into_season"]
  months[food["last_month_in_season"]][:last_chance] << details if food["last_month_in_season"]
  months[food["out_of_season"]][:now_out_of_season] << details if food["out_of_season"]
end

data = MONTH_KEYS.inject([]) { |a, m| a << months[m].merge(name: m) }

ScraperWiki::save_sqlite(['name'], data)require "open-uri"
require "json"

url ="http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=bbc_seasonal_foods&query=select%20*%20from%20%60swdata%60%20limit%20100"

foods = JSON.parse(open(url).read)

MONTH_KEYS = %w(jan feb mar apr may jun jul aug sep oct nov dec)

months = MONTH_KEYS.inject({}) do |h, m|
  h[m] = {now_in_season: [], last_chance: [], now_out_of_season: []}
  h
end

foods.each do |food|
  details = food["name"]
  months[food["comes_into_season"]][:now_in_season] << details if food["comes_into_season"]
  months[food["last_month_in_season"]][:last_chance] << details if food["last_month_in_season"]
  months[food["out_of_season"]][:now_out_of_season] << details if food["out_of_season"]
end

data = MONTH_KEYS.inject([]) { |a, m| a << months[m].merge(name: m) }

ScraperWiki::save_sqlite(['name'], data)