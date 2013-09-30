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

# Set lang to en
#doc_page = Nokogiri.HTML(open("http://www.jobs.bg/change_lang.php?new_lang=en&rpath=/index.php"))

#ScraperWiki::attach("employers_in_jobsbg")
#ScraperWiki::sqliteexecute("drop table employers") rescue rr = 0
#ScraperWiki::sqliteexecute("create table employers as select * from employers_in_jobsbg.employers")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword = 'AWS+C3'")

#ScraperWiki::commit()

words = []
url_all = "http://abv.bg"

url_all = "http://it.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=#paging"

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']


today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s
  
# get cloud open possitions
words.each do |word|
  saved_rows = 0
  cond = word
  url = "http://www.jobs.bg/front_job_search.php?frompage=0&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  url_pages = "http://www.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  #url_pages.force_encoding("UTF-8")
  
  doc_page = Nokogiri.HTML(open(url))
  
  total_rows = doc_page.search 'table[@width="980"]/tr/td[@class="pagingtotal"]'

  #p total_rows

  if total_rows.empty? == false then
  
    rows = total_rows[0].inner_text.strip.split("\u043E\u0442")[1].to_i + 20
    cur_page = 0
    p cond + ' -> ' + (rows - 20).to_s
    
    while rows > 0
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))
    
      doc.search('table[@width="670"]/tr').each do |v|
        cells = v.search 'td'
        #cur_link = cells[2].inner_html
        if cells.count == 5 or cells.count == 7
          if cells[4].inner_html.include? '<table' 
            comp_iner = cells[4].search 'table/tr/td'[1]  #rescue comp_name = cells[4].inner_text.strip
            comp_href = comp_iner.at("a").attributes["href"].value rescue comp_href = cells[4].at("a").attributes["href"].value
            comp_name = comp_iner.at("a").inner_text.strip         rescue comp_name = cells[4].inner_text.strip
          else
            comp_name = cells[4].inner_text.strip
            comp_href = cells[4].at("a").attributes["href"].value  rescue comp_href = cells[4].inner_text.strip
          end
          data = {
            id: cells[2].at("a").attributes["href"].value,
            publish_data: cells[0].inner_text.strip.sub('вчера', yesterday.to_s).sub('днес', today.to_s),
            text_body: cells[2].inner_text.strip.sub(cells[2].inner_html.split("<br>")[2].strip, '').strip,
            #location: cells[2].inner_text.strip.slice(30,60),
            location: cells[2].inner_html.split("<br>")[2].strip,
            company_name: comp_name,
            company_href: comp_href,
            job_link: 'http://www.jobs.bg/' + cells[2].at("a").attributes["href"].value,
            week: cur_week,
            year: cur_year,
            month: cur_month,
            search_keyword: cond
          }
          #puts data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id','week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)
          saved_rows = saved_rows + 1
        elsif cells.count == 6
           p cells[2].at("a").attributes["href"].value + ' - ' + 'http://www.jobs.bg/' + cells[2].at("a").attributes["href"].value
        else
#          p v.inner_text.strip
#           p cells.count.to_s 
        end
      end
      
      cur_page = cur_page + 20
      rows     = rows - 20
      # p rows.to_s + ' -> ' + cur_page.to_s
    end
    p word + ' -> (saved) ' + saved_rows.to_s 
  else
    p cond  + ' -> 0'
  end
  #p rows
end  


# get all open possitions

#url_all = "http://www.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&category[]=14&category[]=15&category[]=16&keyword=#paging"


saved_rows = 0
doc_page2 = Nokogiri.HTML(open(url_all.sub('$$$##mm', '0')))
total_rows2 = doc_page2.search 'table[@width="980"]/tr/td[@class="pagingtotal"]'

if total_rows2.empty? == false then
  rows = total_rows2[0].inner_text.strip.split("\u043E\u0442")[1].to_i
  cur_page = 0
  p 'ALL -> ' + rows.to_s
  
  while rows > -20
    doc =  Nokogiri.HTML(open(url_all.sub('$$$##mm', cur_page.to_s)))
  
    doc.search('table[@width="670"]/tr').each do |v|
      cells = v.search 'td'
      if cells.count == 5  or cells.count == 7
        if cells[4].inner_html.include? '<table' 
          comp_iner = cells[4].search 'table/tr/td'[1]  #rescue comp_name = cells[4].inner_text.strip
          comp_href = comp_iner.at("a").attributes["href"].value rescue comp_href = cells[4].at("a").attributes["href"].value
          comp_name = comp_iner.at("a").inner_text.strip         rescue comp_name = cells[4].inner_text.strip
        else
          comp_name = cells[4].inner_text.strip
          comp_href = cells[4].at("a").attributes["href"].value  rescue comp_href = cells[4].inner_text.strip
        end
        data = {
          id: cells[2].at("a").attributes["href"].value,
          publish_data: cells[0].inner_text.strip.sub('вчера', yesterday.to_s).sub('днес', today.to_s),
          text_body: cells[2].inner_text.strip.sub(cells[2].inner_html.split("<br>")[2].strip, '').strip,
          location: cells[2].inner_html.split("<br>")[2].strip,
          company_name: comp_name,
          company_href: comp_href,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        ScraperWiki::save_sqlite(unique_keys=['id','week', 'year', 'month'], data, table_name="all_possitions", verbose=0)
        saved_rows = saved_rows + 1
      end
    end
    cur_page = cur_page + 20
    rows     = rows - 20
    p rows.to_s + ' -> ' + cur_page.to_s + '(' + saved_rows.to_s + ')'
  end
else
  p 'ALL -> 0'
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

# Set lang to en
#doc_page = Nokogiri.HTML(open("http://www.jobs.bg/change_lang.php?new_lang=en&rpath=/index.php"))

#ScraperWiki::attach("employers_in_jobsbg")
#ScraperWiki::sqliteexecute("drop table employers") rescue rr = 0
#ScraperWiki::sqliteexecute("create table employers as select * from employers_in_jobsbg.employers")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword = 'AWS+C3'")

#ScraperWiki::commit()

words = []
url_all = "http://abv.bg"

url_all = "http://it.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=#paging"

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']


today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s
  
# get cloud open possitions
words.each do |word|
  saved_rows = 0
  cond = word
  url = "http://www.jobs.bg/front_job_search.php?frompage=0&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  url_pages = "http://www.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  #url_pages.force_encoding("UTF-8")
  
  doc_page = Nokogiri.HTML(open(url))
  
  total_rows = doc_page.search 'table[@width="980"]/tr/td[@class="pagingtotal"]'

  #p total_rows

  if total_rows.empty? == false then
  
    rows = total_rows[0].inner_text.strip.split("\u043E\u0442")[1].to_i + 20
    cur_page = 0
    p cond + ' -> ' + (rows - 20).to_s
    
    while rows > 0
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))
    
      doc.search('table[@width="670"]/tr').each do |v|
        cells = v.search 'td'
        #cur_link = cells[2].inner_html
        if cells.count == 5 or cells.count == 7
          if cells[4].inner_html.include? '<table' 
            comp_iner = cells[4].search 'table/tr/td'[1]  #rescue comp_name = cells[4].inner_text.strip
            comp_href = comp_iner.at("a").attributes["href"].value rescue comp_href = cells[4].at("a").attributes["href"].value
            comp_name = comp_iner.at("a").inner_text.strip         rescue comp_name = cells[4].inner_text.strip
          else
            comp_name = cells[4].inner_text.strip
            comp_href = cells[4].at("a").attributes["href"].value  rescue comp_href = cells[4].inner_text.strip
          end
          data = {
            id: cells[2].at("a").attributes["href"].value,
            publish_data: cells[0].inner_text.strip.sub('вчера', yesterday.to_s).sub('днес', today.to_s),
            text_body: cells[2].inner_text.strip.sub(cells[2].inner_html.split("<br>")[2].strip, '').strip,
            #location: cells[2].inner_text.strip.slice(30,60),
            location: cells[2].inner_html.split("<br>")[2].strip,
            company_name: comp_name,
            company_href: comp_href,
            job_link: 'http://www.jobs.bg/' + cells[2].at("a").attributes["href"].value,
            week: cur_week,
            year: cur_year,
            month: cur_month,
            search_keyword: cond
          }
          #puts data.to_json
          ScraperWiki::save_sqlite(unique_keys=['id','week', 'search_keyword', 'year', 'month'], data, table_name="cloud_possitions", verbose=0)
          saved_rows = saved_rows + 1
        elsif cells.count == 6
           p cells[2].at("a").attributes["href"].value + ' - ' + 'http://www.jobs.bg/' + cells[2].at("a").attributes["href"].value
        else
#          p v.inner_text.strip
#           p cells.count.to_s 
        end
      end
      
      cur_page = cur_page + 20
      rows     = rows - 20
      # p rows.to_s + ' -> ' + cur_page.to_s
    end
    p word + ' -> (saved) ' + saved_rows.to_s 
  else
    p cond  + ' -> 0'
  end
  #p rows
end  


# get all open possitions

#url_all = "http://www.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&category[]=14&category[]=15&category[]=16&keyword=#paging"


saved_rows = 0
doc_page2 = Nokogiri.HTML(open(url_all.sub('$$$##mm', '0')))
total_rows2 = doc_page2.search 'table[@width="980"]/tr/td[@class="pagingtotal"]'

if total_rows2.empty? == false then
  rows = total_rows2[0].inner_text.strip.split("\u043E\u0442")[1].to_i
  cur_page = 0
  p 'ALL -> ' + rows.to_s
  
  while rows > -20
    doc =  Nokogiri.HTML(open(url_all.sub('$$$##mm', cur_page.to_s)))
  
    doc.search('table[@width="670"]/tr').each do |v|
      cells = v.search 'td'
      if cells.count == 5  or cells.count == 7
        if cells[4].inner_html.include? '<table' 
          comp_iner = cells[4].search 'table/tr/td'[1]  #rescue comp_name = cells[4].inner_text.strip
          comp_href = comp_iner.at("a").attributes["href"].value rescue comp_href = cells[4].at("a").attributes["href"].value
          comp_name = comp_iner.at("a").inner_text.strip         rescue comp_name = cells[4].inner_text.strip
        else
          comp_name = cells[4].inner_text.strip
          comp_href = cells[4].at("a").attributes["href"].value  rescue comp_href = cells[4].inner_text.strip
        end
        data = {
          id: cells[2].at("a").attributes["href"].value,
          publish_data: cells[0].inner_text.strip.sub('вчера', yesterday.to_s).sub('днес', today.to_s),
          text_body: cells[2].inner_text.strip.sub(cells[2].inner_html.split("<br>")[2].strip, '').strip,
          location: cells[2].inner_html.split("<br>")[2].strip,
          company_name: comp_name,
          company_href: comp_href,
          week: cur_week,
          year: cur_year,
          month: cur_month
        }
        ScraperWiki::save_sqlite(unique_keys=['id','week', 'year', 'month'], data, table_name="all_possitions", verbose=0)
        saved_rows = saved_rows + 1
      end
    end
    cur_page = cur_page + 20
    rows     = rows - 20
    p rows.to_s + ' -> ' + cur_page.to_s + '(' + saved_rows.to_s + ')'
  end
else
  p 'ALL -> 0'
end



