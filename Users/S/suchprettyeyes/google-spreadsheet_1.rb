# Google Spreadsheet Data

# Description: Grab Google Spreadsheet Data
# Date:        2/22/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'json'


url  = "http://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values?alt=json"

response  = open(url).read

page      = JSON.parse(response)

positions = page["feed"]["entry"]

puts positions.length
positions.each do |row|
  #puts positions.inspect
  @data = {
    'state'        => row["gsx$state"]["$t"], 
    'county'       => row["gsx$county"]["$t"],
    'city'         => row["gsx$city"]["$t"],
    'organization' => row["gsx$organization"]["$t"],
    'position'     => row["gsx$position"]["$t"],
    'name'         => row["gsx$name"]["$t"],
    'phone'        => row["gsx$phonenumber"]["$t"],
    'address'      => row["gsx$address"]["$t"],
    'zip'          => row["gsx$zip"]["$t"],
    'email'        => row["gsx$email"]["$t"],
    'email2'       => row["gsx$email2"]["$t"],
    'url'          => row["gsx$website"]["$t"],
    'term_expiration_date' => row["gsx$termexpirationdate"]["$t"],
    'source_url'   => row["gsx$sourcepage"]["$t"],
  }
#puts row.inspect 
puts @data

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # positions.each


=begin


{
"gsx$zip"=>{"$t"=>""},
"gsx$phonenumber"=>{"$t"=>"707-421-7356"},
"category"=>[
 {
 "term"=>"http://schemas.google.com/spreadsheets/2006#list",
 scheme"=>"http://schemas.google.com/spreadsheets/2006"}],
 
"gsx$email"=>{"$t"=>"psanchez@suisun.com"}, "gsx$county"=>{"$t"=>"Solano"}, "title"=>{"$t"=>"California", "type"=>"text"}, "gsx$termexpirationdate"=>{"$t"=>""}, "gsx$website"=>{"$t"=>""}, "gsx$email2"=>{"$t"=>""}, "gsx$sourcepage"=>{"$t"=>"http://www.suisun.com/City%20Council/sanchez.html"}, "gsx$organization"=>{"$t"=>"City Council"}, "gsx$state"=>{"$t"=>"California"}, "id"=>{"$t"=>"https://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values/esfl1"}, "gsx$address"=>{"$t"=>""}, "gsx$name"=>{"$t"=>"Pete Sanchez"}, "gsx$city"=>{"$t"=>"Suisun"}, "content"=>{"$t"=>"county: Solano, city: Suisun, organization: City Council, position: Mayor, name: Pete Sanchez, phonenumber: 707-421-7356, email: psanchez@suisun.com, sourcepage: http://www.suisun.com/City%20Council/sanchez.html", "type"=>"text"}, "link"=>[{"href"=>"https://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values/esfl1", "rel"=>"self", "type"=>"application/atom+xml"}], "updated"=>{"$t"=>"2010-10-21T05:10:23.752Z"}, "gsx$position"=>{"$t"=>"Mayor"}}

=end

# Google Spreadsheet Data

# Description: Grab Google Spreadsheet Data
# Date:        2/22/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'json'


url  = "http://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values?alt=json"

response  = open(url).read

page      = JSON.parse(response)

positions = page["feed"]["entry"]

puts positions.length
positions.each do |row|
  #puts positions.inspect
  @data = {
    'state'        => row["gsx$state"]["$t"], 
    'county'       => row["gsx$county"]["$t"],
    'city'         => row["gsx$city"]["$t"],
    'organization' => row["gsx$organization"]["$t"],
    'position'     => row["gsx$position"]["$t"],
    'name'         => row["gsx$name"]["$t"],
    'phone'        => row["gsx$phonenumber"]["$t"],
    'address'      => row["gsx$address"]["$t"],
    'zip'          => row["gsx$zip"]["$t"],
    'email'        => row["gsx$email"]["$t"],
    'email2'       => row["gsx$email2"]["$t"],
    'url'          => row["gsx$website"]["$t"],
    'term_expiration_date' => row["gsx$termexpirationdate"]["$t"],
    'source_url'   => row["gsx$sourcepage"]["$t"],
  }
#puts row.inspect 
puts @data

ScraperWiki.save(unique_keys = @data.keys, data = @data)

end # positions.each


=begin


{
"gsx$zip"=>{"$t"=>""},
"gsx$phonenumber"=>{"$t"=>"707-421-7356"},
"category"=>[
 {
 "term"=>"http://schemas.google.com/spreadsheets/2006#list",
 scheme"=>"http://schemas.google.com/spreadsheets/2006"}],
 
"gsx$email"=>{"$t"=>"psanchez@suisun.com"}, "gsx$county"=>{"$t"=>"Solano"}, "title"=>{"$t"=>"California", "type"=>"text"}, "gsx$termexpirationdate"=>{"$t"=>""}, "gsx$website"=>{"$t"=>""}, "gsx$email2"=>{"$t"=>""}, "gsx$sourcepage"=>{"$t"=>"http://www.suisun.com/City%20Council/sanchez.html"}, "gsx$organization"=>{"$t"=>"City Council"}, "gsx$state"=>{"$t"=>"California"}, "id"=>{"$t"=>"https://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values/esfl1"}, "gsx$address"=>{"$t"=>""}, "gsx$name"=>{"$t"=>"Pete Sanchez"}, "gsx$city"=>{"$t"=>"Suisun"}, "content"=>{"$t"=>"county: Solano, city: Suisun, organization: City Council, position: Mayor, name: Pete Sanchez, phonenumber: 707-421-7356, email: psanchez@suisun.com, sourcepage: http://www.suisun.com/City%20Council/sanchez.html", "type"=>"text"}, "link"=>[{"href"=>"https://spreadsheets.google.com/feeds/list/0Ag8ZjYwPcKULdEwtd2IxeGp3aFc2SjE0UGVLX1lMckE/1/public/values/esfl1", "rel"=>"self", "type"=>"application/atom+xml"}], "updated"=>{"$t"=>"2010-10-21T05:10:23.752Z"}, "gsx$position"=>{"$t"=>"Mayor"}}

=end

