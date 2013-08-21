require 'nokogiri'
require 'open-uri'

url = "http://salvosstores.salvos.org.au/find-a-store/"

#html = ScraperWiki.scrape()
#puts html
def extract_name(cell)
  cell.xpath("./strong/a/span[@class='name']").inner_html
end

def extract_address(cell)
  cell.search('p').map {|a| a.inner_html.force_encoding('ASCII-8BIT').gsub('<br>', ', ').gsub("\x92", '').strip }.first
end

def extract_phone(cell)
  cell.inner_html.split('<br>').first.gsub('Ph ','').gsub("(",'').gsub(")",'').strip
end

def extract_fax(cell)
  fax = cell.inner_html.split('<br>').select {|r| r =~ /Fax/ }.first || ""
  fax.gsub('Fax ','').gsub("(",'').gsub(")",'').strip
end

def extract_hours(cell)
  cell.inner_html.split('<br>').join(', ')
end

def extract_lat_lng(cell)
  onclick = cell.search('a').attr('onclick').value
  onclick.gsub("display_store_on_map(","").gsub(");","").split(",")
end

doc = Nokogiri::HTML(open(url))
doc.xpath("//table[@class='area-list']//tr").each do |store|
  cells = store.search('td')
  if cells.count==3
    address = extract_address(cells[0])
    name = extract_name(cells[0])

    phone = extract_phone(cells[1])
    fax = extract_fax(cells[1])
    hours = extract_hours(cells[2])
    shop_id, lat, lng = extract_lat_lng(cells[0])
    if address
      data = {
        'salvos_shop_id' => shop_id,
        'name' => name,
        'address' => address,
        'phone' => phone,
        'fax' => fax,
        'hours' => hours,
        'lat' => lat,
        'lng' => lng
      }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['salvos_shop_id'], data=data)
    end
  end
end