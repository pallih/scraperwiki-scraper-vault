# Ruby scraper for consultations from the Ministry of Defence
require 'nokogiri'
require 'uri'
require 'mechanize'

DEPARTMENT = "Ministry of Defence"
Mechanize.html_parser = Nokogiri::HTML

def scrape_page(url)
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
    browser.user_agent_alias = 'Linux Firefox'
  }

  consult_page = br.get(url)
  consult_doc = Nokogiri::HTML(consult_page.body, nil, 'utf-8')

  record['title'] = consult_doc.css('meta[name="DC.title"]')[0]['content']

  record['published_date'] = Date.parse(consult_doc.css('meta[name="UKMOD.date.valid.start"]')[0]['content']).to_s
  unless consult_doc.css('meta[name="DC.issued"]').empty? 
    record['start_date'] = Date.parse(consult_doc.css('meta[name="DC.issued"]')[0]['content']).to_s
  else
    puts "No start date present"
  end
  record['end_date'] = Date.parse(consult_doc.css('meta[name="DC.valid"]')[0]['content']).to_s
  record['sponsor'] = ''
  record['description'] = consult_doc.css('div[property="dc:abstract"]').inner_html.strip

  # Find any linked documents
  parsed_consult_url = URI.parse(record['URI'])
  consult_documents = []
  consult_doc.css('a[rel="DC:haspart"]').each do |link|
    d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
    d['title'] = link.inner_text
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

