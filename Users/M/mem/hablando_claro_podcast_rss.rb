# Blank Ruby
require 'date'
require 'rss/maker'

sourcescraper = 'hablando_claro_--_podcast'
ScraperWiki.httpresponseheader('Content-Type','application/rss+xml')
ScraperWiki.attach(sourcescraper)
data = ScraperWiki.select(%q{
  info.date as date,
  info.summary as summary,
  info.link as link,
  info.published as published,
  info.title as title,
  audio.link as audio,
  audio.length as length
  FROM `info`
    JOIN `audio` ON info.date == audio.date
  ORDER BY date DESC LIMIT 10
})



content = RSS::Maker.make('2.0') do |m|
    m.channel.title = "Hablando Claro"
    m.channel.link = "http://www.hablandoclarocr.com/"
    m.channel.description = "Hablando Claro"
    m.items.do_sort = true

    data.each do |d|
        i = m.items.new_item
        i.link = d['link']
        i.guid.content = i.link
        i.guid.isPermaLink = true
        i.title = d['title']
        i.date = d['published']
        #i.date = DateTime.strptime(d['date'],'%s').strftime("%a, %d %b %Y %T %z")
        i.pubDate = i.date
        i.description = d['summary']
        i.enclosure.url = d['audio']
        i.enclosure.type = 'audio/mpeg'
        i.enclosure.length = d['length'].to_i
    end
end

puts content# Blank Ruby
require 'date'
require 'rss/maker'

sourcescraper = 'hablando_claro_--_podcast'
ScraperWiki.httpresponseheader('Content-Type','application/rss+xml')
ScraperWiki.attach(sourcescraper)
data = ScraperWiki.select(%q{
  info.date as date,
  info.summary as summary,
  info.link as link,
  info.published as published,
  info.title as title,
  audio.link as audio,
  audio.length as length
  FROM `info`
    JOIN `audio` ON info.date == audio.date
  ORDER BY date DESC LIMIT 10
})



content = RSS::Maker.make('2.0') do |m|
    m.channel.title = "Hablando Claro"
    m.channel.link = "http://www.hablandoclarocr.com/"
    m.channel.description = "Hablando Claro"
    m.items.do_sort = true

    data.each do |d|
        i = m.items.new_item
        i.link = d['link']
        i.guid.content = i.link
        i.guid.isPermaLink = true
        i.title = d['title']
        i.date = d['published']
        #i.date = DateTime.strptime(d['date'],'%s').strftime("%a, %d %b %Y %T %z")
        i.pubDate = i.date
        i.description = d['summary']
        i.enclosure.url = d['audio']
        i.enclosure.type = 'audio/mpeg'
        i.enclosure.length = d['length'].to_i
    end
end

puts content