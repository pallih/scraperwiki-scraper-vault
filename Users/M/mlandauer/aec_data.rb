require 'mechanize'

# see https://gist.github.com/mlandauer/5182346

# See http://en.wikipedia.org/wiki/Postcodes_in_Australia
 
# Postcodes that are used for LVRs and PO boxes only
def australian_postcodes_po_boxes
  nsw = (1000..1999).to_a
  act = (200..299).to_a
  vic = (8000..8999).to_a
  qld = (9000..9999).to_a
  sa = (5800..5999).to_a
  wa = (6800..6999).to_a
  tas = (7800..7999).to_a
  nt = (900..999).to_a
 
  # Convert integers to strings (postcodes are *not* integers)
  (nsw + act + vic + qld + sa + wa + tas + nt).map { |p| "%04i" % p }
end
 
# Postcodes that are used for regular street addresses (Not PO boxes and LVRs)
def australian_postcodes_regular
  nsw = (2000..2599).to_a +
        (2619..2898).to_a +
        (2921..2999).to_a
  act = (2600..2618).to_a +
        (2900..2920).to_a
  vic = (3000..3999).to_a
  qld = (4000..4999).to_a
  sa =  (5000..5799).to_a
  wa =  (6000..6797).to_a
  tas = (7000..7799).to_a
  nt =  (800..899).to_a
 
  # Convert integers to strings (postcodes are *not* integers)
  (nsw + act + vic + qld + sa + wa + tas + nt).map { |p| "%04i" % p }
end
 
# Returns an array of Australian Postcodes
def australian_postcodes
  australian_postcodes_regular + australian_postcodes_po_boxes
end

def scrape_page(p)
  p.search('table[border="1"] > tr').each do |tr|
    if tr["class"].nil? 
      v = tr.search('td')
      return if v[0].inner_text =~ /Please search again/
      record = {
        :state => v[0].inner_text,
        :suburb => v[1].inner_text,
        :postcode => v[2].inner_text,
        :electorate => v[3].inner_text,
      }
      partial_record = {
        :postcode => record[:postcode],
        :electorate => record[:electorate],
      }
      #p record
      ScraperWiki::save_sqlite(record.keys, record, 'full')
      ScraperWiki::save_sqlite(partial_record.keys, partial_record, 'postcode')
    end
  end
end

def scrape_results(url)
  agent = Mechanize.new
  puts "Scraping page 1..."
  p = agent.get(url)

  viewstate = p.at('#aspnetForm input[name="__VIEWSTATE"]')["value"]
  eventvalidation = p.at('#aspnetForm input[name="__EVENTVALIDATION"]')["value"]
  number_of_pages = p.search('tr.pagingLink table td').count
  current_page = 1

  while true do
    scrape_page(p)

    if number_of_pages > current_page
      current_page += 1
      puts "Scraping page #{current_page}..."
      p = agent.post(url,
        "__EVENTTARGET" => "ctl00$ContentPlaceHolderBody$gridViewLocalities",
        "__EVENTARGUMENT" => "Page$#{current_page}",
        "__VIEWSTATE" => viewstate,
        "__EVENTVALIDATION" => eventvalidation,
      )
    else
      break
    end
  end
end

fetched_postcodes = ScraperWiki::select('postcode from postcode').map { |h| h['postcode'] }

australian_postcodes_regular.each do |postcode|
  if fetched_postcodes.include? postcode
    puts "Skipping already fetched postcode #{postcode}"
  else
    puts "Getting results for postcode #{postcode}..."
    scrape_results("http://apps.aec.gov.au/eSearch/LocalitySearchResults.aspx?filter=#{postcode}&filterby=Postcode")
  end
end


require 'mechanize'

# see https://gist.github.com/mlandauer/5182346

# See http://en.wikipedia.org/wiki/Postcodes_in_Australia
 
# Postcodes that are used for LVRs and PO boxes only
def australian_postcodes_po_boxes
  nsw = (1000..1999).to_a
  act = (200..299).to_a
  vic = (8000..8999).to_a
  qld = (9000..9999).to_a
  sa = (5800..5999).to_a
  wa = (6800..6999).to_a
  tas = (7800..7999).to_a
  nt = (900..999).to_a
 
  # Convert integers to strings (postcodes are *not* integers)
  (nsw + act + vic + qld + sa + wa + tas + nt).map { |p| "%04i" % p }
end
 
# Postcodes that are used for regular street addresses (Not PO boxes and LVRs)
def australian_postcodes_regular
  nsw = (2000..2599).to_a +
        (2619..2898).to_a +
        (2921..2999).to_a
  act = (2600..2618).to_a +
        (2900..2920).to_a
  vic = (3000..3999).to_a
  qld = (4000..4999).to_a
  sa =  (5000..5799).to_a
  wa =  (6000..6797).to_a
  tas = (7000..7799).to_a
  nt =  (800..899).to_a
 
  # Convert integers to strings (postcodes are *not* integers)
  (nsw + act + vic + qld + sa + wa + tas + nt).map { |p| "%04i" % p }
end
 
# Returns an array of Australian Postcodes
def australian_postcodes
  australian_postcodes_regular + australian_postcodes_po_boxes
end

def scrape_page(p)
  p.search('table[border="1"] > tr').each do |tr|
    if tr["class"].nil? 
      v = tr.search('td')
      return if v[0].inner_text =~ /Please search again/
      record = {
        :state => v[0].inner_text,
        :suburb => v[1].inner_text,
        :postcode => v[2].inner_text,
        :electorate => v[3].inner_text,
      }
      partial_record = {
        :postcode => record[:postcode],
        :electorate => record[:electorate],
      }
      #p record
      ScraperWiki::save_sqlite(record.keys, record, 'full')
      ScraperWiki::save_sqlite(partial_record.keys, partial_record, 'postcode')
    end
  end
end

def scrape_results(url)
  agent = Mechanize.new
  puts "Scraping page 1..."
  p = agent.get(url)

  viewstate = p.at('#aspnetForm input[name="__VIEWSTATE"]')["value"]
  eventvalidation = p.at('#aspnetForm input[name="__EVENTVALIDATION"]')["value"]
  number_of_pages = p.search('tr.pagingLink table td').count
  current_page = 1

  while true do
    scrape_page(p)

    if number_of_pages > current_page
      current_page += 1
      puts "Scraping page #{current_page}..."
      p = agent.post(url,
        "__EVENTTARGET" => "ctl00$ContentPlaceHolderBody$gridViewLocalities",
        "__EVENTARGUMENT" => "Page$#{current_page}",
        "__VIEWSTATE" => viewstate,
        "__EVENTVALIDATION" => eventvalidation,
      )
    else
      break
    end
  end
end

fetched_postcodes = ScraperWiki::select('postcode from postcode').map { |h| h['postcode'] }

australian_postcodes_regular.each do |postcode|
  if fetched_postcodes.include? postcode
    puts "Skipping already fetched postcode #{postcode}"
  else
    puts "Getting results for postcode #{postcode}..."
    scrape_results("http://apps.aec.gov.au/eSearch/LocalitySearchResults.aspx?filter=#{postcode}&filterby=Postcode")
  end
end


