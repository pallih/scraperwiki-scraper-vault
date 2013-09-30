# Scrapes the wort.lu website for the orbituaries

require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

@engine= Mechanize.new { |m|
  m.user_agent_alias = 'Linux Firefox'
}

# CONSTANTS
URL = "http://www.wort.lu/de/service/announcement/obituary"
XPATH = './/div[@id="serviceBody"]/ul[5]/li'
DATE = Date.today

@engine.get(URL) do |page|
  id = 1
  page.search(XPATH).collect do |entry|
    puts "#{DATE}-#{id}"
    
    header = entry.xpath('h2')
    content = entry.xpath('div[@class="content"]/p')
    fulltext = entry
    puts header[0].content
    puts content[0].content

    ScraperWiki.save_sqlite(unique_keys=["orbid"], data={"orbid" => "#{DATE}-#{id}", "name" => header[0].content, "text" => content[0].content, "fulltext" => fulltext.content}, table_name="orbituaries")

    id += 1
  end
end# Scrapes the wort.lu website for the orbituaries

require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

@engine= Mechanize.new { |m|
  m.user_agent_alias = 'Linux Firefox'
}

# CONSTANTS
URL = "http://www.wort.lu/de/service/announcement/obituary"
XPATH = './/div[@id="serviceBody"]/ul[5]/li'
DATE = Date.today

@engine.get(URL) do |page|
  id = 1
  page.search(XPATH).collect do |entry|
    puts "#{DATE}-#{id}"
    
    header = entry.xpath('h2')
    content = entry.xpath('div[@class="content"]/p')
    fulltext = entry
    puts header[0].content
    puts content[0].content

    ScraperWiki.save_sqlite(unique_keys=["orbid"], data={"orbid" => "#{DATE}-#{id}", "name" => header[0].content, "text" => content[0].content, "fulltext" => fulltext.content}, table_name="orbituaries")

    id += 1
  end
end