require 'nokogiri'

page = 1
finished = false

while !finished do
  url = "http://www.number10.gov.uk/news/speeches-and-transcripts/page/#{page}"
  puts "scraping index page: #{page}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  
  doc.search('.posts_list_post/a').each do |a|
    title = a.inner_text.strip
    permalink = a['href'].to_s

    puts "scraping: #{title}"

    record = {'title' => title, 'permalink' => permalink, 'minister_name' => "David Cameron"}

    speech_or_transcript_html = ScraperWiki.scrape(permalink)
    speech_or_transcript_doc = Nokogiri::HTML(speech_or_transcript_html)

    record['given_on'] = speech_or_transcript_doc.at('.timestamp').inner_text

    record['body'] = speech_or_transcript_doc.at('.entry').inner_html

    record['department'] = "Prime Minister's Office"

    ScraperWiki.save(['permalink'], record)
  end

  finished = true
  doc.search('a').each do |a|
    has_previous_entries = a.inner_text[/Previous Entries/]
    finished = false if has_previous_entries
  end
  page = page + 1
end
