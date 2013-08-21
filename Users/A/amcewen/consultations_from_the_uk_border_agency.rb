# Ruby scraper for consultations from the UK Border Agency
require 'nokogiri'
require 'uri'

DEPARTMENT = "UK Border Agency"

def scrape_page(url)
  # Details of the consultation
  record = { 'URI' => url, 'department' => '', 'agency' => DEPARTMENT }
  # Any documents linked from the consultation page
  documents = []

  consult_html = ScraperWiki.scrape(url)
  consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

  # Check it hasn't been archived (which seems to result in a redirect trail that ends in "page not found"...)
  unless consult_doc.css('title').inner_text.match(/page not found/i)
    record['title'] = consult_doc.css('meta[name="DC.title"]')[0]['content']

    record['published_date'] = Date.parse(consult_doc.css('meta[name="DC.date.created"]')[0]['content']).to_s
    unless consult_doc.css('span[property="dc:issued"]').empty? 
      record['start_date'] = Date.parse(consult_doc.css('span[property="dc:issued"]')[0]['content']).to_s
    else
      puts "No start date present"
    end
    unless consult_doc.css('span[property="dc:valid"]').empty? 
      record['end_date'] = Date.parse(consult_doc.css('span[property="dc:valid"]')[0]['content']).to_s
    else
      puts "No end date present"
    end
    record['sponsor'] = ''
    if !consult_doc.css('div[property="dc:abstract"]').empty? 
      record['description'] = consult_doc.css('div[property="dc:abstract"]')[0].inner_text
    elsif !consult_doc.css('meta[name="DC.description"]').empty? 
      record['description'] = consult_doc.css('meta[name="DC.description"]')[0]['content']
    else
      # We don't have a dc:abstract text, so use the first paragraph after the blank abstract
      record['description'] = ""
      skipped_header = false
      consult_doc.css('div#LeftCenterRight')[0].children.each do |n|
        if !skipped_header
          if n.name == 'div' && n['property'] == 'dc:abstract'
            skipped_header = true
          end
        else
          if n.name == 'p' && record['description'] == ""
            # This is the first paragraph after the blank abstract div, so use it as the description
            record['description'] = n.to_s
          end
        end
      end
    end

    # Find any linked documents
    parsed_consult_url = URI.parse(record['URI'])
    consult_documents = []
    consult_doc.css('a[rel="dc:hasPart"]').each do |link|
      d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
      d['title'] = link.inner_text
      consult_documents.push(d)
    end
    consult_doc.css('a.pdf').each do |link|
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
end


record_count = 0

# There are two pages showing current and archived consultations
["http://www.ukba.homeoffice.gov.uk/policyandlaw/consultations/", "http://www.ukba.homeoffice.gov.uk/policyandlaw/consultations/closed/"].each do |index_url|
#["http://www.ukba.homeoffice.gov.uk/policyandlaw/consultations/closed/"].each do |index_url|
  index = ScraperWiki.scrape(index_url)
  index_doc = Nokogiri::HTML(index, nil, 'utf-8')
  parsed_index_url = URI.parse(index_url)

  index_doc.css("#fourthLvlNav a").each do |consultation|
    if consultation['class'] != "backToPage" # Skip the "back" link, which is at the same level as the consultations
      record_count = record_count + 1
      consultation_url = parsed_index_url.merge(consultation['href']).to_s
      puts "Record #{record_count} "+consultation_url
      scrape_page(consultation_url)
    end
  end
end

