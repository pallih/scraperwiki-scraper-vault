# http://www.ibm.com/developerworks/opensource/library/os-dataminingrubytwitter/index.html

# http://rdoc.info/gems/twitter/Twitter/API/Search#search-instance_method

require "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'
require 'nokogiri'

gem 'twitter', '=4.5.0'
require 'twitter'

until_d = "2013-02-28"
since_d = "2013-02-27"
cur_date = Date.today(sg=Date::ITALY).to_s

# Replace the four strings below with your own values.
Twitter.configure do |config|
  config.consumer_key = '9ZMEwMN77jNbRqlDiOA'
  config.consumer_secret = 'SIfdzKa3sb81zK1CZhmxaUfpwkUt6ovDAfiRkEKZuE'
  config.oauth_token = '1236592148-20L59qYeYdnwdAFJWRbCSaWWUXZ8ChiGObhkxze'
  config.oauth_token_secret = 'JVcTXRcQAEvUGXcI80TXIcMcGi8GAiuff247rpRkUqQ'
end

while 1>0

  #tweet_date = ScraperWiki::select("DATE(MAX(tweet_data)) AS until_d, DATE(MAX(tweet_data), '-1 days') AS since_d FROM cloud_tweets")
  tweet_date = ScraperWiki::select("DATE('now') AS cur_d, DATE(MAX(tweet_data), '2 days') AS until_d, DATE(MAX(tweet_data), '1 days') AS since_d, DATE(MAX(tweet_data)) AS max_date FROM cloud_tweets")
  for d in tweet_date
    until_d = d["until_d"].to_s
    since_d = d["since_d"].to_s
    cur_d = d["cur_d"].to_s
  end

  if cur_d == since_d
    break
  end

  cur_id = (2**(0.size * 8 -2) -1)
  p until_d
  p since_d
  
  iter = 100
  #iter = 0
  iter_all = 0

  #p Twitter.user('mlessev')

  #Twitter.search("cloud computing", :count => 30, :lang => "bg", :result_type => "recent", :until => "2013-02-28", :since => "2009-06-16", :near => "sf", :since_id => "307641387694833666", :max_id => "307904737783709696").results.map do |status|


  while iter > 0
    iter = 0  
    Twitter.search("cloud computing", :count => 100, :rpp => 30, :max_id => cur_id, :until => until_d, :since => since_d).results.map do |status|
    #  p " #{status.created_at} #{status.id}/#{status.from_user}: #{status.text}  %%% #{status.source} *** #{status.urls}"
    #  p "Status.id: #{status.id}"
  
      inner_data = {
                  id: status.id,
                  iso_language_code: status.iso_language_code,
                  tweet_data: status.created_at,
                  from_user: status.from_user,
                  tweet_text: status.text,
                  tweet_source: status.source
                }
      #puts inner_data.to_json
      ScraperWiki::save_sqlite(unique_keys=['id'], inner_data, table_name="cloud_tweets", verbose=0)
      
      cur_id = status.id - 1
      iter +=1;
      iter_all +=1;
    end
    
  #  p cur_id
  #  p iter 
  end
end
p iter_all


# p Twitter.status(209584578506133505).text 

# p Twitter.status(307641387694833666).from_user 

#myfollowers = []
#twitter_handle = 'mlessev'

#   https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=mlessev

#   https://api.twitter.com/1/following/ids.json?cursor=-1&screen_name=mlessev



#base_url = 'https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=' + twitter_handle 
#results_json = JSON.parse(open(base_url){|f| f.read})
#myfollowers = results_json['ids']
#myfollowers_str = map(str, myfollowers) 

