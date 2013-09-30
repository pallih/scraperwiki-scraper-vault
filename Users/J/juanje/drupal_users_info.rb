# Drupal user info
require 'open-uri'
require 'nokogiri'

organization = "Emergya"

base_url = "http://drupal.org/"
organizations_url = "profile/profile_current_company_organization/"

org_url = base_url + organizations_url + organization
doc = Nokogiri::HTML(open org_url)

users_links = doc.xpath('//div[@class = "name"]/a').collect do |row|
  link = row.attribute('href').value 
end

users_links.each do |user_link|
  url = base_url + user_link
  doc = Nokogiri::HTML(open url)
  name = doc.xpath('//h1[@id = "page-title"]').text
  projects = doc.xpath('//dl/dd/div[@class = "item-list"]/ul/li[@class != "last"]').count
  commits = doc.xpath('//dl/dd/div[@class = "item-list"]/ul/li[@class = "last"]').text
  commits = commits.split(': ')[1]
  puts "\nName: #{name}\t\tProjects: #{projects}\tNum. Commits: #{commits}"

  url = base_url + user_link + "/track"
  doc = Nokogiri::HTML(open url)
  ["Issue", "Project", "Project release", "Forum topic"].each do |type|
    posts = doc.xpath("//tbody/tr/td[text() = \"#{type}\"]").count
    puts "Posts type #{type}: #{posts}"
  end
end# Drupal user info
require 'open-uri'
require 'nokogiri'

organization = "Emergya"

base_url = "http://drupal.org/"
organizations_url = "profile/profile_current_company_organization/"

org_url = base_url + organizations_url + organization
doc = Nokogiri::HTML(open org_url)

users_links = doc.xpath('//div[@class = "name"]/a').collect do |row|
  link = row.attribute('href').value 
end

users_links.each do |user_link|
  url = base_url + user_link
  doc = Nokogiri::HTML(open url)
  name = doc.xpath('//h1[@id = "page-title"]').text
  projects = doc.xpath('//dl/dd/div[@class = "item-list"]/ul/li[@class != "last"]').count
  commits = doc.xpath('//dl/dd/div[@class = "item-list"]/ul/li[@class = "last"]').text
  commits = commits.split(': ')[1]
  puts "\nName: #{name}\t\tProjects: #{projects}\tNum. Commits: #{commits}"

  url = base_url + user_link + "/track"
  doc = Nokogiri::HTML(open url)
  ["Issue", "Project", "Project release", "Forum topic"].each do |type|
    posts = doc.xpath("//tbody/tr/td[text() = \"#{type}\"]").count
    puts "Posts type #{type}: #{posts}"
  end
end