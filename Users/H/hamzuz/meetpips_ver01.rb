
require 'mechanize'
require 'nokogiri'
require 'open-uri'

agent = Mechanize.new
page = agent.get('http://www.reddit.com/')

#/////////////////////////////////////////////////////////////////////#

# http://ruby.about.com/od/mechanize20handbook/a/The-Page-Class_5.htm
text = page.search(%Q{//div[@id='header']//span[@class='user']}).text
if /want to join/ === text
  puts "You are not logged in"
  exit
end
#/////////////////////////////////////////////////////////////////////#



#Check Our Another option - http://robdodson.me/blog/2012/06/20/crawling-pages-with-mechanize-and-nokogiri/




#/////////////////////////////////////////////////////////////////////#

#links_page = 'http://www.meetpips.com/members'
#doc = Nokogiri::HTML.parse(links_page)
#links = doc.at_css('a.profile-link')['href']
#puts links


# page = Nokogiri::HTML(open('http://www.meetpips.com/members'))

# members_links = page.css("class#member-row")
# members_links.each{|links| puts "#{link.text}\t#{link['href']}"}


# post_page = agent.get('http://www.meetpips.com/members')
# puts post_page.parser.xpath('‪//*[contains(concat( " ", @class, " " ), concat( " ", "login", " " ))]‬').to_html




# page.links.each do |link|
# puts link.text

# h1_tags = Nokogiri::HTML(search_results.body).css('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')
# puts "Number of results =  #{h1_tags.text}"
# agent.page.search(".login").map(&:text).map(&:strip)

#page.links_with(:href => %r{/members/} ).each do |link|
      
#      puts 'Loading %-30s %s' % [link.href, link.text]
#end

