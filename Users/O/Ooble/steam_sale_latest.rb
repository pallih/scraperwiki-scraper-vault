# encoding=utf-8

require 'cgi'
require 'date'

CURRENCIES = {
  'uk' => '£',
  'us' => '$',
  'fr' => '€'
}

ORDER = ['uk', 'us', 'fr']

ScraperWiki::attach "steam_sale"

latest = ScraperWiki::select('MAX(date) latest from steam_sale.prices')[0]['latest']

prices = ScraperWiki::select '''game.id, game.name, game.country, price.original_price, price.discounted_price
      from steam_sale.prices price
      join steam_sale.games game on game.id = price.id and game.country = price.country
     where price.date = ? 
       and price.discounted_price <> \'\'
''', latest

games = prices
  .sort_by { |price| price['name'].downcase }
  .group_by { |price| price['id'] }
  .collect { |id, game_prices|
    game = game_prices[0]
    price_values = game_prices.sort_by { |game_price|
      ORDER.index game_price['country']
    }.collect { |game_price| CURRENCIES[game_price['country']] + game_price['discounted_price'].to_s }
    { url: "http://store.steampowered.com/app/#{game['id']}",
      name: CGI.escape_html(game['name']),
      prices: price_values.join('/') }
  }

puts '<html>'
puts '<head>'
puts "<title>Steam Prices on #{latest}</title>"
puts '<style> p { margin: 0; } </style>'
puts '</head>'
puts '<body>'
puts "<h1>Steam Prices on #{latest}</h1>"
games.each { |game|
  puts "<p><a href=\"#{game[:url]}\">#{game[:name]}</a> - #{game[:prices]}</p>"
}
puts '</body>'
puts '</html>'
# encoding=utf-8

require 'cgi'
require 'date'

CURRENCIES = {
  'uk' => '£',
  'us' => '$',
  'fr' => '€'
}

ORDER = ['uk', 'us', 'fr']

ScraperWiki::attach "steam_sale"

latest = ScraperWiki::select('MAX(date) latest from steam_sale.prices')[0]['latest']

prices = ScraperWiki::select '''game.id, game.name, game.country, price.original_price, price.discounted_price
      from steam_sale.prices price
      join steam_sale.games game on game.id = price.id and game.country = price.country
     where price.date = ? 
       and price.discounted_price <> \'\'
''', latest

games = prices
  .sort_by { |price| price['name'].downcase }
  .group_by { |price| price['id'] }
  .collect { |id, game_prices|
    game = game_prices[0]
    price_values = game_prices.sort_by { |game_price|
      ORDER.index game_price['country']
    }.collect { |game_price| CURRENCIES[game_price['country']] + game_price['discounted_price'].to_s }
    { url: "http://store.steampowered.com/app/#{game['id']}",
      name: CGI.escape_html(game['name']),
      prices: price_values.join('/') }
  }

puts '<html>'
puts '<head>'
puts "<title>Steam Prices on #{latest}</title>"
puts '<style> p { margin: 0; } </style>'
puts '</head>'
puts '<body>'
puts "<h1>Steam Prices on #{latest}</h1>"
games.each { |game|
  puts "<p><a href=\"#{game[:url]}\">#{game[:name]}</a> - #{game[:prices]}</p>"
}
puts '</body>'
puts '</html>'
