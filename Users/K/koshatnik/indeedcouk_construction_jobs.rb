# encoding: utf-8

# Indeed.com.br premium ads dataminer

require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'
require 'sanitize'

queries=[]

counts = Hash.new(0)
j=0
 #while j<queries.count
queryurl="http://www.indeed.co.uk/jobs?q=Construction"
puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
resultstotal=doc.search("div[@id='searchCount']").inner_html
total = resultstotal.sub(/Jobs 1 to 10 of (.*)/,'\1')
total = total.sub(/(\d.),(\d.)/, '\1\2')
total = Integer(total)
puts total
resultsperpage = 10
pages = (total / resultsperpage) + 1
puts pages
resultslimit=1000

while j<=resultslimit
  pageurl = queryurl+"&start="+j.to_s()
  page = Nokogiri::HTML(open(URI::encode(pageurl)))
  page.search("div[@itemtype='http://schema.org/JobPosting']").each do |node|
   if node.count > 0

      jobtitle=node.css("h2 a").inner_html
      jobtitle = Sanitize.clean(jobtitle)
      employer=node.css("span[class=company] span").inner_html
      employer = Sanitize.clean(employer)
      location=node.css("span[itemprop=location] span span").inner_html
      jobdescription=node.css("table tr td div span").inner_html
      jobdescription = jobdescription.sub(/(.*)View more .*/,'/1')
      jobdescription = Sanitize.clean(jobdescription)
      salary=node.css("table tr td div nobr").inner_html

      data={
        jobtitle: jobtitle,
        employer: employer,
        location: location,
        description: jobdescription,
        salary: salary
      }
      ScraperWiki::save_sqlite(['jobtitle'], data)
 
    end
  
  end
   j=j + resultsperpage
end
# encoding: utf-8

# Indeed.com.br premium ads dataminer

require 'open-uri'
require 'nokogiri'
require 'net/http'
require 'ostruct'
require 'mechanize'
require 'sanitize'

queries=[]

counts = Hash.new(0)
j=0
 #while j<queries.count
queryurl="http://www.indeed.co.uk/jobs?q=Construction"
puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
resultstotal=doc.search("div[@id='searchCount']").inner_html
total = resultstotal.sub(/Jobs 1 to 10 of (.*)/,'\1')
total = total.sub(/(\d.),(\d.)/, '\1\2')
total = Integer(total)
puts total
resultsperpage = 10
pages = (total / resultsperpage) + 1
puts pages
resultslimit=1000

while j<=resultslimit
  pageurl = queryurl+"&start="+j.to_s()
  page = Nokogiri::HTML(open(URI::encode(pageurl)))
  page.search("div[@itemtype='http://schema.org/JobPosting']").each do |node|
   if node.count > 0

      jobtitle=node.css("h2 a").inner_html
      jobtitle = Sanitize.clean(jobtitle)
      employer=node.css("span[class=company] span").inner_html
      employer = Sanitize.clean(employer)
      location=node.css("span[itemprop=location] span span").inner_html
      jobdescription=node.css("table tr td div span").inner_html
      jobdescription = jobdescription.sub(/(.*)View more .*/,'/1')
      jobdescription = Sanitize.clean(jobdescription)
      salary=node.css("table tr td div nobr").inner_html

      data={
        jobtitle: jobtitle,
        employer: employer,
        location: location,
        description: jobdescription,
        salary: salary
      }
      ScraperWiki::save_sqlite(['jobtitle'], data)
 
    end
  
  end
   j=j + resultsperpage
end
