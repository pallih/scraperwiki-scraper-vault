# Blank Ruby


require 'nokogiri'

@base_url = "http://www.golfnationwide.com"

html = ScraperWiki.scrape(@base_url + "/default.aspx")
# define the order our columns are displayed in the datastore
ScraperWiki.save_var('data_columns', ['Course', 'State', 'City', 'Address', 'url'])

def scrape_courses( state, url )
  course_html = ScraperWiki.scrape(url)
  course_doc = Nokogiri::HTML(course_html)
  
  courses = course_doc.css("#ctl00_MainContentPlaceholder_GridView1").css("tr")
  courses.delete(courses[0])
  courses.each do |c|
    record = {}
    record['Course'] = c.css('td')[0].css('a')[0].inner_text
    record['url'] = @base_url + c.css('td')[0].css('a')[0]['href']
    record['City'] = c.css('td')[1].inner_text.strip!
    record['State'] = state
    record['Address'] = nil

    # puts(record)

    ScraperWiki.save(['Course','State'], record)
  end
end

doc = Nokogiri::HTML(html)

doc.css("#HomeCourseDirectory").css("a").each do |a|
  state = a.inner_text.split(" Golf Courses")[0]
  puts state
  scrape_courses(state, @base_url + a["href"])

end






