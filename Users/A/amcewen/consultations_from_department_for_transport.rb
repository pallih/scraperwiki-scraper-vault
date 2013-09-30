# Ruby scraper for consultations from Department for Transport
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department for Transport"

def scrape_page(url)
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  begin
    consult_html = ScraperWiki.scrape(url)
    consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

    unless consult_doc.css('h1').inner_text.match(/archived/i)
      record['title'] = consult_doc.css('h1[property="dc:title"]').inner_text

      record['published_date'] = Date.parse(consult_doc.css('meta[name="Date.issued"]')[0]['content']).to_s
      unless consult_doc.css('span[property="dc:issued"]').empty? 
        record['start_date'] = Date.parse(consult_doc.css('span[property="dc:issued"]')[0]['content']).to_s
      else
        puts "No start date present"
      end
      record['end_date'] = Date.parse(consult_doc.css('span[property="dc:valid"]')[0]['content']).to_s
      record['sponsor'] = ''
      record['description'] = consult_doc.css('span[property="dc:abstract"]').inner_html

      # Find any linked documents
      parsed_consult_url = URI.parse(record['URI'])
      consult_documents = []
      consult_doc.css('h2.pdf a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.doc a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.xls a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.zip a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2').each do |heading|
        if !heading['class'].nil? && heading['class'] != "doc" && heading['class'] != "pdf" && heading['class'] != "xls" && heading['class'] != "zip"
          raise "#### ERROR: Got h2 that wasn't a doc or pdf: "+heading.to_s
        end
      end

      puts consult_documents.size.to_s+" documents: "+consult_documents.collect { |d| d['title'] }.join("; ")
 
      ScraperWiki.save_sqlite(['URI'], record, 'consultations')
      consult_documents.each do |d|
        ScraperWiki.save_sqlite(['URI'], d, 'documents')
      end
    else
      puts "This consultation has been archived"
    end
  rescue Net::HTTPServerException => e
    if e == 404
      puts "This consultation has been archived"
    end
    puts e.inspect
  end
end


# The list of consultations is in a separate scraper, so we can just run through the results for that
# looking for ones relevant to this department
record_count = 0
ScraperWiki.attach('directgov_consultations') 
ScraperWiki.select("* from 'directgov_consultations'.swdata").each do |consultation|
  if consultation['department'] == DEPARTMENT
    record_count = record_count + 1
    puts "Record #{record_count} "+consultation['permalink']
    scrape_page(consultation['permalink'])
  end
end

# Ruby scraper for consultations from Department for Transport
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department for Transport"

def scrape_page(url)
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '' }
  # Any documents linked from the consultation page
  documents = []

  begin
    consult_html = ScraperWiki.scrape(url)
    consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

    unless consult_doc.css('h1').inner_text.match(/archived/i)
      record['title'] = consult_doc.css('h1[property="dc:title"]').inner_text

      record['published_date'] = Date.parse(consult_doc.css('meta[name="Date.issued"]')[0]['content']).to_s
      unless consult_doc.css('span[property="dc:issued"]').empty? 
        record['start_date'] = Date.parse(consult_doc.css('span[property="dc:issued"]')[0]['content']).to_s
      else
        puts "No start date present"
      end
      record['end_date'] = Date.parse(consult_doc.css('span[property="dc:valid"]')[0]['content']).to_s
      record['sponsor'] = ''
      record['description'] = consult_doc.css('span[property="dc:abstract"]').inner_html

      # Find any linked documents
      parsed_consult_url = URI.parse(record['URI'])
      consult_documents = []
      consult_doc.css('h2.pdf a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.doc a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.xls a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2.zip a').each do |link|
        d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(link['href'].gsub(" ", "%20")).to_s }
        d['title'] = link.inner_text
        consult_documents.push(d)
      end
      consult_doc.css('h2').each do |heading|
        if !heading['class'].nil? && heading['class'] != "doc" && heading['class'] != "pdf" && heading['class'] != "xls" && heading['class'] != "zip"
          raise "#### ERROR: Got h2 that wasn't a doc or pdf: "+heading.to_s
        end
      end

      puts consult_documents.size.to_s+" documents: "+consult_documents.collect { |d| d['title'] }.join("; ")
 
      ScraperWiki.save_sqlite(['URI'], record, 'consultations')
      consult_documents.each do |d|
        ScraperWiki.save_sqlite(['URI'], d, 'documents')
      end
    else
      puts "This consultation has been archived"
    end
  rescue Net::HTTPServerException => e
    if e == 404
      puts "This consultation has been archived"
    end
    puts e.inspect
  end
end


# The list of consultations is in a separate scraper, so we can just run through the results for that
# looking for ones relevant to this department
record_count = 0
ScraperWiki.attach('directgov_consultations') 
ScraperWiki.select("* from 'directgov_consultations'.swdata").each do |consultation|
  if consultation['department'] == DEPARTMENT
    record_count = record_count + 1
    puts "Record #{record_count} "+consultation['permalink']
    scrape_page(consultation['permalink'])
  end
end

