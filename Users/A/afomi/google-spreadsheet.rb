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

positions.each do |row|
  @data = {
    'state'                => row["gsx$state"]["$t"],
    'county'               => row["gsx$county"]["$t"],
    'city'                 => row["gsx$city"]["$t"],
    'organization'         => row["gsx$organization"]["$t"],
    'position'             => row["gsx$position"]["$t"],
    'name'                 => row["gsx$name"]["$t"],
    'phone'                => row["gsx$phonenumber"]["$t"],
    'address'              => row["gsx$address"]["$t"],
    'zip'                  => row["gsx$zip"]["$t"],
    'email'                => row["gsx$email"]["$t"],
    'email2'               => row["gsx$email2"]["$t"],
    'url'                  => row["gsx$website"]["$t"],
    'term_expiration_date' => row["gsx$termexpirationdate"]["$t"],
    'source_url'           => row["gsx$sourcepage"]["$t"]
  }

  ScraperWiki.save(unique_keys = @data.keys, data = @data)
end