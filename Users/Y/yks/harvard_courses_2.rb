SOURCE = 'Extension Harvard School'
URL = "http://www.extension.harvard.edu/distance-education/online-course-offerings"

#p html

require 'nokogiri'
require 'open-uri'
           
MAPPING = [
[1, /Classics/i],
[1, /Dramatic arts/i],
[1, /Folklore and mythology/i],
[1, /History of art and architecture/i],
[9, /Humanities/i],
[1, /Museum studies/i],
[1, /Music/i],
[9, /Philosophy/i],
[9, /Religion/i],
[1, /Studio arts and film/i],
[3, /Accounting/i],
[3, /Communication/i],
[6, /Economics/i],
[3, /Enterprise management/i],
[6, /Finance/i],
[3, /Information systems management/i],
[3, /Marketing/i],
[3, /Organizational behavior/i],
[5, /Computer science/i],
[8, /Engineering sciences/i],
[15, /Mathematics/i],
[15, /Statistics/i],
[16, /Arabic/i],
[16, /Chinese/i],
[16, /French language and literature/i],
[16, /German/i],
[16, /Greek/i],
[16, /Institute for English Language Programs (IEL)/i],
[16, /Italian/i],
[16, /Japanese/i],
[16, /Latin/i],
[16, /Portuguese/i],
[16, /Russian/i],
[16, /Spanish language and literature/i],
[16, /Creative writing/i],
[16, /English/i],
[16, /Expository writing/i],
[16, /Foreign literature and culture/i],
[9, /Journalism/i],
[9, /Speech/i],
[13, /Astronomy/i],
[2, /Biological sciences/i],
[2, /Biotechnology/i],
[4, /Chemistry/i],
[2, /Environmental studies/i],
[7, /Geology/i],
[12, /Medical sciences/i],
[13, /Physics/i],
[12, /Public health/i],
[14, /Anthropology and archaeology/i],
[14, /Government/i],
[14, /History/i],
[14, /History of science/i],
[11, /Legal studies/i],
[14, /Psychology/i],
[14, /Social sciences/i],
[9, /Education/i],
[9, /Study and research skills/i],
]

def map_category(cat)
  mapped = MAPPING.select {|m| m[1] =~ cat}.map {|m| m[0]}.uniq
end


doc = Nokogiri::HTML(open(URL))
#p doc

courses = []

doc.search("div.item-list").each do |v|
  cat = v.at("h3").text
  #cat_id = map_category(cat)
  
  v.search("span.views-field-title span a").each do |c|
    c_url = c['href']
    #p url_c, c.text
    
    site_link = v.at("span.syllabi-bullet a")
    #p site_link['href']

    c_doc = Nokogiri::HTML(open(c_url))

      c_descr = CGI.unescapeHTML(c_doc.at("div.field-course-detail").inner_html)
      c_instructor = c_doc.at("div.views-field-field-term-nid + div").text.strip rescue ''
      video_link = c_doc.at("div.views-field-field-video-link-url-1 a")
      c_video = video_link.nil? ? nil : video_link['href']

      c_term = c_doc.at("div.views-field-field-term-nid").text.strip rescue ''
      c_term = c_term.split(" (")[0]
      #p c_term

      # 2012-2013:
      #Fall: September 4–December 21
      #Spring: January 28–May 18
      #January 3–26      
        case c_term
        when 'Spring term'
        then 
          year  = '2013'
          month = '01'
          day   = '28'
          in_progress = true
        when 'Fall term', 'Fall term, Section 1'
        then 
          year  = '2012'
          month = '09'
          day   = '04'
          in_progress = false
        end

      course = {
        :name     => c.text,
        :url      => site_link['href'], #c_url,
        :organisation => SOURCE,
        :paid     => true,
        :language => 'en',
        :image    => nil, #course_descr.image,
        :authors  => c_instructor,
        :cat      => cat,
        :term     => c_term,
        :description => c_descr,
        :certificate => true,
        :exam     => true,
        :year     => year,
        :month    => month,
        :day      => day,
        :in_progress => in_progress,
        :video    => c_video,
      }
      puts JSON.pretty_generate(course)
      courses << course

  end

end

SOURCE = 'Extension Harvard School'
URL = "http://www.extension.harvard.edu/distance-education/online-course-offerings"

#p html

require 'nokogiri'
require 'open-uri'
           
MAPPING = [
[1, /Classics/i],
[1, /Dramatic arts/i],
[1, /Folklore and mythology/i],
[1, /History of art and architecture/i],
[9, /Humanities/i],
[1, /Museum studies/i],
[1, /Music/i],
[9, /Philosophy/i],
[9, /Religion/i],
[1, /Studio arts and film/i],
[3, /Accounting/i],
[3, /Communication/i],
[6, /Economics/i],
[3, /Enterprise management/i],
[6, /Finance/i],
[3, /Information systems management/i],
[3, /Marketing/i],
[3, /Organizational behavior/i],
[5, /Computer science/i],
[8, /Engineering sciences/i],
[15, /Mathematics/i],
[15, /Statistics/i],
[16, /Arabic/i],
[16, /Chinese/i],
[16, /French language and literature/i],
[16, /German/i],
[16, /Greek/i],
[16, /Institute for English Language Programs (IEL)/i],
[16, /Italian/i],
[16, /Japanese/i],
[16, /Latin/i],
[16, /Portuguese/i],
[16, /Russian/i],
[16, /Spanish language and literature/i],
[16, /Creative writing/i],
[16, /English/i],
[16, /Expository writing/i],
[16, /Foreign literature and culture/i],
[9, /Journalism/i],
[9, /Speech/i],
[13, /Astronomy/i],
[2, /Biological sciences/i],
[2, /Biotechnology/i],
[4, /Chemistry/i],
[2, /Environmental studies/i],
[7, /Geology/i],
[12, /Medical sciences/i],
[13, /Physics/i],
[12, /Public health/i],
[14, /Anthropology and archaeology/i],
[14, /Government/i],
[14, /History/i],
[14, /History of science/i],
[11, /Legal studies/i],
[14, /Psychology/i],
[14, /Social sciences/i],
[9, /Education/i],
[9, /Study and research skills/i],
]

def map_category(cat)
  mapped = MAPPING.select {|m| m[1] =~ cat}.map {|m| m[0]}.uniq
end


doc = Nokogiri::HTML(open(URL))
#p doc

courses = []

doc.search("div.item-list").each do |v|
  cat = v.at("h3").text
  #cat_id = map_category(cat)
  
  v.search("span.views-field-title span a").each do |c|
    c_url = c['href']
    #p url_c, c.text
    
    site_link = v.at("span.syllabi-bullet a")
    #p site_link['href']

    c_doc = Nokogiri::HTML(open(c_url))

      c_descr = CGI.unescapeHTML(c_doc.at("div.field-course-detail").inner_html)
      c_instructor = c_doc.at("div.views-field-field-term-nid + div").text.strip rescue ''
      video_link = c_doc.at("div.views-field-field-video-link-url-1 a")
      c_video = video_link.nil? ? nil : video_link['href']

      c_term = c_doc.at("div.views-field-field-term-nid").text.strip rescue ''
      c_term = c_term.split(" (")[0]
      #p c_term

      # 2012-2013:
      #Fall: September 4–December 21
      #Spring: January 28–May 18
      #January 3–26      
        case c_term
        when 'Spring term'
        then 
          year  = '2013'
          month = '01'
          day   = '28'
          in_progress = true
        when 'Fall term', 'Fall term, Section 1'
        then 
          year  = '2012'
          month = '09'
          day   = '04'
          in_progress = false
        end

      course = {
        :name     => c.text,
        :url      => site_link['href'], #c_url,
        :organisation => SOURCE,
        :paid     => true,
        :language => 'en',
        :image    => nil, #course_descr.image,
        :authors  => c_instructor,
        :cat      => cat,
        :term     => c_term,
        :description => c_descr,
        :certificate => true,
        :exam     => true,
        :year     => year,
        :month    => month,
        :day      => day,
        :in_progress => in_progress,
        :video    => c_video,
      }
      puts JSON.pretty_generate(course)
      courses << course

  end

end

