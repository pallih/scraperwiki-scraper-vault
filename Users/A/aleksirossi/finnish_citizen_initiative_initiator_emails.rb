# Blank Ruby
require 'nokogiri'
require 'json'
require 'date'

def pick_emails(person)
  person.find_all do |rep| 
    contact = rep["contactInfo"] and contact["email"]
  end.map do |person|
    email = person["contactInfo"]["email"].gsub(/  /, "@").gsub(/ /, ".")  # /
  end
end

def fetch_emails(initiative)
  json = ScraperWiki::scrape(initiative)
  data = JSON.parse(json)

  emails = []
  if reps = data["representatives"] 
    emails.concat(pick_emails(reps))
  end

  if res = data["reserves"] 
    emails.concat(pick_emails(res))
  end

  emails.each do |email|
    just_number_id = initiative.gsub(/.+?\/(\d+)$/){$1}
    started        = Date.parse(data["startDate"]) < Date.today
    ended          = Date.parse(data["endDate"])   < Date.today
    ScraperWiki::save_sqlite(['initiative_id', 'email'], 
      { :initiative_id => just_number_id,
        :email         => email, 
        :totalSupport  => initiative["totalSupportCount"],
        :startDate     => data["startDate"],
        :endDate       => data["endDate"],
        :started       => started,
        :ended         => ended,
        :ongoing       => (started and not ended),
        :proposalType  => data["proposalType"],
        :state         => data["state"],
      })
  end


#  p emails
  emails
end

# Please note up_to is a global variable at the moment. Set it as high as there are initiatives:
up_to = 200
one_fetch = 10

i = 0
while i < up_to
  puts "Fetching #{i}..#{i+one_fetch}"
  json = ScraperWiki::scrape("https://www.kansalaisaloite.fi/api/v1/initiatives?offset=#{i}&limit=#{one_fetch}&minSupportCount=0")
  data = JSON.parse(json)
  
  emails = data.map do |initiative|
    fetch_emails(initiative["id"])
  end

  i += one_fetch
  
  # p emails.flatten
end


# Blank Ruby
require 'nokogiri'
require 'json'
require 'date'

def pick_emails(person)
  person.find_all do |rep| 
    contact = rep["contactInfo"] and contact["email"]
  end.map do |person|
    email = person["contactInfo"]["email"].gsub(/  /, "@").gsub(/ /, ".")  # /
  end
end

def fetch_emails(initiative)
  json = ScraperWiki::scrape(initiative)
  data = JSON.parse(json)

  emails = []
  if reps = data["representatives"] 
    emails.concat(pick_emails(reps))
  end

  if res = data["reserves"] 
    emails.concat(pick_emails(res))
  end

  emails.each do |email|
    just_number_id = initiative.gsub(/.+?\/(\d+)$/){$1}
    started        = Date.parse(data["startDate"]) < Date.today
    ended          = Date.parse(data["endDate"])   < Date.today
    ScraperWiki::save_sqlite(['initiative_id', 'email'], 
      { :initiative_id => just_number_id,
        :email         => email, 
        :totalSupport  => initiative["totalSupportCount"],
        :startDate     => data["startDate"],
        :endDate       => data["endDate"],
        :started       => started,
        :ended         => ended,
        :ongoing       => (started and not ended),
        :proposalType  => data["proposalType"],
        :state         => data["state"],
      })
  end


#  p emails
  emails
end

# Please note up_to is a global variable at the moment. Set it as high as there are initiatives:
up_to = 200
one_fetch = 10

i = 0
while i < up_to
  puts "Fetching #{i}..#{i+one_fetch}"
  json = ScraperWiki::scrape("https://www.kansalaisaloite.fi/api/v1/initiatives?offset=#{i}&limit=#{one_fetch}&minSupportCount=0")
  data = JSON.parse(json)
  
  emails = data.map do |initiative|
    fetch_emails(initiative["id"])
  end

  i += one_fetch
  
  # p emails.flatten
end


