require 'rubygems'
require 'open-uri'
require 'json'
# require 'zip/zip' # NO ZIPS ON SCRAPER WIKI =(

# Specify which Source to Download
# url    = "ftp://ftp.census.gov/govs/gid/2007gid_counties.zip"

# Get it
# stream = open(url); nil;

# Unzip it
# unzipped_text = Zip::ZipFile.open(stream, "r") { |zipfile|
#  zipfile.read("2007gid_counties.txt")
# }
unzipped_text = open("http://dl.dropbox.com/u/1186808/2007gid_counties.txt").read.split("\n")

counties = unzipped_text

counties.each do |county| # grab the attributes from each row of the fixed-width file
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
           :population         => county[379..401].strip
  }

  ScraperWiki.save(unique_keys = data.keys, data = data)
end


