require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://kakaku.com/kuruma/'

agent = Mechanize.new
page1 = agent.get(url)
page1.links_with(:href => /^\/kuruma\/km_[^\/]+\/$/)[0..3].each {|link1|
  regEx2 = link1.href.to_s
  page2 = agent.get(link1.uri)
  page2.links_with(:href => /^#{regEx2}[^\/k]{11}\/$/)[0..3].each {|link2|
    regEx3  = link2.href.to_s
    page3 = agent.get(link2.uri)
    page3.links_with(:href => /^#{regEx3}grade\/[^\/]+\/$/)[0..3].each {|link3|
      hash = {
        'href' => link2.href.to_s,
        'name' => link1.text.to_s + ' ' + link2.text.to_s + ' ' + link3.text.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=['href'], data=hash)

    }

  }
}

require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://kakaku.com/kuruma/'

agent = Mechanize.new
page1 = agent.get(url)
page1.links_with(:href => /^\/kuruma\/km_[^\/]+\/$/)[0..3].each {|link1|
  regEx2 = link1.href.to_s
  page2 = agent.get(link1.uri)
  page2.links_with(:href => /^#{regEx2}[^\/k]{11}\/$/)[0..3].each {|link2|
    regEx3  = link2.href.to_s
    page3 = agent.get(link2.uri)
    page3.links_with(:href => /^#{regEx3}grade\/[^\/]+\/$/)[0..3].each {|link3|
      hash = {
        'href' => link2.href.to_s,
        'name' => link1.text.to_s + ' ' + link2.text.to_s + ' ' + link3.text.to_s
      }
      ScraperWiki.save_sqlite(unique_keys=['href'], data=hash)

    }

  }
}

