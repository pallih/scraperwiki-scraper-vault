# coding: utf-8
require 'open-uri'
require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

BASE_URL = 'http://www.ville.sherbrooke.qc.ca/'
SOURCE_URL = 'http://www.ville.sherbrooke.qc.ca/mairie-et-vie-democratique/conseil-municipal/elus-municipaux/'
doc = Nokogiri::HTML(open(SOURCE_URL))
data = {
      'name' => '',
      'district_name' => '',
      'elected_office' => '',
      'email' => '', 
      'source_url' => ''
    }
# Parse the table of link and open each link, Nicole Bergeron has a different page architecture.
doc.css("div.generic-content a").each do |a|
    personalUrl = BASE_URL + a['href']
    personalInfo = Nokogiri::HTML(open(personalUrl))
    
    name = personalInfo.css("div.generic-content h3").text
    lastName = name.split(',')[0]
    firstName = name.split(',')[1]
    name = firstName + ' ' + lastName
    
    if(personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child a").text.length > 0) # For Nicole Bergeron
      districtName = personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child a").text
    else
      districtName = personalInfo.css("div[id*=c16] div:first-child div:nth-child(2) ul:first-child a").text
    end
    districtName = districtName.split('(')[0]

    electedOffice = personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child li:nth-child(1)").text.split(',')[0]
    
    if(personalInfo.css("div[id*=c16] ul:last-child li a")[0] != nil)

      if personalInfo.css("div[id=c1634]")[0] != nil # For Nicole Bergeron
        email = personalInfo.css("div[id=c1634] > ul:last-child li a")[0]['href']
      else
        email = personalInfo.css("div[id*=c16] ul:last-child li a")[0]['href']
      end

      if personalInfo.css("div[id=c1652]")[0] != nil # For Julien Lachance
        email.slice!("mailto:Courriel%20:%20") 
      else
        email.slice!("mailto:") 
      end    
    end
    
    data['name'] = name
    data['district_name'] = districtName
    data['elected_office'] = electedOffice
    data['source_url'] = personalUrl
    data['email'] = email

    ScraperWiki.save_sqlite(['name'], data)  
end
# coding: utf-8
require 'open-uri'
require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

BASE_URL = 'http://www.ville.sherbrooke.qc.ca/'
SOURCE_URL = 'http://www.ville.sherbrooke.qc.ca/mairie-et-vie-democratique/conseil-municipal/elus-municipaux/'
doc = Nokogiri::HTML(open(SOURCE_URL))
data = {
      'name' => '',
      'district_name' => '',
      'elected_office' => '',
      'email' => '', 
      'source_url' => ''
    }
# Parse the table of link and open each link, Nicole Bergeron has a different page architecture.
doc.css("div.generic-content a").each do |a|
    personalUrl = BASE_URL + a['href']
    personalInfo = Nokogiri::HTML(open(personalUrl))
    
    name = personalInfo.css("div.generic-content h3").text
    lastName = name.split(',')[0]
    firstName = name.split(',')[1]
    name = firstName + ' ' + lastName
    
    if(personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child a").text.length > 0) # For Nicole Bergeron
      districtName = personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child a").text
    else
      districtName = personalInfo.css("div[id*=c16] div:first-child div:nth-child(2) ul:first-child a").text
    end
    districtName = districtName.split('(')[0]

    electedOffice = personalInfo.css("div[id*=c16] div#conseiller-fiche ul:first-child li:nth-child(1)").text.split(',')[0]
    
    if(personalInfo.css("div[id*=c16] ul:last-child li a")[0] != nil)

      if personalInfo.css("div[id=c1634]")[0] != nil # For Nicole Bergeron
        email = personalInfo.css("div[id=c1634] > ul:last-child li a")[0]['href']
      else
        email = personalInfo.css("div[id*=c16] ul:last-child li a")[0]['href']
      end

      if personalInfo.css("div[id=c1652]")[0] != nil # For Julien Lachance
        email.slice!("mailto:Courriel%20:%20") 
      else
        email.slice!("mailto:") 
      end    
    end
    
    data['name'] = name
    data['district_name'] = districtName
    data['elected_office'] = electedOffice
    data['source_url'] = personalUrl
    data['email'] = email

    ScraperWiki.save_sqlite(['name'], data)  
end
