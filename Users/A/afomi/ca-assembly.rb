# CA Assembly

# Description: Grab all CA Assembly members
# Date:        2/21/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'

# Helper Methods
def clean_party(node)
  party = (node.css("td")[1].text.strip rescue '')
  if party == "Dem"
    party = "democrat"
  elsif party == "Rep"
    party = "republican"
  end
  party
end

def clean_mail(member)
  email = member.css("td")[5].css("a")[0]["href"].strip rescue ''
  #strip js if necessary
  if email.match("javascript")
    email = email.gsub(/.*\(/, "") # remove front of .js
    email = email.gsub(/\).*/, "") # remove end of .js
    email = email.split(",")[0]  # split .js
    email = email.gsub("'", "")
    puts email
  elsif email.match("mailto:")
    email = email.gsub("mailto:", "")
  end
  
  return email
end

def clean_room(node)
  room = node.css("td")[4].text rescue ''
  room.gsub("Room ", "").strip
end

def clean_district(node)
  district = node.css("td")[2].text.gsub(/[a-zA-Z]/, "").strip rescue ''
end
# End Helper Methods

url     = "http://www.assembly.ca.gov/clerk/MEMBERINFORMATION/memberdir_1.asp"
html    = open(url).read
page    = Nokogiri::HTML(html)
members = page.css("table tr")

members[2..-1].each do |member|  
  @data = {
    'name'            => (name = member.css("td")[0].text.strip rescue ''),
    'first_name'      => (name.split(",")[1].strip rescue ''),
    'last_name'       => (name.split(",")[0].strip rescue ''),
    'party'           => clean_party(member),
    'district'        => clean_district(member),
    'email'           => clean_mail(member),
    'url'             => (member.css("td")[0].css("a")[0]["href"].strip rescue ''),
    'url_image'       => '',
    'url_bio'         => '',
    'address'         => '',
    'room'            => clean_room(member)
  }
  
  ScraperWiki.save(unique_keys=['name', 'first_name', 'last_name', 'party', 'district', 'email', 'url', 'url_image', 'url_bio', 'address', 'room'], data = @data)
end # members.each


# Helper methods


