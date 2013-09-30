require 'nokogiri'
require 'iconv'

# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Name', 'Text'])

#html = open("index.shtml").read
#puts html

html = ScraperWiki.scrape("http://www.hrad.cz/cs/prezident-cr/rozhodnuti-prezidenta/amnestie-a-milosti/index.shtml")

def is_title?(element)
  if css_class = element.attributes["class"]
    css_class.value.split(" ").member?("title")
  else
    false
  end
end

doc = Nokogiri::HTML(html)
amnesties = doc.at("div#amnesties-index")
amnesties.search('p').each do |p|
  if is_title?(p)
    @amnesty_date = Date.parse(Iconv.iconv('ascii//translit', 'utf-8', p.text).to_s)
    puts @amnesty_date
  else
    strong = p.at("strong")
    if strong
      name = strong.text
      value = p.text
      record = {"Name"=>name, "Text"=> Iconv.iconv('ascii//translit', 'utf-8', value), 'date' => @amnesty_date}
      ScraperWiki.save(['date','Name'], record)
#      puts record.inspect
    end
  end
end
require 'nokogiri'
require 'iconv'

# define the order our columns are displayed in the datastore
ScraperWiki.save_metadata('data_columns', ['Name', 'Text'])

#html = open("index.shtml").read
#puts html

html = ScraperWiki.scrape("http://www.hrad.cz/cs/prezident-cr/rozhodnuti-prezidenta/amnestie-a-milosti/index.shtml")

def is_title?(element)
  if css_class = element.attributes["class"]
    css_class.value.split(" ").member?("title")
  else
    false
  end
end

doc = Nokogiri::HTML(html)
amnesties = doc.at("div#amnesties-index")
amnesties.search('p').each do |p|
  if is_title?(p)
    @amnesty_date = Date.parse(Iconv.iconv('ascii//translit', 'utf-8', p.text).to_s)
    puts @amnesty_date
  else
    strong = p.at("strong")
    if strong
      name = strong.text
      value = p.text
      record = {"Name"=>name, "Text"=> Iconv.iconv('ascii//translit', 'utf-8', value), 'date' => @amnesty_date}
      ScraperWiki.save(['date','Name'], record)
#      puts record.inspect
    end
  end
end
