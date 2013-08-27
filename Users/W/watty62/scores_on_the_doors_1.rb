require 'mechanize'

BASE_URL = "http://www.aberdeencity.gov.uk/xhs_HealthSafetyInspections.asp"

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body, page_num)
  puts "scraping page #{page_num} of #{@page_count}"
  data_table = Nokogiri::HTML(page_body).css('#ScoresTable tr').collect do |row|
    if row.css('td').count > 5
      business = {}
      business['Business']      = row.css('td')[0].inner_text
      business['Address']       = row.css('td')[1].inner_text
      business['Operator']      = row.css('td')[2].inner_text
      business['Business Type'] = row.css('td')[3].inner_text
      business['Date Visited']  = row.css('td')[4].inner_text
      business['Report_Url']    = row.css('td')[5].inner_text
      ScraperWiki.save(["Business"], business)
    end
  end
end

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

page = @br.get(BASE_URL)

@page_count = Nokogiri::HTML(page.body).css('#PagingTable a').count

#puts @page_count 

scrape_table(page.body, 1)

for i in 2..@page_count

# puts i

  page.form_with(:action => 'xhs_HealthSafetyInspections.asp') do |f|
    f['page'] = i
    page = f.submit()
  end
  scrape_table(page.body, i)
endrequire 'mechanize'

BASE_URL = "http://www.aberdeencity.gov.uk/xhs_HealthSafetyInspections.asp"

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body, page_num)
  puts "scraping page #{page_num} of #{@page_count}"
  data_table = Nokogiri::HTML(page_body).css('#ScoresTable tr').collect do |row|
    if row.css('td').count > 5
      business = {}
      business['Business']      = row.css('td')[0].inner_text
      business['Address']       = row.css('td')[1].inner_text
      business['Operator']      = row.css('td')[2].inner_text
      business['Business Type'] = row.css('td')[3].inner_text
      business['Date Visited']  = row.css('td')[4].inner_text
      business['Report_Url']    = row.css('td')[5].inner_text
      ScraperWiki.save(["Business"], business)
    end
  end
end

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

page = @br.get(BASE_URL)

@page_count = Nokogiri::HTML(page.body).css('#PagingTable a').count

#puts @page_count 

scrape_table(page.body, 1)

for i in 2..@page_count

# puts i

  page.form_with(:action => 'xhs_HealthSafetyInspections.asp') do |f|
    f['page'] = i
    page = f.submit()
  end
  scrape_table(page.body, i)
endrequire 'mechanize'

BASE_URL = "http://www.aberdeencity.gov.uk/xhs_HealthSafetyInspections.asp"

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body, page_num)
  puts "scraping page #{page_num} of #{@page_count}"
  data_table = Nokogiri::HTML(page_body).css('#ScoresTable tr').collect do |row|
    if row.css('td').count > 5
      business = {}
      business['Business']      = row.css('td')[0].inner_text
      business['Address']       = row.css('td')[1].inner_text
      business['Operator']      = row.css('td')[2].inner_text
      business['Business Type'] = row.css('td')[3].inner_text
      business['Date Visited']  = row.css('td')[4].inner_text
      business['Report_Url']    = row.css('td')[5].inner_text
      ScraperWiki.save(["Business"], business)
    end
  end
end

@br = Mechanize.new { |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
}

page = @br.get(BASE_URL)

@page_count = Nokogiri::HTML(page.body).css('#PagingTable a').count

#puts @page_count 

scrape_table(page.body, 1)

for i in 2..@page_count

# puts i

  page.form_with(:action => 'xhs_HealthSafetyInspections.asp') do |f|
    f['page'] = i
    page = f.submit()
  end
  scrape_table(page.body, i)
end