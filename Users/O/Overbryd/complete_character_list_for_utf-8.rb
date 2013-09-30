require 'nokogiri'

scraped_queryies = []
next_query = ""

until next_query.nil? || scraped_queryies.include?(next_query) do
  html = ScraperWiki.scrape("http://www.fileformat.info/info/unicode/version/6.0/index.htm#{next_query}")
  data = []
  Nokogiri::HTML(html).css("table.list tr").each do |tr|
    tds = tr.css("td")
    if tds.length == 3
      data << {
        'html_entity'  => tds[0].inner_html,
        'description'  => tds[1].text,
        'encoded_byte' => tds[2].text
      }
    elsif tds.text =~ /More/i
      scraped_queryies << next_query
      next_query = tds.css('a').attr('href').to_s
    else
      next_query = nil
    end
  end
  #                       unique keys                    , key value data
  ScraperWiki.save_sqlite(["html_entity", "encoded_byte"], data)
  puts "Saving page #{scraped_queryies.size}"
end
require 'nokogiri'

scraped_queryies = []
next_query = ""

until next_query.nil? || scraped_queryies.include?(next_query) do
  html = ScraperWiki.scrape("http://www.fileformat.info/info/unicode/version/6.0/index.htm#{next_query}")
  data = []
  Nokogiri::HTML(html).css("table.list tr").each do |tr|
    tds = tr.css("td")
    if tds.length == 3
      data << {
        'html_entity'  => tds[0].inner_html,
        'description'  => tds[1].text,
        'encoded_byte' => tds[2].text
      }
    elsif tds.text =~ /More/i
      scraped_queryies << next_query
      next_query = tds.css('a').attr('href').to_s
    else
      next_query = nil
    end
  end
  #                       unique keys                    , key value data
  ScraperWiki.save_sqlite(["html_entity", "encoded_byte"], data)
  puts "Saving page #{scraped_queryies.size}"
end
