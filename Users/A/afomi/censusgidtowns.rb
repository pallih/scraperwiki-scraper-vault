require 'rubygems'
require 'open-uri'
require 'json'

# this file had to have certain ASCII characters removed to be easily compatible with Ruby
unzipped_text = open("http://dl.dropbox.com/u/1186808/census/2007gid_towns.txt")

towns = unzipped_text.readlines                                             

puts towns.length

towns.each do |town|
  data = {:file_id            => town[0..13].strip,
          :name               => town[14..77].strip,
          :typ                => town[78..107].strip,
          :reporting_position => town[108..152].strip,
          :address1           => town[153..197].strip,
          :address2           => town[198..242].strip,
          :city               => town[243..274].strip,
          :state_id           => town[275..276].strip,
          :zip_code           => town[277..285].strip,
          :url                => town[286..378].strip,
          :population         => town[379..401].strip,
          :parent_body_name   => town[406..440].strip,
          :parent_body_type   => town[441..465].strip
  }

  ScraperWiki.save(unique_keys = data.keys, data = data)
end

