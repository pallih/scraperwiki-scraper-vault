# Ruby scraper for consultations from the Department of Health
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department of Health"

def scrape_page(url)
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  consult_html = ScraperWiki.scrape(url)
  consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

  record['title'] = consult_doc.css('meta[name="DC.title"]')[0]['content']

  record['published_date'] = Date.parse(consult_doc.css('span[property="dc:available"]')[0]['content']).to_s
  unless consult_doc.css('span[property="dc:issued"]').empty? 
    record['start_date'] = Date.parse(consult_doc.css('span[property="dc:issued"]')[0]['content']).to_s
  else
    puts "No start date present"
  end
  record['end_date'] = Date.parse(consult_doc.css('span[property="dc:valid"]')[0]['content']).to_s
  record['sponsor'] = ''
  record['description'] = consult_doc.css('span[property="dc:abstract"]')[0]['content'].strip

  # Find any linked documents
  parsed_consult_url = URI.parse(record['URI'])
  consult_documents = []
  consult_doc.css('ul.linksCollection a').each do |link|
    d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
    if link.inner_text.match(/^Download:/i)
      # The link starts with the text "Download:...", so strip it off
      d['title'] = link.inner_text.match(/^Download:(.*)/i)[1].strip
    elsif link.inner_text.match(/^Download/i)
      # The link starts with the text "Download:...", so strip it off
      d['title'] = link.inner_text.match(/^Download(.*)/i)[1].strip
    else
      d['title'] = link.inner_text
    end
    consult_documents.push(d)
  end

  puts consult_documents.size.to_s+" documents: "+consult_documents.collect { |d| d['title'] }.join("; ")

  ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  consult_documents.each do |d|
    ScraperWiki.save_sqlite(['URI'], d, 'documents')
  end
end


# The list of consultations is in a separate scraper, so we can just run through the results for that
# looking for ones relevant to this department
record_count = 0
ScraperWiki.getData('directgov_consultations').each do |consultation|
  if consultation['department'] == DEPARTMENT
    record_count = record_count + 1
    puts "Record #{record_count} "+consultation['permalink']
    scrape_page(consultation['permalink'])
  end
end

