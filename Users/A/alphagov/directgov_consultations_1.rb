# Ruby scraper for consultations.direct.gov.uk
require 'nokogiri'
require 'uri'

# Just searching for all dates gives us too many results - i.e. the search system only returns the first 50 pages
# of results regardless of whether or not there are more than 1000 possible matches
# So, we'll look through them one year at a time.  Experimentation with the search field shows that 1998 is when
# the first results are returned, so start then
# Actually only results from the current government are needed, so anything from 2010 onwards will catch that

(2010..Time.now.year).each do |y|

  puts "Processing consultations for #{y}"

  # Start searching for a very common word - suspect "a" will be in all the consultations...
  base_url = 'http://consultations.direct.gov.uk/search?q=a&as_q=inmeta%3Adc%253aavailable%3Adaterange%3A..'+y.to_s+'-12-31+AND+inmeta%3Adc%253avalid%3Adaterange%3A'+y.to_s+'-01-01..&inmetafield=&error=&site=dg_default&date_filter=All_Dates&from_dateDD=01&from_dateMM=01&from_dateYY='+y.to_s+'&to_dateDD=31&to_dateMM=12&to_dateYY='+y.to_s+'&btnG=Search&client=dg_default&output=xml_no_dtd&proxystylesheet=dg_default&sort=date%3AD%3AL%3Ad1&entqr=3&requiredfields=dc%253atype&oe=UTF-8&ie=UTF-8&ud=1&getfields=dc%3Aabstract.dc%3Apublisher.dc%3Aavailable.dc%3Avalid.dc%3Aidentifier.dc%3Asource.dc%3Atitle&num=20&filter=0'
  starting_url = base_url
  puts starting_url

  # Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
  while !starting_url.nil? 
    puts "Getting "+starting_url
    parsed_base_url = URI.parse(starting_url)
    html = ScraperWiki.scrape(starting_url)
 
    doc = Nokogiri::HTML(html)

    # Double-check that we haven't got more than a 1000 results, as if we have then we need to pick a smaller date range
    if doc.css('#results_bar').inner_text.match(/of.*\d\d\d\d/)
      # We've hit four-digit results count, which we won't reach the end of
      raise "#### ERROR: Too many results returned"
    end
 
    # And now scrape the consultations
    doc.css('div.result-header').each do |consultation|
      record = {'permalink' => consultation.css('a')[0]['href'],
                'title' => consultation.css('a')[0].inner_text }
      unless consultation.css('span.metatitle').empty? || consultation.css('span.metatitle')[0].inner_text.match(/^start/i)
        record['department'] = consultation.css('span.metatitle')[0].inner_text
      else
        puts "Couldn't find department for "+consultation.to_s
        # Match it from the permalink host
        depts = { "www.charitycommission.gov.uk" => "Charity Commission for England and Wales",
                  "www.bis.gov.uk" => "Department for Business, Innovation and Skills (BIS)",
                  "www.communities.gov.uk" => "Department for Communities and Local Government",
                  "www.culture.gov.uk" => "Department for Culture, Media and Sport",
                  "www.defra.gov.uk" => "Department for Environment, Food and Rural Affairs",
                  "www.dfid.gov.uk" => "Department for International Development",
                  "www.dft.gov.uk" => "Department for Transport",
                  "www.dwp.gov.uk" => "Department for Work and Pensions",
                  "www.decc.gov.uk" => "Department of Energy and Climate Change",
                  "www.dh.gov.uk" => "Department of Health",
                  "www.dsa.gov.uk" => "Driving Standards Agency",
                  "www.food.gov.uk" => "Food Standards Agency",
                  "www.highways.gov.uk" => "Highways Agency",
                  "www.hm-treasury.gov.uk" => "HM Treasury",
                  "www.homeoffice.gov.uk" => "Home Office",
                  "www.mod.uk" => "Ministry of Defence",
                  "www.justice.gov.uk" => "Ministry of Justice",
                  "www.dh.gov.uk" => "Department of Health",
                  "www.ofgem.gov.uk" => "OFGEM",
                  "www.ipo.gov.uk" => "Intellectual Property Office",
                  "www.hse.gov.uk" => "Health and Safety Executive" }
        record['department'] = depts[URI.parse(record['permalink']).host]
      end

      dates = consultation.css('span.metadata').inner_text.match(/.*[open|start|starting] date:(.*)[close|closing] date:(.*)/i)
      unless dates.nil? 
        begin
          record['start_date'] = Date.strptime(dates[1].strip, "%d/%m/%Y")
          record['closing_date'] = Date.strptime(dates[2].strip, "%d/%m/%Y")
        rescue
          # We haven't managed to parse the dates as dd/mm/yyyy, see if Date.parse can cope with them
          record['start_date'] = Date.parse(dates[1].strip)
          record['closing_date'] = Date.parse(dates[2].strip)
        end
      end

      begin
        ScraperWiki.save(['permalink'], record)
      rescue => e
        puts e.message
        puts record.inspect
      end
    end

    # Get the next page of results
    if doc.css('a.pagnext').empty? 
      # We've reached the end of the results
      starting_url = nil
    else
      # Get the next page of results
      starting_url = parsed_base_url.merge(doc.css('a.pagnext')[0]['href']).to_s
    end
  end
end

# Ruby scraper for consultations.direct.gov.uk
require 'nokogiri'
require 'uri'

# Just searching for all dates gives us too many results - i.e. the search system only returns the first 50 pages
# of results regardless of whether or not there are more than 1000 possible matches
# So, we'll look through them one year at a time.  Experimentation with the search field shows that 1998 is when
# the first results are returned, so start then
# Actually only results from the current government are needed, so anything from 2010 onwards will catch that

(2010..Time.now.year).each do |y|

  puts "Processing consultations for #{y}"

  # Start searching for a very common word - suspect "a" will be in all the consultations...
  base_url = 'http://consultations.direct.gov.uk/search?q=a&as_q=inmeta%3Adc%253aavailable%3Adaterange%3A..'+y.to_s+'-12-31+AND+inmeta%3Adc%253avalid%3Adaterange%3A'+y.to_s+'-01-01..&inmetafield=&error=&site=dg_default&date_filter=All_Dates&from_dateDD=01&from_dateMM=01&from_dateYY='+y.to_s+'&to_dateDD=31&to_dateMM=12&to_dateYY='+y.to_s+'&btnG=Search&client=dg_default&output=xml_no_dtd&proxystylesheet=dg_default&sort=date%3AD%3AL%3Ad1&entqr=3&requiredfields=dc%253atype&oe=UTF-8&ie=UTF-8&ud=1&getfields=dc%3Aabstract.dc%3Apublisher.dc%3Aavailable.dc%3Avalid.dc%3Aidentifier.dc%3Asource.dc%3Atitle&num=20&filter=0'
  starting_url = base_url
  puts starting_url

  # Keep getting pages of results until we reach the end (i.e. a page without a "Next" link)
  while !starting_url.nil? 
    puts "Getting "+starting_url
    parsed_base_url = URI.parse(starting_url)
    html = ScraperWiki.scrape(starting_url)
 
    doc = Nokogiri::HTML(html)

    # Double-check that we haven't got more than a 1000 results, as if we have then we need to pick a smaller date range
    if doc.css('#results_bar').inner_text.match(/of.*\d\d\d\d/)
      # We've hit four-digit results count, which we won't reach the end of
      raise "#### ERROR: Too many results returned"
    end
 
    # And now scrape the consultations
    doc.css('div.result-header').each do |consultation|
      record = {'permalink' => consultation.css('a')[0]['href'],
                'title' => consultation.css('a')[0].inner_text }
      unless consultation.css('span.metatitle').empty? || consultation.css('span.metatitle')[0].inner_text.match(/^start/i)
        record['department'] = consultation.css('span.metatitle')[0].inner_text
      else
        puts "Couldn't find department for "+consultation.to_s
        # Match it from the permalink host
        depts = { "www.charitycommission.gov.uk" => "Charity Commission for England and Wales",
                  "www.bis.gov.uk" => "Department for Business, Innovation and Skills (BIS)",
                  "www.communities.gov.uk" => "Department for Communities and Local Government",
                  "www.culture.gov.uk" => "Department for Culture, Media and Sport",
                  "www.defra.gov.uk" => "Department for Environment, Food and Rural Affairs",
                  "www.dfid.gov.uk" => "Department for International Development",
                  "www.dft.gov.uk" => "Department for Transport",
                  "www.dwp.gov.uk" => "Department for Work and Pensions",
                  "www.decc.gov.uk" => "Department of Energy and Climate Change",
                  "www.dh.gov.uk" => "Department of Health",
                  "www.dsa.gov.uk" => "Driving Standards Agency",
                  "www.food.gov.uk" => "Food Standards Agency",
                  "www.highways.gov.uk" => "Highways Agency",
                  "www.hm-treasury.gov.uk" => "HM Treasury",
                  "www.homeoffice.gov.uk" => "Home Office",
                  "www.mod.uk" => "Ministry of Defence",
                  "www.justice.gov.uk" => "Ministry of Justice",
                  "www.dh.gov.uk" => "Department of Health",
                  "www.ofgem.gov.uk" => "OFGEM",
                  "www.ipo.gov.uk" => "Intellectual Property Office",
                  "www.hse.gov.uk" => "Health and Safety Executive" }
        record['department'] = depts[URI.parse(record['permalink']).host]
      end

      dates = consultation.css('span.metadata').inner_text.match(/.*[open|start|starting] date:(.*)[close|closing] date:(.*)/i)
      unless dates.nil? 
        begin
          record['start_date'] = Date.strptime(dates[1].strip, "%d/%m/%Y")
          record['closing_date'] = Date.strptime(dates[2].strip, "%d/%m/%Y")
        rescue
          # We haven't managed to parse the dates as dd/mm/yyyy, see if Date.parse can cope with them
          record['start_date'] = Date.parse(dates[1].strip)
          record['closing_date'] = Date.parse(dates[2].strip)
        end
      end

      begin
        ScraperWiki.save(['permalink'], record)
      rescue => e
        puts e.message
        puts record.inspect
      end
    end

    # Get the next page of results
    if doc.css('a.pagnext').empty? 
      # We've reached the end of the results
      starting_url = nil
    else
      # Get the next page of results
      starting_url = parsed_base_url.merge(doc.css('a.pagnext')[0]['href']).to_s
    end
  end
end

