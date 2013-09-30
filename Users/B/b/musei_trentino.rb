###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.visittrentino.it/it/cosa_fare/da_vedere/risultati?st=Arte+e+Cultura&stt=Musei&daVedereType=daVedere.categoria.0&daVedereSubType=daVedere.arteCultura.categorieRicerca.1'
DOMAIN = 'http://www.visittrentino.it'

# define the order our columns are displayed in the datastore
#ScraperWiki.save_var('data_columns', ['Name', 'Link'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('div.boxListResult').each do |x|
    record = {}
    record[:Link]    = DOMAIN + x.css("div.contInfo h3 a").at_css("a")["href"]
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save_sqlite(unique_keys=[:Link], data=record)
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    if page.css("p.stdPager a").last.content.include? "Succ"
      next_link = page.css("p.stdPager a").last["href"]
    end
    if next_link 
      puts "next link= " + next_link
      next_url = DOMAIN + next_link
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

def ctext(el)           
  if el.text? 
    #puts "text found: "+ el.text
    return el.text.gsub! /\t/, ''
  end
  result = [ ]
  for sel in el.children
    if (!["text", "a", "br", "b", "i"].include?(sel.name))
      raise "disallowed tag: " + sel.name
    end
    if sel.element? 
      #puts "is element "+sel.name
      result.push("<"+sel.name+">")
    end
    result.push(ctext(sel))
    if sel.element? 
      result.push("</"+sel.name+">")
    end
  end
  return result unless result.empty? 
end

def scrape_one_item(url)
  record = {}
  record[:Url] = url
  page = Nokogiri::HTML(open(url))
  record[:Nome] = 
    page.xpath(".//*[@id='portlet-wrapper-ContentPortlet_1_WAR_alfrescoPortletGeneric']/div/div/div/h1/text()").to_s 
  adrarr = page.at_css("div.descrizione").to_s.gsub(/<\/?[^>]*>/, "").strip!.split("\t")
  #puts adrarr.inspect
  record[:Indirizzo] = adrarr[0]+adrarr[1] unless (adrarr[0].start_with?("Tel:") or adrarr[0].start_with?("Email:"))
  record[:Tel] = Array.new
  for e in adrarr do
    if e.start_with?("Tel:")
      record[:Tel] << e.gsub(/[^0-9\+]/, "")
    end
    if e.start_with?("E-mail:")
      record[:Email] = e.slice(7..e.length).strip!
    end 
  end
  
  if (page.at_css("div.elenco_freccia").children.at_css("a").content.to_s.start_with?("www"))
    puts page.at_css("div.elenco_freccia").children.at_css("a").attribute("href")  
  end
  puts page.xpath(".//*[@id='portlet-wrapper-ContentPortlet_1_WAR_alfrescoPortletGeneric']/div/div/div/div[3]").inner_text
  #puts record[:Indirizzo] = adrblock[0]+adrblock[2]
  #puts adrblock[4]
  #record[:Telefono] = adrblock[4].gsub(/[^0-9\+]/, "")
  
  
#  record[:Name] = page.at_css("div.headProfile h1.item").inner_text.strip if page.at_css("div.headProfile h1.item")
#  record[:Subtypes] = page.at_css("div.categories").content.strip[10..-1].strip if page.at_css("div.categories")
#  if page.at_css("span.locality")
#    record[:Votes] = page.at_css("big.votes").content.to_i
#  else
#    record[:Votes] = 0 
#  end
#  record[:Comments] = page.at_css("big.count").content.to_i if page.at_css("big.count")
#  if (record[:Votes] >0 && page.at_css("p.rankLoc span.average"))
#    record[:AvgVote] = page.at_css("p.rankLoc span.average").content.strip.to_i
#  else
#    record[:AvgVote] = 0
#  end
#  record[:street_address] = page.at_css("span.street-address").content.strip if page.at_css("span.street-address")
#  record[:postal_code] = page.at_css("span.postal-code").content.strip if page.at_css("span.postal-code")
#  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
#  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
#  record[:country] = page.at_css("span.country-name").content.strip if page.at_css("span.country-name")
#  record[:phone] = page.at_css("span.tel").content.strip.gsub(/[\/.,-]/, " ") if page.at_css("span.tel")
#
#  add_aperture(page, record)
#  add_coords(page, record)
#  ScraperWiki.save_sqlite(unique_keys=[:Link], data=record)  
puts record
  
end


# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#

starting_url = BASE_URL
#scrape_and_look_for_next_link(starting_url)
#puts "urls acquired, starting to scrape individual restaurants..."
#res=ScraperWiki.sqliteexecute("select Link from swdata")
#res["data"].each do |x|
#  puts "starting to scrape " + x[0]
#  scrape_one_restaurant(x[0])
#  puts "finished scraping restaurant..."
#end

#scrape_one_item("http://www.visittrentino.it/it/cosa_fare/da_vedere/dettagli/dett/museo-della-guerra-bianca-spiazzo")
#scrape_one_item("http://www.visittrentino.it/it/cosa_fare/da_vedere/dettagli/dett/sul-fronte-dei-ricordi")



page = Nokogiri::HTML(open("http://www.visittrentino.it/it/cosa_fare/da_vedere/risultati?st=Arte+e+Cultura&stt=Musei&daVedereType=daVedere.categoria.0&daVedereSubType=daVedere.arteCultura.categorieRicerca.1"))
i=0
for el in page.css(".tab_colonna_centrale_int>p").children do
  #puts "START tab_colonna_centrale_int"
  if (el.name == "text")
    if (!el.previous)
      puts "Element: "+el.text+el.text.length.to_s unless (el.text.include?("Caratteristiche:") or el.text.length==0)
      i+=1 unless (el.text.include?("Caratteristiche:") or el.text.length==0)
    end
  end
  #puts "END tab_colonna_centrale_int"
end
puts i###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.visittrentino.it/it/cosa_fare/da_vedere/risultati?st=Arte+e+Cultura&stt=Musei&daVedereType=daVedere.categoria.0&daVedereSubType=daVedere.arteCultura.categorieRicerca.1'
DOMAIN = 'http://www.visittrentino.it'

# define the order our columns are displayed in the datastore
#ScraperWiki.save_var('data_columns', ['Name', 'Link'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(page)
  data_table = page.css('div.boxListResult').each do |x|
    record = {}
    record[:Link]    = DOMAIN + x.css("div.contInfo h3 a").at_css("a")["href"]
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save_sqlite(unique_keys=[:Link], data=record)
  end
end

#        scrape_and_look_for_next_link(starting_url)

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    scrape_table(page)
    if page.css("p.stdPager a").last.content.include? "Succ"
      next_link = page.css("p.stdPager a").last["href"]
    end
    if next_link 
      puts "next link= " + next_link
      next_url = DOMAIN + next_link
      puts next_url
      scrape_and_look_for_next_link(next_url)
    end
end

def ctext(el)           
  if el.text? 
    #puts "text found: "+ el.text
    return el.text.gsub! /\t/, ''
  end
  result = [ ]
  for sel in el.children
    if (!["text", "a", "br", "b", "i"].include?(sel.name))
      raise "disallowed tag: " + sel.name
    end
    if sel.element? 
      #puts "is element "+sel.name
      result.push("<"+sel.name+">")
    end
    result.push(ctext(sel))
    if sel.element? 
      result.push("</"+sel.name+">")
    end
  end
  return result unless result.empty? 
end

def scrape_one_item(url)
  record = {}
  record[:Url] = url
  page = Nokogiri::HTML(open(url))
  record[:Nome] = 
    page.xpath(".//*[@id='portlet-wrapper-ContentPortlet_1_WAR_alfrescoPortletGeneric']/div/div/div/h1/text()").to_s 
  adrarr = page.at_css("div.descrizione").to_s.gsub(/<\/?[^>]*>/, "").strip!.split("\t")
  #puts adrarr.inspect
  record[:Indirizzo] = adrarr[0]+adrarr[1] unless (adrarr[0].start_with?("Tel:") or adrarr[0].start_with?("Email:"))
  record[:Tel] = Array.new
  for e in adrarr do
    if e.start_with?("Tel:")
      record[:Tel] << e.gsub(/[^0-9\+]/, "")
    end
    if e.start_with?("E-mail:")
      record[:Email] = e.slice(7..e.length).strip!
    end 
  end
  
  if (page.at_css("div.elenco_freccia").children.at_css("a").content.to_s.start_with?("www"))
    puts page.at_css("div.elenco_freccia").children.at_css("a").attribute("href")  
  end
  puts page.xpath(".//*[@id='portlet-wrapper-ContentPortlet_1_WAR_alfrescoPortletGeneric']/div/div/div/div[3]").inner_text
  #puts record[:Indirizzo] = adrblock[0]+adrblock[2]
  #puts adrblock[4]
  #record[:Telefono] = adrblock[4].gsub(/[^0-9\+]/, "")
  
  
#  record[:Name] = page.at_css("div.headProfile h1.item").inner_text.strip if page.at_css("div.headProfile h1.item")
#  record[:Subtypes] = page.at_css("div.categories").content.strip[10..-1].strip if page.at_css("div.categories")
#  if page.at_css("span.locality")
#    record[:Votes] = page.at_css("big.votes").content.to_i
#  else
#    record[:Votes] = 0 
#  end
#  record[:Comments] = page.at_css("big.count").content.to_i if page.at_css("big.count")
#  if (record[:Votes] >0 && page.at_css("p.rankLoc span.average"))
#    record[:AvgVote] = page.at_css("p.rankLoc span.average").content.strip.to_i
#  else
#    record[:AvgVote] = 0
#  end
#  record[:street_address] = page.at_css("span.street-address").content.strip if page.at_css("span.street-address")
#  record[:postal_code] = page.at_css("span.postal-code").content.strip if page.at_css("span.postal-code")
#  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
#  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
#  record[:country] = page.at_css("span.country-name").content.strip if page.at_css("span.country-name")
#  record[:phone] = page.at_css("span.tel").content.strip.gsub(/[\/.,-]/, " ") if page.at_css("span.tel")
#
#  add_aperture(page, record)
#  add_coords(page, record)
#  ScraperWiki.save_sqlite(unique_keys=[:Link], data=record)  
puts record
  
end


# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#

starting_url = BASE_URL
#scrape_and_look_for_next_link(starting_url)
#puts "urls acquired, starting to scrape individual restaurants..."
#res=ScraperWiki.sqliteexecute("select Link from swdata")
#res["data"].each do |x|
#  puts "starting to scrape " + x[0]
#  scrape_one_restaurant(x[0])
#  puts "finished scraping restaurant..."
#end

#scrape_one_item("http://www.visittrentino.it/it/cosa_fare/da_vedere/dettagli/dett/museo-della-guerra-bianca-spiazzo")
#scrape_one_item("http://www.visittrentino.it/it/cosa_fare/da_vedere/dettagli/dett/sul-fronte-dei-ricordi")



page = Nokogiri::HTML(open("http://www.visittrentino.it/it/cosa_fare/da_vedere/risultati?st=Arte+e+Cultura&stt=Musei&daVedereType=daVedere.categoria.0&daVedereSubType=daVedere.arteCultura.categorieRicerca.1"))
i=0
for el in page.css(".tab_colonna_centrale_int>p").children do
  #puts "START tab_colonna_centrale_int"
  if (el.name == "text")
    if (!el.previous)
      puts "Element: "+el.text+el.text.length.to_s unless (el.text.include?("Caratteristiche:") or el.text.length==0)
      i+=1 unless (el.text.include?("Caratteristiche:") or el.text.length==0)
    end
  end
  #puts "END tab_colonna_centrale_int"
end
puts i