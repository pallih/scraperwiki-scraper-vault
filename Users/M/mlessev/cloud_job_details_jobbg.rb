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

#ScraperWiki::sqliteexecute("drop table if exists it_glossary")
#ScraperWiki::sqliteexecute("CREATE TABLE it_glossary (`gloss` text, `word` text, `abbr` text, `key` text, `word_link` text)")
#ScraperWiki::sqliteexecute("insert into it_glossary select gloss, word, abbr, key, word_link from it_glossary.it_glossary")



# ScraperWiki::sqliteexecute("drop table if exists cloud_job_details_fts")
# ScraperWiki::sqliteexecute("CREATE VIRTUAL TABLE cloud_job_details_fts USING fts3(id text, key text, value text)")
# ScraperWiki::sqliteexecute("INSERT INTO cloud_job_details_fts select id, key, value from cloud_job_details")

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword in ('AWS+C3') ")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where id not in (select id from cloud_possitions)")

#ScraperWiki::commit()

words = ['cloud', 'IaaS', 'PaaS', 'SaaS', 'azure', 'Amazon+Web+Services', 'AWS+API', 'AWS+EC2', 'AWS+S3', 'Google+App+Engine', 'Rackspace', 'OpenStack', 'PHP+Fog', 'Heroku', 'AppHarbor', 'Salesforce', 'NoSQL', 'Exadata', 'Exalogic', 'Joyent', 'Cloud+Foundry', 'Terremark', 'GoGrid', 'Navisite', 'IBM+SmartCloud', 'OpSource', 'Dimension+Data+cloud', 'oracle+cloud', 'scraperwiki', 'SAP+Hana', 'Savvis', 'Bluelock', 'Engineyard', 'OpenShift', 'CloudBees', 'CloudSwing']



#ScraperWiki::sqliteexecute("drop table if exists cloud_job_details")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where 1=1")
#ScraperWiki::sqliteexecute("VACUUM")

today = Date.today(sg=Date::ITALY).to_s
yesterday = (Date.today(sg=Date::ENGLAND) -1).to_s
cur_week = Date.today(sg=Date::ITALY).cweek.to_s
cur_year = Date.today(sg=Date::ITALY).year.to_s
cur_month = Date.today(sg=Date::ITALY).month.to_s
  
# get cloud open possitions
words.each do |word|
  cond = word
  url = "http://www.jobs.bg/front_job_search.php?frompage=0&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  url_pages = "http://www.jobs.bg/front_job_search.php?frompage=$$$##mm&str_regions=&str_locations=&tab=jobs&old_country=&country=-1&region=0&l_category[]=0&keyword=" + cond
  #url_pages.force_encoding("UTF-8")
  
  doc_page = Nokogiri.HTML(open(url))
  
  total_rows = doc_page.search 'table[@width="980"]/tr/td[@class="pagingtotal"]'

  #p total_rows

  if total_rows.empty? == false then
  
    rows = total_rows[0].inner_text.strip.split("\u043E\u0442")[1].to_i
    cur_page = 0
    p cond + ' -> ' + rows.to_s
    
    while rows > 0
      doc = Nokogiri.HTML(open(url_pages.sub('$$$##mm', cur_page.to_s)))
    
      doc.search('table[@width="670"]/tr').each do |v|
        cells = v.search 'td'
        if cells.count == 5 or cells.count == 7
          if cells[4].inner_html.include? '<table' 
            comp_iner = cells[4].search 'table/tr/td'[1]  #rescue comp_name = cells[4].inner_text.strip
            comp_href = comp_iner.at("a").attributes["href"].value rescue comp_href = cells[4].at("a").attributes["href"].value
            comp_name = comp_iner.at("a").inner_text.strip         rescue comp_name = cells[4].inner_text.strip
          else
            comp_name = cells[4].inner_text.strip
            comp_href = cells[4].at("a").attributes["href"].value  rescue comp_href = cells[4].inner_text.strip
          end
          if cells[2].at("a").attributes["href"].value.length > 10
            cur_link = cells[2].at("a").attributes["href"].value
          else
            cur_link = 'http://www.jobs.bg/' + cells[2].at("a").attributes["href"].value
          end

          doc_inner = Nokogiri.HTML(open(cur_link))

          detiles = doc_inner.search 'table[@width="670"]/tr/td[@style="font-size:12px;"]'
          if detiles.inner_text.strip != ''
            inner_data = {
              id: cells[2].at("a").attributes["href"].value,
              key: detiles.inner_text.strip,
              value: detiles.inner_html.strip
            }
            #puts inner_data.to_json
            ScraperWiki::save_sqlite(unique_keys=['id'], inner_data, table_name="cloud_job_details", verbose=0)
          else
#            p cur_link

            detiles = doc_inner.search 'table[@width="980"]'
            if detiles.inner_text.strip != ''
              inner_data = {
                id: cells[2].at("a").attributes["href"].value,
                key: '',
                value: detiles.inner_html.strip
              }
            else
              inner_data = {
                id: cells[2].at("a").attributes["href"].value,
                key: '',
                value: doc_inner.inner_html.strip
              }
            end
            #puts inner_data.to_json
            ScraperWiki::save_sqlite(unique_keys=['id'], inner_data, table_name="cloud_job_details", verbose=0)

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
        end
      end
      
      cur_page = cur_page + 20
      rows     = rows - 20
      # p rows.to_s + ' -> ' + cur_page.to_s
    end
  else
    p cond  + ' -> 0'
  end
  #p rows
end  


