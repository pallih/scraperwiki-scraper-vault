# Ruby scraper for consultations from Department for Business, Innovation and Skills (BIS)
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department for Business, Innovation and Skills (BIS)"

def scrape_page(url)
  puts "Scraping #{url}"
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  consult_html = ScraperWiki.scrape(url)
  consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

  record['title'] = consult_doc.css('h1').inner_text
  record['published_date'] = Date.parse(consult_doc.css('meta[name="DC.date.issued"]')[0]['content']).to_s
  record['start_date'] = Date.parse(consult_doc.css('p.detail span')[0].inner_text).to_s
  record['end_date'] = Date.parse(consult_doc.css('p.detail span')[0].inner_text).to_s
  record['sponsor'] = ''

  # The description is held in the paragraphs after the "<h2>Background</h2>" and before the "Contact details"
  skipped_header = false
  reached_footer = false
  description = []
  consult_doc.css('div[property="dc:publisher"]').css('p').each do |e|
    if !skipped_header
      if e.name == "p" && e['class'] == "detail"
        # This is the header element, so everything after will be the content
        skipped_header = true
      end
    else
      if !reached_footer
        if e.name == "p" && e.inner_text.match(/contact details/i)
          # We've hit the "contact details" area, and so the end of the description
          reached_footer = true
        elsif e.name == "p" && e['class'] != "detail" 
          # Collect any paragraph elements
          description.push(e)
        end
      end
    end
  end

  unless description.empty? 
    record['description'] = description.collect { |d| d.to_s }.join("\n\n")
  else
    raise "#### ERROR: Failed to find the description"
  end

  # Find any linked documents
  parsed_consult_url = URI.parse(record['URI'])
  consult_documents = []
  consult_doc.css('a.mediaLink').each do |link|
    d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
    d['title'] = link.css('span')[0].inner_text
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
    puts "Record #{record_count}"
    scrape_page(consultation['permalink'])
  end
end

# Ruby scraper for consultations from Department for Business, Innovation and Skills (BIS)
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department for Business, Innovation and Skills (BIS)"

def scrape_page(url)
  puts "Scraping #{url}"
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  consult_html = ScraperWiki.scrape(url)
  consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

  record['title'] = consult_doc.css('h1').inner_text
  record['published_date'] = Date.parse(consult_doc.css('meta[name="DC.date.issued"]')[0]['content']).to_s
  record['start_date'] = Date.parse(consult_doc.css('p.detail span')[0].inner_text).to_s
  record['end_date'] = Date.parse(consult_doc.css('p.detail span')[0].inner_text).to_s
  record['sponsor'] = ''

  # The description is held in the paragraphs after the "<h2>Background</h2>" and before the "Contact details"
  skipped_header = false
  reached_footer = false
  description = []
  consult_doc.css('div[property="dc:publisher"]').css('p').each do |e|
    if !skipped_header
      if e.name == "p" && e['class'] == "detail"
        # This is the header element, so everything after will be the content
        skipped_header = true
      end
    else
      if !reached_footer
        if e.name == "p" && e.inner_text.match(/contact details/i)
          # We've hit the "contact details" area, and so the end of the description
          reached_footer = true
        elsif e.name == "p" && e['class'] != "detail" 
          # Collect any paragraph elements
          description.push(e)
        end
      end
    end
  end

  unless description.empty? 
    record['description'] = description.collect { |d| d.to_s }.join("\n\n")
  else
    raise "#### ERROR: Failed to find the description"
  end

  # Find any linked documents
  parsed_consult_url = URI.parse(record['URI'])
  consult_documents = []
  consult_doc.css('a.mediaLink').each do |link|
    d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
    d['title'] = link.css('span')[0].inner_text
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
    puts "Record #{record_count}"
    scrape_page(consultation['permalink'])
  end
end

