require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML( open( "http://www.sbb.ch/en/station-services/am-bahnhof/railway-stations.html" ) )

doc.search('.teaserrow li').each do |li|
  li.search('h2 a').each do |a|
    data = {
      'href' => a.attribute('href').to_s,
      'title' => a.search('.bd strong')[0].content
    }

    ScraperWiki.save_sqlite(unique_keys=["href"], data)
  end
end

doc.search('.parbase.table a').each do |a|
  data = {
    'href' => a.attribute('href').to_s,
    'title' => a.content
  }

  ScraperWiki.save_sqlite(unique_keys=["href"], data)
endrequire 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML( open( "http://www.sbb.ch/en/station-services/am-bahnhof/railway-stations.html" ) )

doc.search('.teaserrow li').each do |li|
  li.search('h2 a').each do |a|
    data = {
      'href' => a.attribute('href').to_s,
      'title' => a.search('.bd strong')[0].content
    }

    ScraperWiki.save_sqlite(unique_keys=["href"], data)
  end
end

doc.search('.parbase.table a').each do |a|
  data = {
    'href' => a.attribute('href').to_s,
    'title' => a.content
  }

  ScraperWiki.save_sqlite(unique_keys=["href"], data)
end