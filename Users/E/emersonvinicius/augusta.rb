require "nokogiri"
require "typhoeus"

beco = "http://www.beco203.com.br/capa-beco-sp.php"

response = Typhoeus::Request.get(beco,
                                :user_agent    => " Mozilla/5.0 Augusta Bot"
                                  ).body


parser = Nokogiri::HTML(response)

beco_show = parser.search(".agenda-item.beco-sp")

puts beco_show.count

beco_show.each do |item|
 title = (item/".poster a").attr "title"
 link = (item/".poster a").attr "href"
 id = link.text.split("=")[1]
 ScraperWiki.save_sqlite(unique_keys=["id"], data={"id"=>id, "link"=> link, "title" => title})
endrequire "nokogiri"
require "typhoeus"

beco = "http://www.beco203.com.br/capa-beco-sp.php"

response = Typhoeus::Request.get(beco,
                                :user_agent    => " Mozilla/5.0 Augusta Bot"
                                  ).body


parser = Nokogiri::HTML(response)

beco_show = parser.search(".agenda-item.beco-sp")

puts beco_show.count

beco_show.each do |item|
 title = (item/".poster a").attr "title"
 link = (item/".poster a").attr "href"
 id = link.text.split("=")[1]
 ScraperWiki.save_sqlite(unique_keys=["id"], data={"id"=>id, "link"=> link, "title" => title})
end