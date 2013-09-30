# Ruby scraper for DECC.gov.uk speeches
require 'nokogiri'
require 'uri'

# retrieve the index page
base_url = "http://www.decc.gov.uk/en/content/news/categories/huhne_speech/huhne_speech.aspx"
starting_url = base_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

# Find the links to the pages of results
pages = []
paging_info = doc.css('.pagelinks>a').each do |pagelink|
  if pagelink['class'][0..9] == 'paginglink'
    # This is one of the links we're interested in (i.e. not a prev/next link)
    pages.push(pagelink['href'])
  end
end

pages.each do |page_url|

  starting_url = parsed_base_url.merge(page_url).to_s
  html = ScraperWiki.scrape(starting_url)
  doc = Nokogiri::HTML(html)

  doc.css('ol.search-results li').each do |li|
    record = {'title' => li.at('strong').inner_text.strip, 'permalink' => parsed_base_url.merge(li.at('a')['href']).to_s,
              'given_on' => li.css('span')[1].inner_text, 'minister_name' => 'Rt Hon Chris Huhne', 
              'department' => 'Department for Energy and Climate Change'}
    puts "Looking at #{record['title']}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

    #record['where'] = the_speech_doc.search('#Page>table tr td').last.text.strip
    if !the_speech_doc.css('.cms-text').empty? 
      # Sometimes, but not always, there'll be more than one "<div class='cms-text'>" element, and we'll just want the last one
      record['body'] = the_speech_doc.css('.cms-text').last.css('p').collect { |para| para.inner_html }.join("\n\n") 
    elsif !the_speech_doc.css('.cms-textandimage').empty? 
      record['body'] = the_speech_doc.css('.cms-textandimage').last.css('p').collect { |para| para.inner_html }.join("\n\n")
    else
      puts "FAILED TO FIND THE SPEECH"
    end
    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end

  end

end
# Ruby scraper for DECC.gov.uk speeches
require 'nokogiri'
require 'uri'

# retrieve the index page
base_url = "http://www.decc.gov.uk/en/content/news/categories/huhne_speech/huhne_speech.aspx"
starting_url = base_url
parsed_base_url = URI.parse(starting_url)
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

# Find the links to the pages of results
pages = []
paging_info = doc.css('.pagelinks>a').each do |pagelink|
  if pagelink['class'][0..9] == 'paginglink'
    # This is one of the links we're interested in (i.e. not a prev/next link)
    pages.push(pagelink['href'])
  end
end

pages.each do |page_url|

  starting_url = parsed_base_url.merge(page_url).to_s
  html = ScraperWiki.scrape(starting_url)
  doc = Nokogiri::HTML(html)

  doc.css('ol.search-results li').each do |li|
    record = {'title' => li.at('strong').inner_text.strip, 'permalink' => parsed_base_url.merge(li.at('a')['href']).to_s,
              'given_on' => li.css('span')[1].inner_text, 'minister_name' => 'Rt Hon Chris Huhne', 
              'department' => 'Department for Energy and Climate Change'}
    puts "Looking at #{record['title']}"
    puts "=> "+record['permalink']
    the_actual_speech_html = ScraperWiki.scrape(record['permalink'])
    the_speech_doc = Nokogiri::HTML(the_actual_speech_html)

    #record['where'] = the_speech_doc.search('#Page>table tr td').last.text.strip
    if !the_speech_doc.css('.cms-text').empty? 
      # Sometimes, but not always, there'll be more than one "<div class='cms-text'>" element, and we'll just want the last one
      record['body'] = the_speech_doc.css('.cms-text').last.css('p').collect { |para| para.inner_html }.join("\n\n") 
    elsif !the_speech_doc.css('.cms-textandimage').empty? 
      record['body'] = the_speech_doc.css('.cms-textandimage').last.css('p').collect { |para| para.inner_html }.join("\n\n")
    else
      puts "FAILED TO FIND THE SPEECH"
    end
    begin
      ScraperWiki.save(['permalink'], record)
    rescue => e
      puts e.message
      puts record.inspect
    end

  end

end
