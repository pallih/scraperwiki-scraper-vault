require 'nokogiri'

BASE_URL = "https://good-practice.bibb.de/adb/"

def scrape_list
  puts "Scraping list..."
  html = ScraperWiki::scrape(BASE_URL + "suche.php?action=result&searchid=3&adressliste=1&sid=a038ef957d79aaff6845688e2e87a284")
  doc = Nokogiri::HTML(html)
  
  doc.search("table[border='1'] tr:not(.rubrikheadline2)").each do |row|
    cells = row.search('td')
    
    unless ScraperWiki.get_var(cells[0].search('a').first.attr :href) # If we find it then it's already been scraped, in which case no need to scrape it again.
      details_link = cells[0].search('a').first.attr :href
      partner = cells[1].text.strip unless cells[1].text.strip == '-' # In the raw data, an empty field is sometimes denoted by a "-" character (at other times the field is just left blank).
      street = cells[2].text.strip unless cells[2].text.strip == '-'
      plz = cells[3].text.strip unless cells[3].text.strip == '-'
      tel = cells[4].text.strip.gsub(' ', '') unless cells[4].text.strip.gsub(' ', '') == '-' # It would be nice to tidy this up more, but some characters are used inconsistently in the data
      fax = cells[5].text.strip.gsub(' ', '') unless cells[5].text.strip.gsub(' ', '') == '-' # It would be nice to tidy this up more, but some characters are used inconsistently in the data
      email = cells[6].text.strip unless cells[6].text.strip == '-'

      data = {
        'Name' => cells[0].text.strip,
        'Ansprechpartner in' => partner,
        'Strasse' => street,
        'PLZ Ort' => plz,
        'Tel' => tel,
        'Fax' => fax,
        'eMail' => email,
        'detailslink' => details_link
      }
      data.merge! scrape_details_link(details_link)
      ScraperWiki::save_sqlite ['Name'], data, 'projects'
      ScraperWiki.save_var(details_link, true)
    end
  end
end

def scrape_details_link(url)  
    # puts "Scraping #{url}..."
    html = ScraperWiki::scrape(BASE_URL + url)
    doc = Nokogiri::HTML(html)
    
    project = doc.search('//td[@width="70%"]/p[@class="space"]/b').first
    internet = doc.search('//td[@valign="top" and text()="Internet:"]/following-sibling::td/a').first
    project_text = project.text.strip unless project.nil? 
    internet_text = internet.text.strip unless internet.nil? 
    
    {'Eines unserer Projekte' => project_text, 'Internet' => internet_text}
end

scrape_list


  
    
  
  

require 'nokogiri'

BASE_URL = "https://good-practice.bibb.de/adb/"

def scrape_list
  puts "Scraping list..."
  html = ScraperWiki::scrape(BASE_URL + "suche.php?action=result&searchid=3&adressliste=1&sid=a038ef957d79aaff6845688e2e87a284")
  doc = Nokogiri::HTML(html)
  
  doc.search("table[border='1'] tr:not(.rubrikheadline2)").each do |row|
    cells = row.search('td')
    
    unless ScraperWiki.get_var(cells[0].search('a').first.attr :href) # If we find it then it's already been scraped, in which case no need to scrape it again.
      details_link = cells[0].search('a').first.attr :href
      partner = cells[1].text.strip unless cells[1].text.strip == '-' # In the raw data, an empty field is sometimes denoted by a "-" character (at other times the field is just left blank).
      street = cells[2].text.strip unless cells[2].text.strip == '-'
      plz = cells[3].text.strip unless cells[3].text.strip == '-'
      tel = cells[4].text.strip.gsub(' ', '') unless cells[4].text.strip.gsub(' ', '') == '-' # It would be nice to tidy this up more, but some characters are used inconsistently in the data
      fax = cells[5].text.strip.gsub(' ', '') unless cells[5].text.strip.gsub(' ', '') == '-' # It would be nice to tidy this up more, but some characters are used inconsistently in the data
      email = cells[6].text.strip unless cells[6].text.strip == '-'

      data = {
        'Name' => cells[0].text.strip,
        'Ansprechpartner in' => partner,
        'Strasse' => street,
        'PLZ Ort' => plz,
        'Tel' => tel,
        'Fax' => fax,
        'eMail' => email,
        'detailslink' => details_link
      }
      data.merge! scrape_details_link(details_link)
      ScraperWiki::save_sqlite ['Name'], data, 'projects'
      ScraperWiki.save_var(details_link, true)
    end
  end
end

def scrape_details_link(url)  
    # puts "Scraping #{url}..."
    html = ScraperWiki::scrape(BASE_URL + url)
    doc = Nokogiri::HTML(html)
    
    project = doc.search('//td[@width="70%"]/p[@class="space"]/b').first
    internet = doc.search('//td[@valign="top" and text()="Internet:"]/following-sibling::td/a').first
    project_text = project.text.strip unless project.nil? 
    internet_text = internet.text.strip unless internet.nil? 
    
    {'Eines unserer Projekte' => project_text, 'Internet' => internet_text}
end

scrape_list


  
    
  
  

