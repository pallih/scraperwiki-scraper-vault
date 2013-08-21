require 'open-uri'
require 'json'
require 'yaml'

def titleize(string)
  string.split(/(\W)/).map(&:capitalize).join
end

crime = JSON.parse open('http://policeapi2.rkh.co.uk/api/crimes-street/all-crime?lat=52.496792&lng=-1.706791&date=2012-11').read

def save_crime(crime)

  crime.each do |crime|
    details = {}
  
    details[:id] = crime['persistent_id']
    details[:category] = titleize(crime['category'].gsub("-", " "))
    details[:street] = crime['location']['street']['name']
    details[:month] = Date.parse(crime['month'] + '-01').strftime('%B %Y')
    details[:date] = Date.parse(crime['month'] + '-01')
    details[:lat] = crime['location']['latitude']
    details[:lng] = crime['location']['longitude']
  
    ScraperWiki.save([:id], details)
  end

end

def get_latest
  crime = JSON.parse open('http://policeapi2.rkh.co.uk/api/crimes-street/all-crime?lat=52.496792&lng=-1.706791').read
  save_crime(crime)
end

def get_historic
  24.times do |i|
    date = (DateTime.now() << i).strftime("%Y-%m")
    crime = JSON.parse open("http://policeapi2.rkh.co.uk/api/crimes-street/all-crime?lat=52.496792&lng=-1.706791&date=#{date}").read
    save_crime(crime)
  end
end

#get_historic
get_latest