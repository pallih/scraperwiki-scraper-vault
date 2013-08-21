###############################################################################
# DCIncide Scraper
##################
#############################################################

require 'uri'
require 'nokogiri'

POST_ID_PATTERN = /no=(\d+)/

# retrieve a page
starting_url = URI('http://gall.dcinside.com/list.php?id=taeyeon_new')
html = ScraperWiki.scrape(starting_url.to_s)

# use Nokogiri to get all <td> tags
doc = Nokogiri::HTML(html)
posts = doc.xpath('//table[@id="list_table"]//tr//td[@style="word-break:break-all;"]//a').to_a
# Remove the comment links
posts.reject! {|i| i.attributes["href"].value =~ /.+&view_comment=1/}
posts.each do |post|
  absolute_post_url = starting_url + post.attributes['href'].value
  post_id = POST_ID_PATTERN.match(absolute_post_url.to_s)[1]
  post = {
    'id' => post_id,
    'url' => absolute_post_url,
    'title' => post.content
  }
  ScraperWiki.save_sqlite(['id'], post, table_name = "posts")
end