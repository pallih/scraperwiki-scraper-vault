require 'open-uri'
require 'csv'

# This CSV is no longer up to date
# Need to scrape: http://www.merseyside.police.uk/index.aspx?articleid=3791

url = "http://www.merseyside.police.uk/Ext-site/Helicopter/helicopter.csv"
csv = open(url).read
 
CSV.parse(csv) do |row|
    date = row[0]
    time = row[1]
    area = row[2]
    incident = row[3]
    outcome = row[4]

    ScraperWiki.save(["date", "time"], { 'date' => date, 'time' => time, 'area' => area, 'incident' => incident, 'outcome' => outcome })
end

