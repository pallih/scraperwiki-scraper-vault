require "nokogiri"


(5..5).each do |id|
  url = "http://www.deinbus.de/fs/result/?bus_von=#{id}&bus_nach=7&passengers=1"
  page = Nokogiri::HTML(ScraperWiki.scrape url)
  places = page.search(".bare-list li")
  name = places[0].text.split(':')[1].strip
  if name != ""
    city = {'unique' => 'orig'+name, 'id' => id, 'type' => 'orig', 'name' => name}
    puts "#{city['name']} has ID #{city['id']}"
    ScraperWiki.save_sqlite(unique_keys=['unique'], data=city)
  end
end

(5..440).each do |id|
  url = "http://www.deinbus.de/fs/result/?bus_von=9&bus_nach=#{id}&passengers=1"
  page = nil
  begin
    page = Nokogiri::HTML(ScraperWiki.scrape url)
  rescue
    puts "KOMPOST! retry.."
    retry
  end
  places = page.search(".bare-list li")
  name = places[1].text.split(':')[1].strip
  if name != ""
    city = {'unique' => 'dest'+name, 'id' => id, 'type' => 'dest', 'name' => name}
    puts "#{city['name']} has ID #{city['id']}"
    ScraperWiki.save_sqlite(unique_keys=['unique'], data=city)
  end
end

require "nokogiri"


(5..5).each do |id|
  url = "http://www.deinbus.de/fs/result/?bus_von=#{id}&bus_nach=7&passengers=1"
  page = Nokogiri::HTML(ScraperWiki.scrape url)
  places = page.search(".bare-list li")
  name = places[0].text.split(':')[1].strip
  if name != ""
    city = {'unique' => 'orig'+name, 'id' => id, 'type' => 'orig', 'name' => name}
    puts "#{city['name']} has ID #{city['id']}"
    ScraperWiki.save_sqlite(unique_keys=['unique'], data=city)
  end
end

(5..440).each do |id|
  url = "http://www.deinbus.de/fs/result/?bus_von=9&bus_nach=#{id}&passengers=1"
  page = nil
  begin
    page = Nokogiri::HTML(ScraperWiki.scrape url)
  rescue
    puts "KOMPOST! retry.."
    retry
  end
  places = page.search(".bare-list li")
  name = places[1].text.split(':')[1].strip
  if name != ""
    city = {'unique' => 'dest'+name, 'id' => id, 'type' => 'dest', 'name' => name}
    puts "#{city['name']} has ID #{city['id']}"
    ScraperWiki.save_sqlite(unique_keys=['unique'], data=city)
  end
end

