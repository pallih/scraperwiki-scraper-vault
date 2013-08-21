require 'rubygems'
require 'open-uri'
require 'json'

unzipped_text = open("http://dl.dropbox.com/u/1186808/census/2007gid_cities.txt").read

cities = unzipped_text.split("\n")

puts cities.length

cities.each do |county|
  data = {:file_id             => county[0..13].strip,
           :name               => county[14..77].strip,
           :typ                => county[78..107].strip,
           :reporting_position => county[108..152].strip,
           :address1           => county[153..197].strip,
           :address2           => county[198..242].strip,
           :city               => county[243..274].strip,
           :state_id           => county[275..276].strip,
           :zip_code           => county[277..285].strip,
           :url                => county[286..378].strip,
           :population         => county[379..401].strip,
           :parent_body_name   => county[406..440].strip,
           :parent_body_type   => county[441..465].strip
  }

  ScraperWiki.save(unique_keys = data.keys, data = data)
end

