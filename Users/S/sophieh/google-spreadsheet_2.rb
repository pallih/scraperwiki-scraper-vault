# Google Spreadsheet Data
# Description: Grab Google Spreadsheet Data
# Date:        2/22/2011
# Author:      Ryan Wold - rwold@morequality.org

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'json'

url  = "http://spreadsheets.google.com/feeds/list/0AjaPH1oINIzwdHFQWWlaOU0zRGtoSmhCNGpKcTJ2R0E/od6/public/values?alt=json"
#https://docs.google.com/spreadsheet/pub?key=0AjaPH1oINIzwdHFQWWlaOU0zRGtoSmhCNGpKcTJ2R0E&single=true&gid=0&range=a1%3Ah45&output=html&widget=true


response  = open(url).read
page      = JSON.parse(response)
positions = page["feed"]["entry"]

positions.each do |row|
  @data = {
    'coursetitle'          => row["gsx$coursetitle"]["$t"],
    'insitution'           => row["gsx$insitutionsortedalphabetically"]["$t"],
    'discipline'           => row["gsx$discipline"]["$t"],
    'location'             => row["gsx$location"]["$t"],
    'level'                => row["gsx$level"]["$t"],
    'studentCount'         => row["gsx$approximatenumberofstudents"]["$t"],
    'instructor'           => row["gsx$instructor"]["$t"],
    'url'                  => row["gsx$url"]["$t"]
  }

  ScraperWiki.save(unique_keys = @data.keys, data = @data)
end