require 'nokogiri'
require 'open-uri'
require 'typhoeus'


results = []
pages = []

for year in 2007..2014
  for month in 1..12
    hydra = Typhoeus::Hydra.new
    c_request = Typhoeus::Request.new(curi = "http://www.osl.no/osl/omoss/_statistikk/_punktlighet?page=punctuality_per_airline&selected_year=#{year}&selected_month=#{month}&type=D")
    c_request.on_complete do |response|
      Nokogiri::HTML(response.body).css(".resultData .tabell tr").collect {|x| x.css('td') }.reject {|x| x.length == 0 }.each do |c|
        r_request = Typhoeus::Request.new(uri = URI.escape("http://www.osl.no/osl/omoss/_statistikk/_punktlighet" + c[0].at("a")[:href]))
        r_request.on_complete do |res|
          params = URI.unescape(res.request.url).force_encoding("utf-8")
          airline  = params.match(/airline=([^&]+)&/)[1].gsub("%20"," ")
          theyear  = params.match(/selected_year=([^&]+)&/)[1]
          themonth = params.match(/selected_month=([^&]+)&/)[1]
          puts "#{theyear}-#{themonth}:  #{airline}"
          Nokogiri::HTML(res.body).css(".resultData .tabell tr").collect {|x| x.css('td') }.reject {|x| x.length == 0 }.each do |r|
            result = { 
              :year => theyear, :month => themonth, :airline => airline, :service => r[0].text, :type => r[1].text, 
              :flights_planned => r[2].text, :flights_conducted => r[3].text, :flights_cancelled => r[4].text,
              :flights_delayed => r[6].text, :average_delay => r[8].text
            }
            ScraperWiki.save([:year,:month,:airline,:service,:type],result)
          end #table
        end #on_complete
        hydra.queue r_request
      end #outer table
    end #on_complete
    hydra.queue c_request
    hydra.run
  end #month
end #year
require 'nokogiri'
require 'open-uri'
require 'typhoeus'


results = []
pages = []

for year in 2007..2014
  for month in 1..12
    hydra = Typhoeus::Hydra.new
    c_request = Typhoeus::Request.new(curi = "http://www.osl.no/osl/omoss/_statistikk/_punktlighet?page=punctuality_per_airline&selected_year=#{year}&selected_month=#{month}&type=D")
    c_request.on_complete do |response|
      Nokogiri::HTML(response.body).css(".resultData .tabell tr").collect {|x| x.css('td') }.reject {|x| x.length == 0 }.each do |c|
        r_request = Typhoeus::Request.new(uri = URI.escape("http://www.osl.no/osl/omoss/_statistikk/_punktlighet" + c[0].at("a")[:href]))
        r_request.on_complete do |res|
          params = URI.unescape(res.request.url).force_encoding("utf-8")
          airline  = params.match(/airline=([^&]+)&/)[1].gsub("%20"," ")
          theyear  = params.match(/selected_year=([^&]+)&/)[1]
          themonth = params.match(/selected_month=([^&]+)&/)[1]
          puts "#{theyear}-#{themonth}:  #{airline}"
          Nokogiri::HTML(res.body).css(".resultData .tabell tr").collect {|x| x.css('td') }.reject {|x| x.length == 0 }.each do |r|
            result = { 
              :year => theyear, :month => themonth, :airline => airline, :service => r[0].text, :type => r[1].text, 
              :flights_planned => r[2].text, :flights_conducted => r[3].text, :flights_cancelled => r[4].text,
              :flights_delayed => r[6].text, :average_delay => r[8].text
            }
            ScraperWiki.save([:year,:month,:airline,:service,:type],result)
          end #table
        end #on_complete
        hydra.queue r_request
      end #outer table
    end #on_complete
    hydra.queue c_request
    hydra.run
  end #month
end #year
