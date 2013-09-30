require 'mechanize'
require 'open-uri'

def extract_links(page)
  page.at('#companylist ul').search('article').map do |a|
    b = a.at('h1 a')
    "http://www.bandt.com.au" + b['href']
  end
end

def go_to_page(page, page_no)
  form = page.forms[0]
  form["__EVENTTARGET"] =
    "plc$lt$zoneContent$MainContentPlaceholder$MainContentPlaceholder$lt$zoneCenter$RBIRandomOrderRepeater$pager"
  form["__EVENTARGUMENT"] = page_no
  form.submit
end

agent = Mechanize.new

response = agent.get("http://www.bandt.com.au/companies/advertising-agencies?Location=NSW")
links = extract_links(response)

page_no = 1
while response.at('.paginator .next a') do
  # Go to the next page
  page_no += 1
  response = go_to_page(response, page_no)
  links += extract_links(response)
end

links.each do |link|
  # Using Nokogiri because the web server seems to randomly return the wrong content-type which
  # confuses the hell out of mechanize. So, always interpreting what comes back as html
  begin
    response = Nokogiri::HTML(open(link))
  rescue
    puts "Skipping link: #{link}"
  end
 
  if response
    if response.search('#detailinfo .phone')
      if response.search('#detailinfo .phone')[0] && response.search('#detailinfo .phone')[0].at('p')
        phone = response.search('#detailinfo .phone')[0].at('p').inner_html
      end
      if response.search('#detailinfo .phone')[1] && response.search('#detailinfo .phone')[1].at('p')
        fax = response.search('#detailinfo .phone')[1].at('p').inner_html
      end
    end
    name = response.at('#maincolumn h1').inner_html if response.at('#maincolumn h1')
    if response.at('#detailinfo span[itemprop="streetAddress"]')
      street_address = response.at('#detailinfo span[itemprop="streetAddress"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="addressLocality"]')
      address_locality = response.at('#detailinfo span[itemprop="addressLocality"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="addressRegion"]')
      address_region = response.at('#detailinfo span[itemprop="addressRegion"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="postalCode"]')
      postal_code = response.at('#detailinfo span[itemprop="postalCode"]').inner_text.strip
    end
    website = response.at('#exmessage1 a')['href'] if response.at('#exmessage1 a')
    description = response.at('#bodycontent .alpha p').inner_html if response.at('#bodycontent .alpha p')

    ScraperWiki.save_sqlite([],
      name: name,
      street_address: street_address,
      address_locality: address_locality,
      address_region: address_region,
      postal_code: postal_code,
      phone: phone,
      fax: fax,
      website: website,
      description: description
    )
  end
end

require 'mechanize'
require 'open-uri'

def extract_links(page)
  page.at('#companylist ul').search('article').map do |a|
    b = a.at('h1 a')
    "http://www.bandt.com.au" + b['href']
  end
end

def go_to_page(page, page_no)
  form = page.forms[0]
  form["__EVENTTARGET"] =
    "plc$lt$zoneContent$MainContentPlaceholder$MainContentPlaceholder$lt$zoneCenter$RBIRandomOrderRepeater$pager"
  form["__EVENTARGUMENT"] = page_no
  form.submit
end

agent = Mechanize.new

response = agent.get("http://www.bandt.com.au/companies/advertising-agencies?Location=NSW")
links = extract_links(response)

page_no = 1
while response.at('.paginator .next a') do
  # Go to the next page
  page_no += 1
  response = go_to_page(response, page_no)
  links += extract_links(response)
end

links.each do |link|
  # Using Nokogiri because the web server seems to randomly return the wrong content-type which
  # confuses the hell out of mechanize. So, always interpreting what comes back as html
  begin
    response = Nokogiri::HTML(open(link))
  rescue
    puts "Skipping link: #{link}"
  end
 
  if response
    if response.search('#detailinfo .phone')
      if response.search('#detailinfo .phone')[0] && response.search('#detailinfo .phone')[0].at('p')
        phone = response.search('#detailinfo .phone')[0].at('p').inner_html
      end
      if response.search('#detailinfo .phone')[1] && response.search('#detailinfo .phone')[1].at('p')
        fax = response.search('#detailinfo .phone')[1].at('p').inner_html
      end
    end
    name = response.at('#maincolumn h1').inner_html if response.at('#maincolumn h1')
    if response.at('#detailinfo span[itemprop="streetAddress"]')
      street_address = response.at('#detailinfo span[itemprop="streetAddress"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="addressLocality"]')
      address_locality = response.at('#detailinfo span[itemprop="addressLocality"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="addressRegion"]')
      address_region = response.at('#detailinfo span[itemprop="addressRegion"]').inner_text.strip
    end
    if response.at('#detailinfo span[itemprop="postalCode"]')
      postal_code = response.at('#detailinfo span[itemprop="postalCode"]').inner_text.strip
    end
    website = response.at('#exmessage1 a')['href'] if response.at('#exmessage1 a')
    description = response.at('#bodycontent .alpha p').inner_html if response.at('#bodycontent .alpha p')

    ScraperWiki.save_sqlite([],
      name: name,
      street_address: street_address,
      address_locality: address_locality,
      address_region: address_region,
      postal_code: postal_code,
      phone: phone,
      fax: fax,
      website: website,
      description: description
    )
  end
end

