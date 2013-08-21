# http://www.ibm.com/developerworks/opensource/library/os-dataminingrubytwitter/index.html

# http://rdoc.info/gems/twitter/Twitter/API/Search#search-instance_method

require "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'
require 'nokogiri'

gem 'twitter', '=4.5.0'
require 'twitter'

until_d = "2013-03-01"
since_d = "2013-01-01"
cur_date = Date.today(sg=Date::ITALY).to_s
iter_all = 0
cur_id = (2**(0.size * 8 -2) -1)

words = ['%22Cloud job%22','%22IaaS job%22','%22PaaS job%22','%22SaaS job%22', '%22Public cloud job%22', '%22Private cloud job%22', '%22Hybrid cloud job%22', '%22Azure job%22', '%22amazon EC2 job%22', '%22GOGRID job%22', '%22JoyentCloud job%22', '%22OpSource job%22', '%22Rackspace jobs%22', '%22google app engine job%22', '%22Exadata job%22', '%22Exalogic job%22', '%22Oracle Public Cloud job%22', '%22Heroku Job%22', '%22BigData Job%22', '%22NoSQL Job%22']

#words = ['%22Cloud job%22','%22IaaS job%22','%22PaaS job%22','%22SaaS job%22', '%22Public cloud job%22', '%22Private cloud job%22', '%22Hybrid cloud job%22', '%22Azure job%22', '%22amazon EC2 job%22', '%22BigData Job%22', '%22NoSQL Job%22']

#words = ['%22GOGRID job%22', '%22JoyentCloud job%22', '%22OpSource job%22', '%22Rackspace jobs%22', '%22google app engine job%22', '%22Exadata job%22', '%22Exalogic job%22', '%22Oracle Public Cloud job%22', '%22Heroku Job%22']


# ScraperWiki::sqliteexecute("delete from cloud_jobs_tweets where tweet_data > DATE('now', '-10 days') ")

# Replace the four strings below with your own values.
Twitter.configure do |config|
  config.consumer_key = '9ZMEwMN77jNbRqlDiOA'
  config.consumer_secret = 'SIfdzKa3sb81zK1CZhmxaUfpwkUt6ovDAfiRkEKZuE'
  config.oauth_token = '1236592148-20L59qYeYdnwdAFJWRbCSaWWUXZ8ChiGObhkxze'
  config.oauth_token_secret = 'JVcTXRcQAEvUGXcI80TXIcMcGi8GAiuff247rpRkUqQ'
end

 Twitter.search('"Private cloud job"', :count => 100, :max_id => cur_id).results.map.count

#words.each do |word|

  tweet_date = ScraperWiki::select("DATE('now') AS cur_d, DATE(MAX(tweet_data), '2 days') AS until_d, ifnull(DATE(MAX(tweet_data), '1 days'), DATE('now', '-5 days')) AS since_d, DATE(MAX(tweet_data)) AS max_date FROM cloud_jobs_tweets where search_key = '" + word + "'") rescue until_d = "2013-02-28"
  for d in tweet_date
    until_d = d["cur_d"].to_s
    since_d = d["since_d"].to_s
  end
  
  p until_d
  p since_d

  Twitter.search(word, :count => 100, :until => until_d, :since => since_d, :result_type => "recent").results.map do |status|
#  Twitter.search(word, :count => 100, :max_id => cur_id).results.map do |status|
    p " #{status.created_at} #{status.id}/#{status.from_user}: #{status.text}  %%% #{status.source} *** #{status.urls}"
  #  p "Status.id: #{status.id}"

    inner_data = {
                id: status.id,
                search_key: word,
                iso_language_code: status.user.lang,
                tweet_data: status.created_at,
                from_user: status.from_user,
                tweet_text: status.text,
                tweet_source: status.source
              }
    #puts inner_data.to_json
    ScraperWiki::save_sqlite(unique_keys=['id', 'search_key'], inner_data, table_name="cloud_jobs_tweets", verbose=0)
    
    iter_all +=1;
  end  #search
  p word + ': ' + iter_all.to_s
end



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

