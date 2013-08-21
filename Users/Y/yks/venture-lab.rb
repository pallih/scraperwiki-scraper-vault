@SOURCE = 'Venture-Lab'
@URL = "https://venture-lab.org"
@ID = 0

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
# 1. open main page
# 2. open each course on page


doc = Nokogiri::HTML(open(@URL))
#p doc

courses = []

doc.search("div.courseCell").each do |v|

  c_link = v.at("h2.courseName a")
  c_url = c_link['href']
  c_title = c_link.text
  photo_el = v.at("img")
  photo = photo_el['src']
  
  #p c_title, photo

  c_doc = Nokogiri::HTML(open(c_url))

  c_descr =""
  c_doc.search("div.content *").each do |c|
    if c.text == "The Course" then
      next
    end
    if c.text == "The Instructor" then
      break
    end
    c_descr = c_descr + c.text
  end 

  #p c_descr

  author = c_doc.at("span.instructorName").text + c_doc.at("span.instructorTitle").text

  meta = c_doc.at("meta[property='og:image']")
  if meta.nil? then
    video = nil
  else
    video = "http://www.youtube.com/watch?v=" + meta['content'].split("/")[-2]
  end
  
  session_text = c_doc.at("div.starting-date").text
  p session_text

      course = {
        :name     => c_title,
        :url      => c_url,
        :organisation => @SOURCE,
        :provider_id => @ID,
        :paid     => false,
        :free     => true,
        :language => 'en',
        :photo    => photo,
        :authors  => [author],
        :cat      => [],
        :description => c_descr,
        :certificate => true,
        :exam     => true,
        #:year     => year,
        #:month    => month,
        #:day      => day,
        #:in_progress => in_progress,
        :video    => video,
      }
      p JSON.pretty_generate(course)
#      courses << course


end