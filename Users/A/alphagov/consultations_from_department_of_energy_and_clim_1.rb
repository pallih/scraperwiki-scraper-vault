# Ruby scraper for consultations from Department of Energy and Climate Change
require 'nokogiri'
require 'uri'

DEPARTMENT = "Department of Energy and Climate Change"

# Because ScraperWiki.scrape just uses Net::HTTP.get under the hood and because that doesn't support redirects...
def scrape_with_redirect(url, limit = 10)
  # You should choose better exception.
  raise ArgumentError, 'HTTP redirect too deep' if limit == 0

  parsed_url = URI.parse(url)
  response = Net::HTTP.get_response(parsed_url)
  case response
  when Net::HTTPSuccess     then response.body
  when Net::HTTPRedirection then scrape_with_redirect(parsed_url.merge(response['location']).to_s, limit - 1)
  else
    response.error!
  end
end

def scrape_page(url, from_date, to_date)
  # Details of the consultation
  record = { 'URI' => url, 'department' => DEPARTMENT, 'agency' => '', 'start_date' => from_date.to_s,
             'end_date' => to_date.to_s }
  # Any documents linked from the consultation page
  documents = []

  consult_html = ScraperWiki.scrape(url)
  consult_doc = Nokogiri::HTML(consult_html, nil, 'utf-8')

  record['title'] = consult_doc.css('h2#ctl00_Pagetitle').inner_text

  #record['published_date'] = Date.parse(consult_doc.css('span[property="dc:issued"]')[0]['content']).to_s
  record['sponsor'] = ''
  record['description'] = consult_doc.css('.cms-text')[0].css('p').to_s

  # Find any linked documents
  parsed_consult_url = URI.parse(record['URI'])
  consult_documents = []
  consult_doc.css('.cms-documents a').each do |link|
    link_url = link['href'].gsub(" ", "%20").gsub('\\', "%5C")
    # link_url actually takes us to a "download this document" page rather than the download itself...
    download_html = scrape_with_redirect(parsed_consult_url.merge(link_url).to_s)
    download_doc = Nokogiri::HTML(download_html, nil, 'utf-8')
    d = { 'consultation' => record['URI'], 'URI' => parsed_consult_url.merge(download_doc.css('.content a')[0]['href']).to_s }
    d['title'] = link.inner_text
    consult_documents.push(d)
  end

  puts consult_documents.size.to_s+" documents: "+consult_documents.collect { |d| d['title'] }.join("; ")
 
  ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  consult_documents.each do |d|
    ScraperWiki.save_sqlite(['URI'], d, 'documents')
  end
end

record_count = 0
['http://www.decc.gov.uk/en/content/cms/consultations/open/open.aspx',
 'http://www.decc.gov.uk/en/content/cms/consultations/closed_awaiting/closed_awaiting.aspx',
 'http://www.decc.gov.uk/en/content/cms/consultations/closed/closed.aspx'].each do |list_url|
  puts "Checking list #{list_url}"
  list_html = ScraperWiki.scrape(list_url)
  list_doc = Nokogiri::HTML(list_html, nil, 'utf-8')
  parsed_list_url = URI.parse(list_url)

  list_doc.css('.cms-text li').each do |consultation|
    # Work out the dates first
    dates = consultation.css('strong').inner_text.split('-')
    if dates.size == 1
      # We haven't split the dates - might be because we've got an mdash rather than a normal one
      dates = consultation.css('strong').inner_text.split("\200")
    end
    from_date = Date.parse(dates[0])
    to_date = Date.parse(dates[1])

    # We're only interested in scraping consultations valid since the coalition got into power
    if to_date > Date.parse("01 May 2010")
      record_count = record_count + 1
      consultation_link = parsed_list_url.merge(consultation.css('a')[0]['href']).to_s
      puts "Record #{record_count} "+consultation_link
      if consultation_link.match(/www.decc.gov.uk/i)
        scrape_page(consultation_link, from_date, to_date)
      else
        puts "Skipping #{consultation_link}"
      end
    end
  end
end

