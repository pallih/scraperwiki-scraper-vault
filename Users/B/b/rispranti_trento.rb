###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.2spaghi.it/ristoranti/trentino-alto-adige/tn/trento/'
DOMAIN = 'http://www.2spaghi.it'
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



def scrape_one_restaurant(url)
  record = {}
  record[:Link] = url
  page = Nokogiri::HTML(open(url))
  record[:Name] = page.at_css("div.headProfile h1.item").inner_text.strip if page.at_css("div.headProfile h1.item")
  record[:Subtypes] = page.at_css("div.categories").content.strip[10..-1].strip if page.at_css("div.categories")
  if page.at_css("span.locality")
    record[:Votes] = page.at_css("big.votes") ? page.at_css("big.votes").content.to_i : 0
  else
    record[:Votes] = 0 
  end
  record[:Comments] = page.at_css("big.count").content.to_i if page.at_css("big.count")
  if (record[:Votes] >0 && page.at_css("p.rankLoc span.average"))
    record[:AvgVote] = page.at_css("p.rankLoc span.average").content.strip.to_i
  else
    record[:AvgVote] = 0
  end
  record[:street_address] = page.at_css("span.street-address").content.strip if page.at_css("span.street-address")
  record[:postal_code] = page.at_css("span.postal-code").content.strip if page.at_css("span.postal-code")
  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
  record[:locality] = page.at_css("span.locality").content.strip if page.at_css("span.locality")
  record[:country] = page.at_css("span.country-name").content.strip if page.at_css("span.country-name")
  record[:phone] = page.at_css("span.tel").content.strip.gsub(/[\/.,-]/, " ") if page.at_css("span.tel")

  add_aperture(page, record)
  add_coords(page, record)
  ScraperWiki.save_sqlite(unique_keys=[:Link], data=record)  
  
end

def add_aperture(page, record)
  if( ! page.css("table.timetable") )
    return record; 
  end
  record[:lun_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[1].css("p").first["title"]
  record[:mar_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[2].css("p").first["title"]
  record[:mer_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[3].css("p").first["title"]
  record[:gio_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[4].css("p").first["title"]
  record[:ven_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[5].css("p").first["title"]
  record[:sab_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[6].css("p").first["title"]
  record[:dom_pranzo] = page.css("table.timetable").css("tr")[1].css("td")[7].css("p").first["title"]
  record[:lun_cena] = page.css("table.timetable").css("tr")[2].css("td")[1].css("p").first["title"]
  record[:mar_cena] = page.css("table.timetable").css("tr")[2].css("td")[2].css("p").first["title"]
  record[:mer_cena] = page.css("table.timetable").css("tr")[2].css("td")[3].css("p").first["title"]
  record[:gio_cena] = page.css("table.timetable").css("tr")[2].css("td")[4].css("p").first["title"]
  record[:ven_cena] = page.css("table.timetable").css("tr")[2].css("td")[5].css("p").first["title"]
  record[:sab_cena] = page.css("table.timetable").css("tr")[2].css("td")[6].css("p").first["title"]
  record[:dom_cena] = page.css("table.timetable").css("tr")[2].css("td")[7].css("p").first["title"]
  return record
end

def add_coords(page, record)
  for script in page.css('script')
    if script.inner_text.include? "mArray.push('"
      latlon = script.inner_text[/\d{2}[.]\d{2,16}[;]\d{2}[.]\d{2,16}/].split(";") if script.inner_text[/\d{2}[.]\d{2,16}[;]\d{2}[.]\d{2,16}/]
      record[:latitude] = latlon[0] if latlon
      record[:longitude] = latlon[1] if latlon
    end       
  end
  puts record
  return record
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
#scrape_one_restaurant("http://www.2spaghi.it/ristoranti/trentino-alto-adige/tn/trento/mas-dela-fam/")

starting_url = BASE_URL
scrape_and_look_for_next_link(starting_url)
puts "urls acquired, starting to scrape individual restaurants..."
res=ScraperWiki.sqliteexecute("select Link from swdata")
res["data"].each do |x|
  puts "starting to scrape " + x[0]
  scrape_one_restaurant(x[0])
  puts "finished scraping restaurant..."
end

