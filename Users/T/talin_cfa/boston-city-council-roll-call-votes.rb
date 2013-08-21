# Blank Ruby

require 'net/http'
require 'nokogiri'
require 'date'

def get_with_timeout(url,post_data)
  ret=nil
  timeout=0
  while true
    ret=Net::HTTP.post_form(url,post_data)
    if Net::HTTPOK===ret
      break
    else
      if timeout>300
        raise "couldn't get #{url} with post url #{post_data}"
      else
        puts "problem retrieving page. sleeping for #{timeout} seconds"
        sleep(timeout)
        timeout+=30
      end
    end
 end
 Nokogiri::HTML(ret.body)
end

url=URI.parse("http://www.cityofboston.gov/cityclerk/rollcall/Default.aspx")
page=Nokogiri::HTML(Net::HTTP.get(url))
form=page.at_css("form#aspnetForm")
post_data=Hash[*(form.search("input[type=hidden]").map {|x| [x["name"],x["value"]]}.flatten)]
post_data["ctl00$MainContent$ctl00"]="Go!"
num_of_pages=form.at_css("#ctl00_MainContent_lblCurrentPage").content.to_i

1.upto(num_of_pages) do |i|
  post_data["ctl00$MainContent$lblCurrentText"]=i.to_s

  page=get_with_timeout(url,post_data)

  page.css(".ContainerPanel").each do |x|
    save_data={
    "vote_title"=>x.at_css(".HeaderContent b").content.strip,
    "docket_num"=>x.at_css(".HeaderContent b").content.gsub(/\D/,''),
    "description"=>(x.at_css(".Content div").children[0].text.strip rescue nil),
    "date"=>Date.parse(x.at_css("font").content),
    "link"=>("http://www.cityofboston.gov/cityclerk"+x.at_css(".Content div a")["href"].sub(/^\.\./,'') rescue nil),
    "votes"=>x.css(".Content div div").to_enum(:each_slice,3).map {|a,b| "[#{a.content}: #{b.content}]"}*", "
    }
    ScraperWiki.save(save_data.keys,save_data)
    puts save_data["vote_title"]
  end
puts "page #{i}, #{page.css(".ContainerPanel").length} records."
end
