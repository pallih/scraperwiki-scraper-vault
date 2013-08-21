require 'nokogiri'

def get_data url, tries=0
  max = 5

  begin
    return ScraperWiki.scrape(url)
  rescue
    if tries >= max
      raise "error retrieving data"
    else
      tries += 1
      sleep(1)
      get_data(url, tries)
    end
  end
end


#setup the tables
if ScraperWiki.table_info(name="missing") == []
  ScraperWiki.sqliteexecute("create table missing (`series` string, `volume` string, `expected_filename` string)")
  ScraperWiki.sqliteexecute("create table incomplete (`series` string, `volume` string, `status` string, `url` string)")
end

pages = [
  {:title => "First Series", :prefix => 'S1', :url => "http://hansard.millbanksystems.com/volumes/1"},
  {:title => "Second Series", :prefix => 'S2', :url => "http://hansard.millbanksystems.com/volumes/2"},
  {:title => "Third Series", :prefix => 'S3', :url => "http://hansard.millbanksystems.com/volumes/3"},
  {:title => "Fourth Series", :prefix => 'S4', :url => "http://hansard.millbanksystems.com/volumes/4"},
  {:title => "Fifth Series (Commons)", :prefix => 'S5C', :url => "http://hansard.millbanksystems.com/volumes/5C"},
  {:title => "Fifth Series (Lords)", :prefix => 'S5L', :url => "http://hansard.millbanksystems.com/volumes/5L"},
  {:title => "Sixth Series (Commons)", :prefix => 'S6C', :url => "http://hansard.millbanksystems.com/volumes/6C"}
]

pages.each do |page|
  html = get_data(page[:url])

  doc = Nokogiri::HTML(html)
  table = doc.xpath('//table["class=volumes"]/thead')
  table.xpath('//tr').each do |row|
    if row.xpath('td/text()')[4]
      loaded = row.xpath('td/text()')[4].to_s.strip
      unless loaded == "100%"
        if loaded == "—"
          title = row.xpath('td/text()')[0].to_s.strip
          puts "#{page[:title]}: #{title}: Missing Volume"


          volume = "0000" + title.strip.split(" ")[1]
          volume = volume[volume.length-4..volume.length] 

          filename = page[:prefix] + 'V' + volume + "P0"

          record = {'series' => page[:title], 'volume' => title, 'expected_filename' => filename}
          ScraperWiki.save_sqlite(['series','volume'], record, "missing")
        else
          title = row.xpath('td/a/text()')[0].to_s.strip
          link = row.xpath('td/a').attr('href')
          puts "#{page[:title]}: #{title}: #{loaded} loaded"
         
          record = {'series' => page[:title], 'volume' => title, 'status' => "#{loaded} loaded", 'url' => link}
          ScraperWiki.save_sqlite(['series', 'volume'], record, "incomplete")
        end
      end
    end
  end
end