require 'scraperwiki'
require 'active_support'
require 'nokogiri'

html = ScraperWiki::scrape("http://www.rubyjobs.ie/")
doc = Nokogiri::HTML(html)

ScraperWiki::sqliteexecute("drop table if exists swdata")

all_jobs = []

# Jeremie scraped a class today :)

# This iterates through each job
doc.xpath(%^//ul[@id='job_list']/li[@class='job']^).each { |li|
  spans = li.xpath('span[@class]')

  data = {}

  # Hmmm... 0 worked as if by magic... Hmmm...
  spans.each {|span|data[span.attribute_nodes[0].value] = span.inner_text}
  
  all_jobs << data
}

# only list 1 job per company
encountered_companies = []
all_jobs.uniq! {|job| job['company']}

all_jobs.each do |job|
  ScraperWiki::save_sqlite(job.keys, job)
end

