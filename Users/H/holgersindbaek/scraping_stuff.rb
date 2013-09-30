#require 'open-uri'

=begin scraping scoutzie
  $i = 0;
  $num = 23;

  until $i == $num  do
    $i = $i+1
    p $i
    doc = Nokogiri::HTML(open('http://www.scoutzie.com/designers?page='+$i.to_s))

    doc.css('.designer_block>a').each do |links|
      designer_site = Nokogiri::HTML(open('http://www.scoutzie.com'+links['href']))
      designer_site.css("#contact_designer_twitter").each do |designer|
        p designer.content
      end
    end
  end
=end

$i = 1;
$n = 29;
require 'nokogiri'
price = []
sales = []

until $i == $n  do
  $i = $i+1
  p $i
  html = ScraperWiki::scrape("http://themeforest.net/category/wordpress/creative?page="+$i.to_s)
  doc = Nokogiri::HTML html

  doc.css('.price').each do |amount|
    p amount.content.gsub("$","").to_i
    price << amount.content.gsub("$","").to_i
  end

  doc.css('.sale-count').each do |amount|
    p amount.content.gsub(" Sales","").to_i
    sales << amount.content.gsub("$","").to_i
  end
end
p price
p salesrequire 'nokogiri'
require 'json'
require 'open-uri'

json_hash = { chapters: [] }

for i in 2..114 do
  p i 
  doc = Nokogiri::HTML open("http://www.clearquran.com/quran-chapter-#{i.to_s.rjust(3, '0')}.html")

  json_hash[:chapters].push({ title: "", verses: [] })

  verse_hash = json_hash[:chapters][i-2]
  verse_hash[:title] = doc.at_css('p#chNameEn').text
  
  doc.css('#quran-text > p').each_with_index do |child, i|
    next if i==0
    verse_hash[:verses].push( child.children.last.text )
  end  
end

print JSON.pretty_generate(JSON.parse(json_hash.to_json))