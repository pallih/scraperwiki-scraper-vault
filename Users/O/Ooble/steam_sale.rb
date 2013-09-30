# encoding=utf-8

require 'date'
require 'nokogiri'
require 'typhoeus'

$start = Time.now.to_date

COUNTRIES = ['uk', 'us', 'fr']
REMOVE = /[\uFFFD®™]/
CURRENCIES = /[$£€]/

PRICE_REGEX = /[^0-9.,][0-9.,]+|[0-9.,]+[^0-9.,]/

def games_and_prices_from response, country
  document = Nokogiri::HTML response.body.encode('utf-8', 'utf-8', :invalid => :replace)

  document.css('.search_result_row').collect { |row|
    id = /^http:\/\/[^\/]+\/app\/(\d+)/.match(row['href'])[1].to_i
    name = row.at_css('.search_name h4').text.gsub(REMOVE, '')
    release_date_text = row.at_css('.search_released').text.strip
    release_date = Date.parse(row.at_css('.search_released').text.strip) rescue nil
    prices = row.at_css('.search_price').text
    original_price, discounted_price = (/(#{PRICE_REGEX}) *(#{PRICE_REGEX})/.match(prices) || /(#{PRICE_REGEX})/.match(prices) || //.match('')).captures.collect { |price| price.strip.gsub(CURRENCIES, '').sub(',', '.').to_f }
    original_price ||= 0
    {
      id: id,
      country: country,
      name: name,
      release_date: release_date,
      original_price: original_price,
      discounted_price: discounted_price
    }
  }
end

requests = COUNTRIES.flat_map do |country|
  html = Typhoeus::Request.get("http://store.steampowered.com/search/?cc=#{country}&category1=998").body
  html.encode! 'utf-8', 'utf-8', :invalid => :replace
  document = Nokogiri::HTML html
  page_count = document.css('.search_pagination_right a').map(&:text).map(&:to_i).max
  puts "#{country} has #{page_count} pages."

  (1..page_count).collect { |page|
    request = Typhoeus::Request.new "http://store.steampowered.com/search/?cc=#{country}&category1=998&page=#{page}"
    request.on_complete do |response|
      games_and_prices_from response, country
    end
    request
  }
end

hydra = Typhoeus::Hydra.new max_concurrency: 5
requests.each do |request|
  hydra.queue request
end
hydra.run

responses = requests.flat_map(&:handled_response)
games = responses.collect { |response|
  {
    id: response[:id],
    country: response[:country],
    name: response[:name],
    release_date: response[:release_date]
  }
}
prices = responses.collect { |response|
    {
      id: response[:id],
      country: response[:country],
      date: $start,
      original_price: response[:original_price],
      discounted_price: response[:discounted_price]
    }
}

ScraperWiki::save_sqlite [:id, :country], games, 'games'
ScraperWiki::save_sqlite [:id, :country, :date], prices, 'prices'
# encoding=utf-8

require 'date'
require 'nokogiri'
require 'typhoeus'

$start = Time.now.to_date

COUNTRIES = ['uk', 'us', 'fr']
REMOVE = /[\uFFFD®™]/
CURRENCIES = /[$£€]/

PRICE_REGEX = /[^0-9.,][0-9.,]+|[0-9.,]+[^0-9.,]/

def games_and_prices_from response, country
  document = Nokogiri::HTML response.body.encode('utf-8', 'utf-8', :invalid => :replace)

  document.css('.search_result_row').collect { |row|
    id = /^http:\/\/[^\/]+\/app\/(\d+)/.match(row['href'])[1].to_i
    name = row.at_css('.search_name h4').text.gsub(REMOVE, '')
    release_date_text = row.at_css('.search_released').text.strip
    release_date = Date.parse(row.at_css('.search_released').text.strip) rescue nil
    prices = row.at_css('.search_price').text
    original_price, discounted_price = (/(#{PRICE_REGEX}) *(#{PRICE_REGEX})/.match(prices) || /(#{PRICE_REGEX})/.match(prices) || //.match('')).captures.collect { |price| price.strip.gsub(CURRENCIES, '').sub(',', '.').to_f }
    original_price ||= 0
    {
      id: id,
      country: country,
      name: name,
      release_date: release_date,
      original_price: original_price,
      discounted_price: discounted_price
    }
  }
end

requests = COUNTRIES.flat_map do |country|
  html = Typhoeus::Request.get("http://store.steampowered.com/search/?cc=#{country}&category1=998").body
  html.encode! 'utf-8', 'utf-8', :invalid => :replace
  document = Nokogiri::HTML html
  page_count = document.css('.search_pagination_right a').map(&:text).map(&:to_i).max
  puts "#{country} has #{page_count} pages."

  (1..page_count).collect { |page|
    request = Typhoeus::Request.new "http://store.steampowered.com/search/?cc=#{country}&category1=998&page=#{page}"
    request.on_complete do |response|
      games_and_prices_from response, country
    end
    request
  }
end

hydra = Typhoeus::Hydra.new max_concurrency: 5
requests.each do |request|
  hydra.queue request
end
hydra.run

responses = requests.flat_map(&:handled_response)
games = responses.collect { |response|
  {
    id: response[:id],
    country: response[:country],
    name: response[:name],
    release_date: response[:release_date]
  }
}
prices = responses.collect { |response|
    {
      id: response[:id],
      country: response[:country],
      date: $start,
      original_price: response[:original_price],
      discounted_price: response[:discounted_price]
    }
}

ScraperWiki::save_sqlite [:id, :country], games, 'games'
ScraperWiki::save_sqlite [:id, :country, :date], prices, 'prices'
