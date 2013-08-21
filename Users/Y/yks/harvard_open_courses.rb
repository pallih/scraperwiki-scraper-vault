SOURCE = 'Extension Harvard School'
URL = "http://www.extension.harvard.edu/open-learning-initiative"


#p html

require 'nokogiri'
require 'open-uri'
           
MAPPING = [
[1, /Computer/i],
[1, /Bits/i],
[9, /Classic/i],
[9, /Play/i],
[15, /Algebra/i],
[15, /Probability/i],
[9, /Century/i],
[9, /Traditions/i],
[9, /Shakespeare/i],
]

def map_category(cat)
  mapped = MAPPING.select {|m| m[1] =~ cat}.map {|m| m[0]}.uniq
end


doc = Nokogiri::HTML(open(URL))
#p doc

courses = []

doc.search("div[class='course clearfix']").each do |v|
  title = v.at("h3").text
  image = "http://www.extension.harvard.edu" + v.at("img")['src']
  cat = map_category(title)
  site_link = "http://www.extension.harvard.edu" + v.at("h3 a")['href']
  
  #p title, image
  p cat

  authors = ""
  v.search("p").each do |c|
    if not c.at("span").nil? 
      authors += c.text + " "
    end
  end    

    #p site_link['href']

    c_doc = Nokogiri::HTML(open(site_link))

      c_descr = c_doc.at("div.oli-body-container p").text
      video_link = site_link
 
      course = {
        :name     => title,
        :url      => site_link, #c_url,
        :organisation => SOURCE,
        :paid     => false,
        :language => 'en',
        :image    => image,
        :authors  => authors,
        :cat      => cat,
        :term     => nil,
        :description => c_descr,
        :certificate => false,
        :exam     => false,
        #:year     => year,
        #:month    => month,
        #:day      => day,
        #:in_progress => in_progress,
        :video    => video_link,
      }
      puts JSON.pretty_generate(course)
#      courses << course


end

