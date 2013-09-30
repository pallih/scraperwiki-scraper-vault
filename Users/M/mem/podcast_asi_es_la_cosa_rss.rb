require 'rss/maker'
require 'date'
require 'cgi'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'

sourcescraper = 'podcast_asi_es_la_cosa'
ScraperWiki.httpresponseheader('Content-Type', 'application/rss+xml')
ScraperWiki.attach(sourcescraper)

feed_title = "Asi es la cosa"

data = ScraperWiki.select(%Q{
  published,
  description,
  title,
  audio,
  length
  FROM audio
  ORDER BY published DESC LIMIT 10
})

content = RSS::Maker.make('2.0') do |m|
    m.channel.title = feed_title
    m.channel.link = "http://radiosucr.com/radiouniversidad/"
    m.channel.description = feed_title
    m.items.do_sort = true

    data.each do |d|
        i = m.items.new_item
        i.link = d['audio']
        i.guid.content = i.link
        i.guid.isPermaLink = true
        i.title = d['title']
        i.date = DateTime.strptime(d['published'].to_s,'%s').strftime(RFC2822)
        i.pubDate = i.date
        i.description = d['description']
        i.enclosure.url = d['audio']
        i.enclosure.type = 'audio/mpeg'
        i.enclosure.length = d['length'].to_i
    end
end

puts contentrequire 'rss/maker'
require 'date'
require 'cgi'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'

sourcescraper = 'podcast_asi_es_la_cosa'
ScraperWiki.httpresponseheader('Content-Type', 'application/rss+xml')
ScraperWiki.attach(sourcescraper)

feed_title = "Asi es la cosa"

data = ScraperWiki.select(%Q{
  published,
  description,
  title,
  audio,
  length
  FROM audio
  ORDER BY published DESC LIMIT 10
})

content = RSS::Maker.make('2.0') do |m|
    m.channel.title = feed_title
    m.channel.link = "http://radiosucr.com/radiouniversidad/"
    m.channel.description = feed_title
    m.items.do_sort = true

    data.each do |d|
        i = m.items.new_item
        i.link = d['audio']
        i.guid.content = i.link
        i.guid.isPermaLink = true
        i.title = d['title']
        i.date = DateTime.strptime(d['published'].to_s,'%s').strftime(RFC2822)
        i.pubDate = i.date
        i.description = d['description']
        i.enclosure.url = d['audio']
        i.enclosure.type = 'audio/mpeg'
        i.enclosure.length = d['length'].to_i
    end
end

puts content