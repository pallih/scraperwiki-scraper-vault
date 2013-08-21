require 'nokogiri'

def main
  doc = Nokogiri::HTML(ScraperWiki::scrape('http://www.regjeringen.no/nb/tema_a-aa.html?id=223486'))

  doc.css('.subjectIndex li').each do |li|
    if "a" == li.first_element_child().name.downcase() then
      li.first_element_child()['href'] =~ /id=(\d+)$/
      data = ['url' => 'http://www.regjeringen.no/' + li.first_element_child()['href'],
              'topic' => li.first_element_child().inner_text,
              'id' => $1,
              'scrapestamputc' => DateTime.now]
      
     ScraperWiki::save_sqlite(["id"], data)
    end
  end
end

main