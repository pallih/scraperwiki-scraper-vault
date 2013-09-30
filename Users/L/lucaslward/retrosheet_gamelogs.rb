require "zip/zip"
require "csv" 

zipfile = ScraperWiki::scrape("http://www.retrosheet.org/gamelogs/gl1871.zip")

File.open("1871.zip", "wb") do |file|
  file.write(zipfile)
end

format = {0 => "date", 1 => "number_of_game", 3 => "visiting_team", 4 => "visiting_team_league", 5 => "visiting_team_game_num", 6 => "home_team", 7 => "home_team_league", 8 => "home_team_game_number" }

Zip::ZipFile.open("1871.zip") do |zipfile|
  zipfile.each do |file|
  csv = zipfile.read(file)
  CSV.parse(csv) do |row|
    data = {}
    format.each do |key,value|
      data[value] = row[key]                
    end
    #puts data
    ScraperWiki::save_sqlite(unique_keys=["date","home_team_game_number"], data)
    
    end
  end
end






require "zip/zip"
require "csv" 

zipfile = ScraperWiki::scrape("http://www.retrosheet.org/gamelogs/gl1871.zip")

File.open("1871.zip", "wb") do |file|
  file.write(zipfile)
end

format = {0 => "date", 1 => "number_of_game", 3 => "visiting_team", 4 => "visiting_team_league", 5 => "visiting_team_game_num", 6 => "home_team", 7 => "home_team_league", 8 => "home_team_game_number" }

Zip::ZipFile.open("1871.zip") do |zipfile|
  zipfile.each do |file|
  csv = zipfile.read(file)
  CSV.parse(csv) do |row|
    data = {}
    format.each do |key,value|
      data[value] = row[key]                
    end
    #puts data
    ScraperWiki::save_sqlite(unique_keys=["date","home_team_game_number"], data)
    
    end
  end
end






