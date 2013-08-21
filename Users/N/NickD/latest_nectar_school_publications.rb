# Blank Ruby

require 'hpricot'
require 'open-uri'

data=Hash.new
id=0

sources={"NBS"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/NBS/RSS2/NBS.xml",
  "Education"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/EDU/RSS2/EDU.xml",
  "Health"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/HEA/RSS2/HEA.xml",
  "SciTech"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/SST/RSS2/SST.xml",
  "SocSci"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/SSC/RSS2/SSC.xml",
  "Arts"=>"http://nectar.northampton.ac.uk/cgi/exportview/divisions/ART/RSS2/ART.xml"
}

sources.each do |school,feed|
  doc = Hpricot.XML(open(feed))
  data = {
    "id" => id,
    "title" => "(" + school + ") " + (doc/:item).at("title").inner_html,
    "date" => (doc/:item).at("pubDate").inner_html,
    "link" => (doc/:item).at("link").inner_html,
    "description" => (doc/:item).at("description").inner_html
  }
  ScraperWiki::save_sqlite(['id'], data) 
  id += 1
end
