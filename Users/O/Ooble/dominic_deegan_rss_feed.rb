require 'rss/maker'

ScraperWiki::httpresponseheader('Content-Type', 'application/xml')

ScraperWiki::attach('dominic_deegan')
comics = ScraperWiki::select '* FROM dominic_deegan.comics ORDER BY date DESC, position DESC LIMIT 10'
news = ScraperWiki::select '* FROM dominic_deegan.news ORDER BY date DESC LIMIT 10'
entries = (comics + news).map! { |entry|
  entry['date'] = Date.strptime entry['date'], '%Y-%m-%d'
  entry
}.sort_by { |entry|
  position = entry['position'] || 100
  [entry['date'], position]
}.reverse.slice(0...10)

puts RSS::Maker.make('2.0') { |feed|
  feed.channel.title = 'Dominic Deegan'
  feed.channel.description = 'Dominic Deegan: Oracle for Hire'
  feed.channel.link = 'http://dominic-deegan.com/'
  
  entries.each do |entry|
    date = entry['date']
    description = entry['image'] ? "<img src=\"http://dominic-deegan.com/#{entry['image']}\" alt=\"\"/>" : entry['content']
    feed.items.new_item do |item|
      item.title = date.strftime '%A, %B %e, %Y'
      item.link = "http://dominic-deegan.com/view.php?date=#{date.strftime '%Y-%m-%d'}"
      item.date = date.to_time
      item.description = description
    end
  end
}
require 'rss/maker'

ScraperWiki::httpresponseheader('Content-Type', 'application/xml')

ScraperWiki::attach('dominic_deegan')
comics = ScraperWiki::select '* FROM dominic_deegan.comics ORDER BY date DESC, position DESC LIMIT 10'
news = ScraperWiki::select '* FROM dominic_deegan.news ORDER BY date DESC LIMIT 10'
entries = (comics + news).map! { |entry|
  entry['date'] = Date.strptime entry['date'], '%Y-%m-%d'
  entry
}.sort_by { |entry|
  position = entry['position'] || 100
  [entry['date'], position]
}.reverse.slice(0...10)

puts RSS::Maker.make('2.0') { |feed|
  feed.channel.title = 'Dominic Deegan'
  feed.channel.description = 'Dominic Deegan: Oracle for Hire'
  feed.channel.link = 'http://dominic-deegan.com/'
  
  entries.each do |entry|
    date = entry['date']
    description = entry['image'] ? "<img src=\"http://dominic-deegan.com/#{entry['image']}\" alt=\"\"/>" : entry['content']
    feed.items.new_item do |item|
      item.title = date.strftime '%A, %B %e, %Y'
      item.link = "http://dominic-deegan.com/view.php?date=#{date.strftime '%Y-%m-%d'}"
      item.date = date.to_time
      item.description = description
    end
  end
}
