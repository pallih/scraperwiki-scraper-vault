require 'mechanize'


@br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
end
page = @br.get("http://www.13lignes.be")


data_list = []

i = 0
page.parser.xpath("//h2[@class='date-header']/span").each { |item|   data_list[i] ||= {'idx' => i}; data_list[i]['datestr'] = item.text; i+=1; }

i = 0
page.parser.xpath("//h3[@class='post-title entry-title']/a").each { |item|   data_list[i] ||= {'idx' => i}; data_list[i]['title'] = item.text; i+=1; }

i = 0
page.parser.xpath("//div[@class='post-body entry-content']").each { |item|   data_list[i] ||= {'idx' => i}; data_list[i]['content'] = item.text.gsub!(/\n/, " "); i+=1; }


data_list.each do |data|
  ScraperWiki.save_sqlite(unique_keys=["idx"], data=data)
end


