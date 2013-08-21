# http://www.ibm.com/developerworks/opensource/library/os-dataminingrubytwitter/index.html

# http://rdoc.info/gems/twitter/Twitter/API/Search#search-instance_method

require "rubygems"
require "fastercsv"
require 'open-uri'
require 'json'
require 'nokogiri'

gem 'twitter', '=4.5.0'
require 'twitter'

until_d = "2013-05-10"
since_d = "2013-01-01"
cur_d = "2013-05-10"
cur_id = (2**(0.size * 8 -2) -1)
cur_date = Date.today(sg=Date::ITALY).to_s

words = ['ios', 'android', 'windows', 'blackberry', 'iphone', 'galaxy', 's4', 's3', 'z10', 'q10']

#words = ['ios']

# ScraperWiki::sqliteexecute("delete from aas_tweets where tweet_data > DATE('now', '-2 days') and key_word = 'PaaS'")
# ScraperWiki::sqliteexecute("delete from aas_tweets where key_word = 'IaaS'")

# Replace the four strings below with your own values.
Twitter.configure do |config|
  config.consumer_key = '9ZMEwMN77jNbRqlDiOA'
  config.consumer_secret = 'SIfdzKa3sb81zK1CZhmxaUfpwkUt6ovDAfiRkEKZuE'
  config.oauth_token = '1236592148-20L59qYeYdnwdAFJWRbCSaWWUXZ8ChiGObhkxze'
  config.oauth_token_secret = 'JVcTXRcQAEvUGXcI80TXIcMcGi8GAiuff247rpRkUqQ'
end

words.each do |word|

#  while 1>0
    cur_id = (2**(0.size * 8 -2) -1)
 
    #tweet_date = ScraperWiki::select("DATE(MAX(tweet_data)) AS until_d, DATE(MAX(tweet_data), '-1 days') AS since_d FROM cloud_tweets")
    tweet_date = ScraperWiki::select("DATE('now') AS cur_d, DATE(MAX(tweet_data), '2 days') AS until_d, DATE(MAX(tweet_data), '1 days') AS since_d, DATE(MAX(tweet_data)) AS max_date FROM aas_tweets where key_word = '" + word + "'") rescue until_d = "2013-02-28"

    for d in tweet_date
      until_d = d["cur_d"].to_s
      since_d = d["since_d"].to_s
      cur_d = d["cur_d"].to_s
    end

    tweet_id = ScraperWiki::select("ifnull(MIN(ID), 4611686018427387903) as min_id FROM aas_tweets where tweet_data between '" + since_d + "' and '" + until_d + "' and key_word = '" + word + "'") rescue tweet_id = [cur_id] #cur_id = (2**(0.size * 8 -2) -1)

    for d in tweet_id
      cur_id = d["min_id"].to_s
    end
#   cur_id = 306191878498426900
   
#    if cur_d == since_d
#      break
#    end

    

    p until_d
    p since_d
    
    iter = 100
    iter_all = 0
  
    while iter > 0
      iter = 0  
      Twitter.search(word, :count => 100, :max_id => cur_id, :until => until_d, :since => since_d).results.map do |status|
      #  p " #{status.created_at} #{status.id}/#{status.from_user}: #{status.text}  %%% #{status.source} *** #{status.urls}"
      #  p "Status.id: #{status.id}"
    
        inner_data = {
                    id: status.id,
                    key_word: word,
                    iso_language_code: status.user.lang,
                    tweet_data: status.created_at,
                    from_user: status.from_user,
                    tweet_text: status.text,
                    tweet_source: status.source
                  }
        #puts inner_data.to_json
        ScraperWiki::save_sqlite(unique_keys=['id', 'key_word'], inner_data, table_name="aas_tweets", verbose=0)
        
        cur_id = status.id - 1
        iter +=1;
        iter_all +=1;
      end  #search
      p word + ': ' + iter_all.to_s + ' - ' + cur_id.to_s
    end #iter
#  end  #while
  p word + ': ' + iter_all.to_s
end #for




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