require 'rss/maker'
require 'date'
require 'cgi'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'

sourcescraper = 'desayunos'
ScraperWiki.httpresponseheader('Content-Type', 'application/rss+xml')
ScraperWiki.attach(sourcescraper)

feed_title = "Radio Universidad de Costa Rica"
show_title = feed_title
where = ""
if ENV.has_key?('QUERY_STRING') && !ENV['QUERY_STRING'].empty? 
  params = CGI::parse( ENV['QUERY_STRING'] )
  if params.has_key?('show')
    show = params['show'][0].to_i
    unless show.nil? or show <= 0
      data = ScraperWiki.select(%Q{title FROM shows WHERE id = #{show}})
      if data.size > 0
        where = %Q{WHERE show_id = #{show}}
        show_title = data.first['title'].strip
        feed_title = show_title + " - " + feed_title
      end
    end
  end
end

data = ScraperWiki.select(%Q{
  published,
  desc,
  title,
  audio
  FROM audio
  #{where}
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
        i.title = show_title + ": " + d['title']
        i.date = DateTime.strptime(d['published'].to_s,'%s').strftime(RFC2822)
        # i.pubDate = i.date
        i.description = d['desc']
        i.enclosure.url = d['audio']
        i.enclosure.type = 'audio/mpeg'
        i.enclosure.length = 0 # d['length'].to_i
    end
end

puts content