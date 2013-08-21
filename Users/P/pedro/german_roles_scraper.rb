# encoding: utf-8


require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'

queries=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#'http://berufenet.arbeitsagentur.de/berufe/resultList.do?_pgnt_act=goToAnyPage&_pgnt_pn=1&_pgnt_id=resultList'
j=0

agent = Mechanize.new
cookie = Mechanize::Cookie.new(
    "domain"=> "berufenet.arbeitsagentur.de",
    "hostOnly"=> true,
    "httpOnly"=> false,
    "name"=> "JSESSIONID",
    "path"=> "/",
    "secure"=> false,
    "session"=> true,
    "storeId"=> "0",
    "value"=> "ckZ3RkYpbTDBr62ShqpwpYpP8zVvXyjjHm8GgvH1FY1jDyj4ynYt!-178136610"  )
cookie.domain = "berufenet.arbeitsagentur.de"
cookie.path = "/"
page = agent.get("http://berufenet.arbeitsagentur.de/berufe/search/alpha/index.jsp")
agent.cookie_jar.add(agent.history.last.uri, cookie)
while j<queries.count
queryurl='http://berufenet.arbeitsagentur.de/berufe/alphaSearch.do?alphaCaps='+queries[j] 
mecdoc = agent.get(queryurl)
doc=Nokogiri::HTML(mecdoc.content)
  #puts queryurl
 # doc = Nokogiri::HTML(open(queryurl))
  puts doc
  doc.search("td[@class='daten']").each do |node|
      rolename=node.inner_html
      #puts name
         data={
            advertiser: rolename
          }
         #ScraperWiki::save_sqlite(['role'], data)
    end
j=j+1
end
