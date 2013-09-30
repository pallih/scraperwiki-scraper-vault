# Twitter feed without OAuth (let's get back to v1.0)

html = ScraperWiki::scrape("https://twitter.com/search?q=%23theactivity&src=typd")

#p html
           
require 'nokogiri'           
doc = Nokogiri::HTML html.gsub(/\n/,'')
doc.search(".search-stream > ol > li").each do |v|
  tweet = v.search '.tweet'
  content = tweet.search '.content'
  avatar = content.search '.avatar'
  username = content.search '.username'
  username = username.inner_html.gsub(/<s>/, "\\3").gsub(/<\/s>/, "\\3").gsub(/<b>/, "\\3").gsub(/<\/b>/, "\\3")
  tweet_text = content.search '.tweet-text'
  time_stamp_full = ((content.search '.tweet-timestamp').first.search 'span')
  time_stamp = time_stamp_full.inner_html.gsub(/<span class=(['"])([^(>)])*>/, "\\3").gsub(/<\/span>/, "\\3")
  a_link_url = content.search '.js-display-url'
  tweet_text = tweet_text.inner_html.gsub(/<a href=(['"])([^(>)])*>/, "\\3").gsub(/<\/a>/, "\\3").gsub(/<\\\/>/, "\\3")
  tweet_text = tweet_text.gsub(/<s>/, "\\3").gsub(/<\/s>/, "\\3").gsub(/<b>/, "\\3").gsub(/<\/b>/, "\\3").gsub(/<strong>/, "\\3").gsub(/<\/strong>/, "\\3").gsub(/<span class=(['"])([^(>)])*>/, "\\3").gsub(/<\/span>/, "\\3")
  #p avatar.first["src"]
    data = {
      #tweet: tweet.inner_html,
      time_stamp: time_stamp,
      time_stamp_full: time_stamp_full.first["data-time"],
      name: avatar.first["alt"],
      avatar: avatar.first["src"],
      tweet_text: tweet_text,
      username: username
    }
    ScraperWiki::save_sqlite(['time_stamp','time_stamp_full','name','avatar','tweet_text','username'], data)
    #puts data.to_json

end   
# Twitter feed without OAuth (let's get back to v1.0)

html = ScraperWiki::scrape("https://twitter.com/search?q=%23theactivity&src=typd")

#p html
           
require 'nokogiri'           
doc = Nokogiri::HTML html.gsub(/\n/,'')
doc.search(".search-stream > ol > li").each do |v|
  tweet = v.search '.tweet'
  content = tweet.search '.content'
  avatar = content.search '.avatar'
  username = content.search '.username'
  username = username.inner_html.gsub(/<s>/, "\\3").gsub(/<\/s>/, "\\3").gsub(/<b>/, "\\3").gsub(/<\/b>/, "\\3")
  tweet_text = content.search '.tweet-text'
  time_stamp_full = ((content.search '.tweet-timestamp').first.search 'span')
  time_stamp = time_stamp_full.inner_html.gsub(/<span class=(['"])([^(>)])*>/, "\\3").gsub(/<\/span>/, "\\3")
  a_link_url = content.search '.js-display-url'
  tweet_text = tweet_text.inner_html.gsub(/<a href=(['"])([^(>)])*>/, "\\3").gsub(/<\/a>/, "\\3").gsub(/<\\\/>/, "\\3")
  tweet_text = tweet_text.gsub(/<s>/, "\\3").gsub(/<\/s>/, "\\3").gsub(/<b>/, "\\3").gsub(/<\/b>/, "\\3").gsub(/<strong>/, "\\3").gsub(/<\/strong>/, "\\3").gsub(/<span class=(['"])([^(>)])*>/, "\\3").gsub(/<\/span>/, "\\3")
  #p avatar.first["src"]
    data = {
      #tweet: tweet.inner_html,
      time_stamp: time_stamp,
      time_stamp_full: time_stamp_full.first["data-time"],
      name: avatar.first["alt"],
      avatar: avatar.first["src"],
      tweet_text: tweet_text,
      username: username
    }
    ScraperWiki::save_sqlite(['time_stamp','time_stamp_full','name','avatar','tweet_text','username'], data)
    #puts data.to_json

end   
