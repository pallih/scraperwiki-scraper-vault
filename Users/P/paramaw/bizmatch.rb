require 'nokogiri'    

base_url = 'http://www.bizmatch.ca/'
html = ScraperWiki.scrape("#{base_url}business_for_sale.php?&keyword=&location=ON&cat=0&show=&cpage=1")           
puts html

#div[@align='left']

doc = Nokogiri::HTML(html)
list = []
i = 0
for v in doc.search("div#page-bgbtm div#content > table[@cellpadding!='2']")
  puts i+=1
  cells = v.search('tr>td>table>tr')
  relative_url = cells[1].search('td>span>a').first['href']

  data = {
    'listing_id' => relative_url.gsub('business_details.php?LID=','').to_i,
    'url' => "#{base_url}#{relative_url}",
    'image' => cells[0].search('td>a>img'),
    'title' => cells[1].search('td>span>a').text.strip,
    'location' => cells[2].search('td').text.gsub(/Located in\s*/i,'').strip,
    'asking_price' => cells[3].search('td').text.gsub(/Asking price is\s*/i,'').gsub(/\s*/,''),
    'description' => cells[4].search('td').text.strip    
  }
 
  #puts data['image']
  #puts data.to_json
  #puts '-----------------'
  ScraperWiki.save_sqlite(unique_keys=['listing_id'], data=data)   
  list << data
end
#puts list[0]['id']#
#puts list[0]['url']

#https://scraperwiki.com/docs/ruby/ruby_intro_tutorial/
