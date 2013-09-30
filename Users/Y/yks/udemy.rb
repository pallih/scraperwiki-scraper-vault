@SOURCE = 'Udemy'
@URL = "http://www.udemy.com"
@ID = 0

#p html

require 'nokogiri'
require 'open-uri'
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
           
MAPPING = [
[1, /Arts and Photography/i],
[3, /Business/i],
[1, /Crafts and Hobbies/i],
[1, /Design/i],
[9, /Education/i],
[5, /Games/i],
[12, /Health and Fitness/i],
[9, /Humanities/i],
[16, /Languages/i],
[14, /Lifestyle/i],
[15, /Math and Science/i],
[9, /Music/i],
[14, /Other/i],
[14, /Social/i],
[8, /Sciences/i],
[14, /Sports/i],
[8, /Technology/i],
]

def map_category(cat)
  mapped = MAPPING.select {|m| m[1] =~ cat}.map {|m| m[0]}.uniq
end

# our plan: 
# 1. open category page https://www.udemy.com/categories
# 2. open each category
# 3. open each course on page
# 4. open next page in category


doc = Nokogiri::HTML(open('https://www.udemy.com/categories'))
#p doc

courses = []

doc.search("li a").each do |v|
  cat = v.text
  cat_url = v['href']

  p cat

  while cat_url != ""
    
    cat_doc = Nokogiri::HTML(open(cat_url))

    #p cat_doc

    cat_doc.search("li.ellipsis a").each do |c|

      title = c['title']
      site_link = c['href']

      #p title, site_link

      c_doc = Nokogiri::HTML(open(site_link))

      c_descr = c_doc.at("div.slp-custom-html div.w3c-default").inner_html
      video_link = site_link
 
      #image = "http://www.extension.harvard.edu" + v.at("img")['src']
  
      authors = c_doc.at("div.ins-details h4").text.strip

      image_elm = c_doc.at("script.jwplayer-params")

      if image_elm.nil? 
         image_link = c_doc.at("div.slp-image img")['src']
      else
         image_link = image_elm.text.split(",")[-1][9..-1].split("\"")[0]
         image_link = image_link.gsub("\\/","/")
      end

      image_link = image_link.gsub("480x270","304x171")

      #p image_link

      free_txt = c_doc.at("a.buy-button-link span").text
      free = (free_txt != "Free")

      course = {
        :name     => title,
        :url      => site_link, #c_url,
        :organisation => @SOURCE,
        :provider_id => @ID,
        :paid     => free,
        :language => 'en',
        :image    => nil,
        :authors  => authors,
        :cat      => cat,
        :description => c_descr,
        :certificate => false,
        :exam     => false,
        #:year     => year,
        #:month    => month,
        #:day      => day,
        #:in_progress => in_progress,
        :video    => video_link,
      }
      p JSON.pretty_generate(course)
#      courses << course

    end #search

    next_page = cat_doc.at("li.last a")

    #p next_page

    cat_url = next_page.nil? ? "" : next_page['href']

  end #while

end #categories

@SOURCE = 'Udemy'
@URL = "http://www.udemy.com"
@ID = 0

#p html

require 'nokogiri'
require 'open-uri'
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
           
MAPPING = [
[1, /Arts and Photography/i],
[3, /Business/i],
[1, /Crafts and Hobbies/i],
[1, /Design/i],
[9, /Education/i],
[5, /Games/i],
[12, /Health and Fitness/i],
[9, /Humanities/i],
[16, /Languages/i],
[14, /Lifestyle/i],
[15, /Math and Science/i],
[9, /Music/i],
[14, /Other/i],
[14, /Social/i],
[8, /Sciences/i],
[14, /Sports/i],
[8, /Technology/i],
]

def map_category(cat)
  mapped = MAPPING.select {|m| m[1] =~ cat}.map {|m| m[0]}.uniq
end

# our plan: 
# 1. open category page https://www.udemy.com/categories
# 2. open each category
# 3. open each course on page
# 4. open next page in category


doc = Nokogiri::HTML(open('https://www.udemy.com/categories'))
#p doc

courses = []

doc.search("li a").each do |v|
  cat = v.text
  cat_url = v['href']

  p cat

  while cat_url != ""
    
    cat_doc = Nokogiri::HTML(open(cat_url))

    #p cat_doc

    cat_doc.search("li.ellipsis a").each do |c|

      title = c['title']
      site_link = c['href']

      #p title, site_link

      c_doc = Nokogiri::HTML(open(site_link))

      c_descr = c_doc.at("div.slp-custom-html div.w3c-default").inner_html
      video_link = site_link
 
      #image = "http://www.extension.harvard.edu" + v.at("img")['src']
  
      authors = c_doc.at("div.ins-details h4").text.strip

      image_elm = c_doc.at("script.jwplayer-params")

      if image_elm.nil? 
         image_link = c_doc.at("div.slp-image img")['src']
      else
         image_link = image_elm.text.split(",")[-1][9..-1].split("\"")[0]
         image_link = image_link.gsub("\\/","/")
      end

      image_link = image_link.gsub("480x270","304x171")

      #p image_link

      free_txt = c_doc.at("a.buy-button-link span").text
      free = (free_txt != "Free")

      course = {
        :name     => title,
        :url      => site_link, #c_url,
        :organisation => @SOURCE,
        :provider_id => @ID,
        :paid     => free,
        :language => 'en',
        :image    => nil,
        :authors  => authors,
        :cat      => cat,
        :description => c_descr,
        :certificate => false,
        :exam     => false,
        #:year     => year,
        #:month    => month,
        #:day      => day,
        #:in_progress => in_progress,
        :video    => video_link,
      }
      p JSON.pretty_generate(course)
#      courses << course

    end #search

    next_page = cat_doc.at("li.last a")

    #p next_page

    cat_url = next_page.nil? ? "" : next_page['href']

  end #while

end #categories

