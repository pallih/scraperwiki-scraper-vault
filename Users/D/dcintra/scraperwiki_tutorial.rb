require 'open-uri'
require 'nokogiri'

  yelpurl = "http://www.yelp.com/user_details_bookmarks?userid=WE-hYoQ3B4hvLUilyV2lSg" #set user's Yelp URL (Eric's bookmarks)
  userid = yelpurl[yelpurl.index("userid=") + 7, 50] #gets user id
  yelpurl += "&cc=US&city=New+York&state=NY" #set's Yelp URL location to NY
  yelppaginate = "http://www.yelp.com/user_details_bookmarks?cc=US&city=New+York&state=NY&userid=" + userid #set's Yelp URL for multiple pages
   
  names = []                                               
  urls = []
  doc = Nokogiri::HTML(open(yelpurl))
  v = doc.css('.book_biz_info > h3 > a') #CSS selector for bookmarks page
  w = doc.css('td.go-to-page') #CSS selector for pagination test
   
   
  #iterator for users with bookmarks > 50
  if w.text != nil
    for i in 0..w.css('.pager-page').count
      if i === 0
        v = doc.css('.book_biz_info > h3 > a') #CSS selector for bookmarks page
        urls = v.map { |link| "www.yelp.com" + link['href'] }
        names = v.map { |restaurant| restaurant.text }
      else
        doc = Nokogiri::HTML(open(yelppaginate + "&start=#{i*50}")) #iterate through pages
        v = doc.css('.book_biz_info > h3 > a') #CSS selector for bookmarks page
        urls += v.map { |link| "www.yelp.com" + link['href'] }
        names += v.map { |restaurant| restaurant.text }
      end
    end
  else
    urls = v.map { |link| "www.yelp.com" + link['href'] }
    names = v.map { |restaurant| restaurant.text }
  end
puts names
puts urls