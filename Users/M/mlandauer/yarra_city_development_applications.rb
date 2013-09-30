require 'mechanize'

url = "http://www.yarracity.vic.gov.au/Planning-Application-Search/Results.aspx?ApplicationNumber=&Suburb=(All)&Street=(All)&Status=Current&Ward=(All)"

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def get_page_data(page)
  comment_url = "http://www.yarracity.vic.gov.au/planning--building/Planning-applications/Objecting-to-a-planning-applicationVCAT/"

  trs = page.search('table tr')
  trs[1..-2].each do |tr|
    texts = tr.search('td').map{|n| n.inner_text}
    council_reference = clean_whitespace(texts[0])
    info_url = "http://www.yarracity.vic.gov.au/Planning-Application-Search/Results.aspx?ApplicationNumber=#{council_reference}&Suburb=(All)&Street=(All)&Status=(All)&Ward=(All)"
    record = {
      'info_url' => info_url,
      'comment_url' => comment_url,
      'council_reference' => council_reference,
      'date_received' => Date.parse(texts[1]).to_s,
      'address' => clean_whitespace(texts[2]),
      'description' => clean_whitespace(texts[3]),
      'date_scraped' => Date.today.to_s
    }
    begin
      record["on_notice_from"] = Date.parse(texts[4]).to_s
    rescue
      # In case the date is invalid
    end

    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end

agent = Mechanize.new

page = agent.get(url)

current_page = 1
begin
  get_page_data(page)

  # Click on the link to the next page
  links = page.search('table tr')[-1].search('a')
  link = links.find{|a| a.inner_text.to_i == current_page + 1}
  # This page has a really odd paging mechanism
  if link.nil? 
    # Ignore the first link in case it's a "..." as well that will go back rather than forward
    link = links[1..-1].find{|a| a.inner_text == "..."}
  end
  if link
    href = link["href"]
    first_argument = href.match(/javascript:__doPostBack\('(.*)',''\)/)[1]
    # We're faking what the __doPostBack javascript does
    form = page.forms.first
    form["__EVENTTARGET"] = first_argument
    page = form.submit
    current_page += 1
  end
end while link

require 'mechanize'

url = "http://www.yarracity.vic.gov.au/Planning-Application-Search/Results.aspx?ApplicationNumber=&Suburb=(All)&Street=(All)&Status=Current&Ward=(All)"

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def get_page_data(page)
  comment_url = "http://www.yarracity.vic.gov.au/planning--building/Planning-applications/Objecting-to-a-planning-applicationVCAT/"

  trs = page.search('table tr')
  trs[1..-2].each do |tr|
    texts = tr.search('td').map{|n| n.inner_text}
    council_reference = clean_whitespace(texts[0])
    info_url = "http://www.yarracity.vic.gov.au/Planning-Application-Search/Results.aspx?ApplicationNumber=#{council_reference}&Suburb=(All)&Street=(All)&Status=(All)&Ward=(All)"
    record = {
      'info_url' => info_url,
      'comment_url' => comment_url,
      'council_reference' => council_reference,
      'date_received' => Date.parse(texts[1]).to_s,
      'address' => clean_whitespace(texts[2]),
      'description' => clean_whitespace(texts[3]),
      'date_scraped' => Date.today.to_s
    }
    begin
      record["on_notice_from"] = Date.parse(texts[4]).to_s
    rescue
      # In case the date is invalid
    end

    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end

agent = Mechanize.new

page = agent.get(url)

current_page = 1
begin
  get_page_data(page)

  # Click on the link to the next page
  links = page.search('table tr')[-1].search('a')
  link = links.find{|a| a.inner_text.to_i == current_page + 1}
  # This page has a really odd paging mechanism
  if link.nil? 
    # Ignore the first link in case it's a "..." as well that will go back rather than forward
    link = links[1..-1].find{|a| a.inner_text == "..."}
  end
  if link
    href = link["href"]
    first_argument = href.match(/javascript:__doPostBack\('(.*)',''\)/)[1]
    # We're faking what the __doPostBack javascript does
    form = page.forms.first
    form["__EVENTTARGET"] = first_argument
    page = form.submit
    current_page += 1
  end
end while link

