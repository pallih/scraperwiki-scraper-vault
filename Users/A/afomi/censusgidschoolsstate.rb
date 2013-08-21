require 'rubygems'
require 'open-uri'
require 'json'

unzipped_text = open("http://dl.dropbox.com/u/1186808/census/2007gid_schools_statedep.txt").read

schools = unzipped_text.split("\n")

puts schools.length

schools.each do |school|
  data = {:file_id            => school[0..13].strip,
          :name               => school[14..77].strip,
          :reporting_position => school[78..122].strip,
          :address1           => school[123..167].strip,
          :address2           => school[168..212].strip,
          :city               => school[213..244].strip,
          :state_id           => school[245..246].strip,
          :zip_code           => school[247..256].strip,
          :url                => school[256..350].strip,
          :number             => school[353..366].strip
  }
  # puts data.to_json
  ScraperWiki.save(unique_keys = data.keys, data = data)
end

