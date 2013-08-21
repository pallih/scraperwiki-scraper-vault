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
  ScraperWiki.sqliteexecute("create table missing (`series` string, `volume` string)")
  ScraperWiki.sqliteexecute("create table incomplete (`series` string, `volume` string, `status` string, `url` string)")
end

pages = [
  {:title => "1st", :url => "http://hansard.millbanksystems.com/volumes/1"},
  {:title => "2nd", :url => "http://hansard.millbanksystems.com/volumes/2"},
  {:title => "3rd", :url => "http://hansard.millbanksystems.com/volumes/3"},
  {:title => "4th", :url => "http://hansard.millbanksystems.com/volumes/4"},
  {:title => "5th [HC]", :url => "http://hansard.millbanksystems.com/volumes/5C"},
  {:title => "5th [HL]", :url => "http://hansard.millbanksystems.com/volumes/5L"},
  {:title => "6th [HC]", :url => "http://hansard.millbanksystems.com/volumes/6C"}
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
          puts "#{page[:title]} Series, #{title}, NOT FOUND"

          record = {'series' => page[:title], 'volume' => title}
          ScraperWiki.save_sqlite(['series','volume'], record, "not-found")
        elsif loaded == "0%"
          title = row.xpath('td/text()')[0].to_s.strip
          puts "#{page[:title]} Series, #{title}, NOT LOADED"

          record = {'series' => page[:title], 'volume' => title}
          ScraperWiki.save_sqlite(['series','volume'], record, "not-loaded")
        else
          title = row.xpath('td/a/text()')[0].to_s.strip
          link = row.xpath('td/a').attr('href')
          puts "#{page[:title]} #{title}: #{loaded} loaded"
          
          record = {'series' => page[:title], 'volume' => title, 'status' => "#{loaded} loaded", 'url' => link}
          ScraperWiki.save_sqlite(['series', 'volume'], record, "incomplete")
        end
      end
    end
  end
end