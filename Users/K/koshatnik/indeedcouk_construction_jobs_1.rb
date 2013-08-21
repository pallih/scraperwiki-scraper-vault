# encoding: utf-8

# Indeed.com.br premium ads dataminer

require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'
require 'sanitize'

queries=[]
data = []

counts = Hash.new(0)
j=1
 #while j<queries.count
domain = "http://www.careersinconstruction.com"
searchstring = "/searchjobs/?countrycode=GB&Page="
queryurl=domain+searchstring
pageurl = queryurl+j.to_s()
puts pageurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
resultstotal=doc.search("div[@id='primary'] h1").inner_html
total = resultstotal.sub(/Found ([\d,]*) jobs matching your criteria/,'\1')
total = total.sub(/(\d*),(\d*)/, '\1\2')
total = Integer(total)
puts total
resultsperpage = 10
pages = (total / resultsperpage) + 1
puts pages
resultslimit=100

while j<=resultslimit
  pageurl = queryurl+j.to_s()
  page = Nokogiri::HTML(open(URI::encode(pageurl)))
  page.search("li[@class='regular cf']").each do |node|
   if node.count > 0
      atag=node.css("div[@class='jobWrap'] h4 a")
      if !atag.empty? 
        url=atag.attr("href").to_s
        data.push(url)
        
      end
     
 
    end
  
  end
   j=j + 1
end

data.each do |jobad|
  joburl = domain+jobad
  jobpage = Nokogiri::HTML(open(URI::encode(joburl)))
  content = jobpage.search("div[@itemtype='http://schema.org/JobPosting']")
  title = content.css("div[@id='detailHeader'] h1").inner_html
  description = content.css("div[@class='articleBody']").inner_html
  description = Sanitize.clean(description)
  results={
          url: joburl,
          title: title,
          description: description
          }
  ScraperWiki::save_sqlite(['url'], results)
end

