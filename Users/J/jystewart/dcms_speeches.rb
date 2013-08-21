# Blank Ruby
require 'nokogiri'
require 'uri'
#ScraperWiki.sqlitecommand("execute", "drop table swdata")

# retrieve the index page
base_url = "http://www.communities.gov.uk/corporate/newsroom/speechesstatements/"
starting_url = base_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
paging_info = doc.at('.pagingWrapper>p').text
matched_pages = paging_info.match(/Page (\d+) of (\d+) /)
start_page = matched_pages[1].to_i
end_page = matched_pages[2].to_i
# start_page = end_page = 1 # no idea why this was ever here?

(start_page..end_page).each do |page|

  if page > 1
    starting_url = base_url + "?viewPrevious=true&currentPageNumber=#{page}"
    html = ScraperWiki.scrape(starting_url)
    doc = Nokogiri::HTML(html)
  end

  doc.search('.searchResultList h4').each do |h4|
    record = {'title' => h4.inner_text.strip, 'permalink' => parsed_base_url.merge(h4.at('a')['href']).to_s}
    puts "Looking at #{record['title']}"
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)
   
    # http://www.communities.gov.uk/statements/corporate/londonroyaldocks has no minister h3, so move on
    minister_name_node = the_speech_doc.at('.ministerIntro h3') or next

    # TODO: There are some issues with names losing spaces, so need to replace
    # [a-z][A-Z] with [a-z] [A-Z]
    record['minister_name'] = minister_name_node.text.strip #gsub(/\302\240/, ' ').strip
    record['given_on'] = the_speech_doc.at('#Page>table tr td').text.strip
    record['where'] = the_speech_doc.search('#Page>table tr td').last.text.strip
    record['body'] = the_speech_doc.xpath('//div[@id="Page"]/hr/following-sibling::*').
        collect(&:to_s).join('').gsub(/\302\240/, ' ').strip

    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end

  end

end
