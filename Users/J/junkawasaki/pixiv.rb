require 'mechanize'
require 'kconv'
require 'nokogiri'

mechanize = Mechanize.new
pixiv_loginpage = mechanize.get("http://www.pixiv.net/login.php")

login_form = pixiv_loginpage.forms.first
login_form['pixiv_id'] = ""
login_form['pass'] = ""
redirect_page = mechanize.submit(login_form, login_form.buttons.first)
# p redirect_page 

search_form = redirect_page.forms.first
search_form['word'] = "naruto" # keyword
search_page = mechanize.submit(search_form, search_form.buttons.first)

# search_page = ScraperWiki::scrape("http://www.pixiv.net/search.php?s_mode=s_tag&word=naruto")

(1..5).each do |num|
  p num
  search_page.search('section#search-result > ul.images > li').each_with_index do |pic, i|
    illust_url       = pic.search('a')[0]    ? pic.search('a')[0]['href'] : nil
    illust_title     = pic.search('h2')      ? pic.search('h2').text : nil
    illust_image_url = pic.search('img')     ? pic.search('img').first['src'] : nil
    user_name        = pic.search('.user a') ? pic.search('.user a').text : nil
    user_url         = pic.search('a')[1]    ? pic.search('a')[1]['href'] : nil

    pic_data = ['illust_url' => illust_url,
         'illust_title'      => illust_title,
         'illust_image_url'  => illust_image_url,
         'user_name'         => user_name,
         'user_url'          => user_url,
    ]

    p i
    
    ScraperWiki::save_sqlite(['illust_url'], pic_data)   
  end

  search_page = mechanize.click(search_page.link_with(:text => '>')) 
endrequire 'mechanize'
require 'kconv'
require 'nokogiri'

mechanize = Mechanize.new
pixiv_loginpage = mechanize.get("http://www.pixiv.net/login.php")

login_form = pixiv_loginpage.forms.first
login_form['pixiv_id'] = ""
login_form['pass'] = ""
redirect_page = mechanize.submit(login_form, login_form.buttons.first)
# p redirect_page 

search_form = redirect_page.forms.first
search_form['word'] = "naruto" # keyword
search_page = mechanize.submit(search_form, search_form.buttons.first)

# search_page = ScraperWiki::scrape("http://www.pixiv.net/search.php?s_mode=s_tag&word=naruto")

(1..5).each do |num|
  p num
  search_page.search('section#search-result > ul.images > li').each_with_index do |pic, i|
    illust_url       = pic.search('a')[0]    ? pic.search('a')[0]['href'] : nil
    illust_title     = pic.search('h2')      ? pic.search('h2').text : nil
    illust_image_url = pic.search('img')     ? pic.search('img').first['src'] : nil
    user_name        = pic.search('.user a') ? pic.search('.user a').text : nil
    user_url         = pic.search('a')[1]    ? pic.search('a')[1]['href'] : nil

    pic_data = ['illust_url' => illust_url,
         'illust_title'      => illust_title,
         'illust_image_url'  => illust_image_url,
         'user_name'         => user_name,
         'user_url'          => user_url,
    ]

    p i
    
    ScraperWiki::save_sqlite(['illust_url'], pic_data)   
  end

  search_page = mechanize.click(search_page.link_with(:text => '>')) 
end