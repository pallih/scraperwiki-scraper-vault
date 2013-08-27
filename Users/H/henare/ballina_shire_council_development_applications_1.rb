require 'rss'

url = "http://da.ballina.nsw.gov.au/\
Pages/XC.Track/SearchApplication.aspx?o=rss&d=last14days&t=10,18"

feed = RSS::Parser.parse(url, false)

feed.channel.items.each do |item|
  record = {
    :council_reference => item.title.split[0],
    :address           => item.description.split('.')[0].strip,
    :description       => item.description.split('.')[1].strip,
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_received     => item.pubDate.strftime('%Y-%m-%d'),
    :date_scraped      => Time.now.strftime('%Y-%m-%d')
  }

  ScraperWiki.save_sqlite([:council_reference], record)
endrequire 'rss'

url = "http://da.ballina.nsw.gov.au/\
Pages/XC.Track/SearchApplication.aspx?o=rss&d=last14days&t=10,18"

feed = RSS::Parser.parse(url, false)

feed.channel.items.each do |item|
  record = {
    :council_reference => item.title.split[0],
    :address           => item.description.split('.')[0].strip,
    :description       => item.description.split('.')[1].strip,
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_received     => item.pubDate.strftime('%Y-%m-%d'),
    :date_scraped      => Time.now.strftime('%Y-%m-%d')
  }

  ScraperWiki.save_sqlite([:council_reference], record)
endrequire 'rss'

url = "http://da.ballina.nsw.gov.au/\
Pages/XC.Track/SearchApplication.aspx?o=rss&d=last14days&t=10,18"

feed = RSS::Parser.parse(url, false)

feed.channel.items.each do |item|
  record = {
    :council_reference => item.title.split[0],
    :address           => item.description.split('.')[0].strip,
    :description       => item.description.split('.')[1].strip,
    :info_url          => item.link,
    :comment_url       => item.link,
    :date_received     => item.pubDate.strftime('%Y-%m-%d'),
    :date_scraped      => Time.now.strftime('%Y-%m-%d')
  }

  ScraperWiki.save_sqlite([:council_reference], record)
end