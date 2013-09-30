# coding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'


#ScraperWiki::attach("it_glossary")
#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_keyword as select * from it_glossary.search_keyword")

#ScraperWiki::sqliteexecute("drop table search_city") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_city as select * from it_glossary.search_city")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword IN ( 'AWS+C3')")

#ScraperWiki::commit()


words = []
url_all = 'http://abv.bg'

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']


url_all = 'http://www.jobtiger.bg/obiavi-za-rabota/?ln=2&sector=121,122,123,124,145,125&_pagerRows=30'

today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s

words.each do |word|

  saved_rows = 0
  url = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&jtref=megahome"
  url_pages = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&_pagerRows=30&_page=$$$##mm" 

  doc_page = Nokogiri.HTML(open(url))
  total_rows = doc_page.search 'table/tr/td[@class="first"]/b'
  #p total_rows.inner_text.stripq

  if total_rows.empty? == false then

    rows = total_rows.inner_text.strip.to_i
    cur_page = 1
    p word + ' -> ' + rows.to_s

    while rows > -30
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))

      doc.search('table[@class="pager_details"]/tr').each do |v|
        cells = v.search 'td'

        job_id= cells[0].search 'table/tr/td'
        location = v.search 'td[@class="job_regions"]'
        job_date = v.search 'td[@class="rel_period"]'

#        if cells.count == 14 or cells.count == 13
        if cells.count >8 
          data = {
            id: job_id[1].at("a").attributes["id"].value,
            publish_data: job_date[0].inner_text.strip,
            text_body: cells[2].inner_text.strip,
            location: location[0].inner_text.strip,
            company_name: cells[5].inner_text.strip,
            job_link: ("http://www.jobtiger.bg" + job_id[1].at("a").attributes["href"].value).sub('http://www.jobtiger.bghttp://www.jobtiger.bg', 'http://www.jobtiger.bg'),
            week: cur_week,
            year: cur_year,
            month: cur_month,
            search_keyword: word
          }
          #puts data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id','week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)
          saved_rows = saved_rows + 1
#        end
        else
          data = {
            id: job_id[1].at("a").attributes["id"].value,
            publish_data: job_date[0].inner_text.strip,
            text_body: cells[2].inner_text.strip,
            location: location[0].inner_text.strip,
            company_name: cells[5].inner_text.strip,
            week: cur_week,
            year: cur_year,
            month: cur_month
          }
          p data
  #          p v
        end
      end

      cur_page = cur_page + 1
      rows     = rows - 30
      #p rows.to_s + ' -> ' + cur_page.to_s
    end  
    p word + ' -> (saved) ' + saved_rows.to_s 
  else
    p word + ' -> 0'
  end
end

#ScraperWiki::sqliteexecute("delete from all_possitions2 where 1=1") rescue cur_id = 0
#ScraperWiki::sqliteexecute("drop table all_possitions2") rescue cur_id = 0

url_all_pages = 'http://www.jobtiger.bg/obiavi-za-rabota/?ln=2&sector=121,122,123,124,145,125&_pagerRows=30&_page=$$$##mm'

doc_page = Nokogiri.HTML(open(url_all))
total_rows = doc_page.search 'table/tr/td[@class="first"]/b'

if total_rows.empty? == false then

  rows = total_rows.inner_text.strip.to_i
  cur_page = 1
  row_saved = 0
  p 'all -> ' + rows.to_s

  while rows > -30
    doc = Nokogiri.HTML(open(url_all_pages.sub('$$$##mm', cur_page.to_s)))

    doc.search('table[@class="pager_details"]/tr').each do |v|
      cells = v.search 'td'

      job_id= cells[0].search 'table/tr/td'
      location = v.search 'td[@class="job_regions"]'
      job_date = v.search 'td[@class="rel_period"]'

#      if cells.count == 14 or cells.count == 13 or cells.count == 16
      if cells.count >8 
        data = {
          id: job_id[1].at("a").attributes["id"].value,
          publish_data: job_date[0].inner_text.strip,
          text_body: cells[2].inner_text.strip,
          location: location[0].inner_text.strip,
          company_name: cells[5].inner_text.strip,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        #puts data.to_json
        ScraperWiki::save_sqlite(unique_keys=['id','week', 'year', 'month'], data, table_name="all_possitions", verbose=0)
        row_saved = row_saved + 1
#      end
      else
        data = {
          id: job_id[1].at("a").attributes["id"].value,
          publish_data: job_date[0].inner_text.strip,
          text_body: cells[2].inner_text.strip,
          location: location[0].inner_text.strip,
          company_name: cells[5].inner_text.strip,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        p data
#          p v
      end

    end

    cur_page = cur_page + 1
    rows     = rows - 30
#    rows     = 0 - 30
    p rows.to_s + ' -> ' + cur_page.to_s + '(' + row_saved.to_s + ')'
  end   
else
  p 'all -> 0'
end
# coding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'


#ScraperWiki::attach("it_glossary")
#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_keyword as select * from it_glossary.search_keyword")

#ScraperWiki::sqliteexecute("drop table search_city") rescue rr = 0
#ScraperWiki::sqliteexecute("create table search_city as select * from it_glossary.search_city")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword IN ( 'AWS+C3')")

#ScraperWiki::commit()


words = []
url_all = 'http://abv.bg'

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']


url_all = 'http://www.jobtiger.bg/obiavi-za-rabota/?ln=2&sector=121,122,123,124,145,125&_pagerRows=30'

today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s

words.each do |word|

  saved_rows = 0
  url = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&jtref=megahome"
  url_pages = "http://www.jobtiger.bg/obiavi-za-rabota/?keyword=" + word + "&_pagerRows=30&_page=$$$##mm" 

  doc_page = Nokogiri.HTML(open(url))
  total_rows = doc_page.search 'table/tr/td[@class="first"]/b'
  #p total_rows.inner_text.stripq

  if total_rows.empty? == false then

    rows = total_rows.inner_text.strip.to_i
    cur_page = 1
    p word + ' -> ' + rows.to_s

    while rows > -30
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))

      doc.search('table[@class="pager_details"]/tr').each do |v|
        cells = v.search 'td'

        job_id= cells[0].search 'table/tr/td'
        location = v.search 'td[@class="job_regions"]'
        job_date = v.search 'td[@class="rel_period"]'

#        if cells.count == 14 or cells.count == 13
        if cells.count >8 
          data = {
            id: job_id[1].at("a").attributes["id"].value,
            publish_data: job_date[0].inner_text.strip,
            text_body: cells[2].inner_text.strip,
            location: location[0].inner_text.strip,
            company_name: cells[5].inner_text.strip,
            job_link: ("http://www.jobtiger.bg" + job_id[1].at("a").attributes["href"].value).sub('http://www.jobtiger.bghttp://www.jobtiger.bg', 'http://www.jobtiger.bg'),
            week: cur_week,
            year: cur_year,
            month: cur_month,
            search_keyword: word
          }
          #puts data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id','week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)
          saved_rows = saved_rows + 1
#        end
        else
          data = {
            id: job_id[1].at("a").attributes["id"].value,
            publish_data: job_date[0].inner_text.strip,
            text_body: cells[2].inner_text.strip,
            location: location[0].inner_text.strip,
            company_name: cells[5].inner_text.strip,
            week: cur_week,
            year: cur_year,
            month: cur_month
          }
          p data
  #          p v
        end
      end

      cur_page = cur_page + 1
      rows     = rows - 30
      #p rows.to_s + ' -> ' + cur_page.to_s
    end  
    p word + ' -> (saved) ' + saved_rows.to_s 
  else
    p word + ' -> 0'
  end
end

#ScraperWiki::sqliteexecute("delete from all_possitions2 where 1=1") rescue cur_id = 0
#ScraperWiki::sqliteexecute("drop table all_possitions2") rescue cur_id = 0

url_all_pages = 'http://www.jobtiger.bg/obiavi-za-rabota/?ln=2&sector=121,122,123,124,145,125&_pagerRows=30&_page=$$$##mm'

doc_page = Nokogiri.HTML(open(url_all))
total_rows = doc_page.search 'table/tr/td[@class="first"]/b'

if total_rows.empty? == false then

  rows = total_rows.inner_text.strip.to_i
  cur_page = 1
  row_saved = 0
  p 'all -> ' + rows.to_s

  while rows > -30
    doc = Nokogiri.HTML(open(url_all_pages.sub('$$$##mm', cur_page.to_s)))

    doc.search('table[@class="pager_details"]/tr').each do |v|
      cells = v.search 'td'

      job_id= cells[0].search 'table/tr/td'
      location = v.search 'td[@class="job_regions"]'
      job_date = v.search 'td[@class="rel_period"]'

#      if cells.count == 14 or cells.count == 13 or cells.count == 16
      if cells.count >8 
        data = {
          id: job_id[1].at("a").attributes["id"].value,
          publish_data: job_date[0].inner_text.strip,
          text_body: cells[2].inner_text.strip,
          location: location[0].inner_text.strip,
          company_name: cells[5].inner_text.strip,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        #puts data.to_json
        ScraperWiki::save_sqlite(unique_keys=['id','week', 'year', 'month'], data, table_name="all_possitions", verbose=0)
        row_saved = row_saved + 1
#      end
      else
        data = {
          id: job_id[1].at("a").attributes["id"].value,
          publish_data: job_date[0].inner_text.strip,
          text_body: cells[2].inner_text.strip,
          location: location[0].inner_text.strip,
          company_name: cells[5].inner_text.strip,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        p data
#          p v
      end

    end

    cur_page = cur_page + 1
    rows     = rows - 30
#    rows     = 0 - 30
    p rows.to_s + ' -> ' + cur_page.to_s + '(' + row_saved.to_s + ')'
  end   
else
  p 'all -> 0'
end
