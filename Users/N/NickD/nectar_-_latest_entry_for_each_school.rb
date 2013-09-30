# Blank Ruby
require 'nokogiri'   

data=Hash.new
id=1

sources={
  "NBS"=>"http://nectar.northampton.ac.uk/view/divisions/NBS.date.html",
  "Education"=>"http://nectar.northampton.ac.uk/view/divisions/EDU.date.html",
  "Health"=>"http://nectar.northampton.ac.uk/view/divisions/HEA.date.html",
  "SciTech"=>"http://nectar.northampton.ac.uk/view/divisions/SST.date.html",
  "SocSci"=>"http://nectar.northampton.ac.uk/view/divisions/SSC.date.html",
  "Arts"=>"http://nectar.northampton.ac.uk/view/divisions/ART.date.html"
}

sources.each do |school,source|   
  html = ScraperWiki::scrape(source)   
  doc = Nokogiri::HTML html
  item = doc.css("div#contentCol ol a").first
  data = {
    "id" => id,
    "title" => "(#{school}) " + item.inner_html,
    "date" => Time.now,
    "link" => item["href"],
    "description" => ""
  }
  ScraperWiki::save_sqlite(['id'], data) 
  id += 1
end
# Blank Ruby
require 'nokogiri'   

data=Hash.new
id=1

sources={
  "NBS"=>"http://nectar.northampton.ac.uk/view/divisions/NBS.date.html",
  "Education"=>"http://nectar.northampton.ac.uk/view/divisions/EDU.date.html",
  "Health"=>"http://nectar.northampton.ac.uk/view/divisions/HEA.date.html",
  "SciTech"=>"http://nectar.northampton.ac.uk/view/divisions/SST.date.html",
  "SocSci"=>"http://nectar.northampton.ac.uk/view/divisions/SSC.date.html",
  "Arts"=>"http://nectar.northampton.ac.uk/view/divisions/ART.date.html"
}

sources.each do |school,source|   
  html = ScraperWiki::scrape(source)   
  doc = Nokogiri::HTML html
  item = doc.css("div#contentCol ol a").first
  data = {
    "id" => id,
    "title" => "(#{school}) " + item.inner_html,
    "date" => Time.now,
    "link" => item["href"],
    "description" => ""
  }
  ScraperWiki::save_sqlite(['id'], data) 
  id += 1
end
