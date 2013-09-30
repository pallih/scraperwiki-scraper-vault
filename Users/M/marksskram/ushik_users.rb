require 'open-uri'
require 'net/http'

row = {"at" => Time.now}

params = {'request_action' => 'SessionCount'}
url = URI.parse('http://ushik.ahrq.gov/ajaxHandler')
response, result = Net::HTTP.post_form(url, params)


data = JSON.parse(result)
row["sessionCount"] = data["sessionCount"]

ScraperWiki::save_sqlite(unique_keys=["at"], data=row)           
require 'open-uri'
require 'net/http'

row = {"at" => Time.now}

params = {'request_action' => 'SessionCount'}
url = URI.parse('http://ushik.ahrq.gov/ajaxHandler')
response, result = Net::HTTP.post_form(url, params)


data = JSON.parse(result)
row["sessionCount"] = data["sessionCount"]

ScraperWiki::save_sqlite(unique_keys=["at"], data=row)           
require 'open-uri'
require 'net/http'

row = {"at" => Time.now}

params = {'request_action' => 'SessionCount'}
url = URI.parse('http://ushik.ahrq.gov/ajaxHandler')
response, result = Net::HTTP.post_form(url, params)


data = JSON.parse(result)
row["sessionCount"] = data["sessionCount"]

ScraperWiki::save_sqlite(unique_keys=["at"], data=row)           
