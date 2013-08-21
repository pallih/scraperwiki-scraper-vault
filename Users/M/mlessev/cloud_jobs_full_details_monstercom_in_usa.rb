#Cloud jobs full details monster.com in USA

# Blank Ruby
# encoding: utf-8

require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

ScraperWiki::attach("cloud_jobs_details_monstercom")

#ScraperWiki::sqliteexecute("CREATE TABLE cloud_job_details( id TEXT PRIMARY KEY, job_name TEXT, job_link TEXT, key TEXT )")

#ScraperWiki::attach("it_glossary")
#ScraperWiki::sqliteexecute("drop table search_keyword") rescue rr = 0

#ScraperWiki::sqliteexecute("create table cloud_possitions as select * from cloud_jobs_details_monstercom.cloud_possitions")

ScraperWiki::sqliteexecute("create table cloud_job_details2 as select id, job_name, job_link, key from cloud_jobs_details_monstercom.cloud_job_details where rowID between 31001 and 32000")


ScraperWiki::sqliteexecute("insert into cloud_job_details select id, job_name, job_link, key from cloud_job_details2")
ScraperWiki::commit()

ScraperWiki::sqliteexecute("drop table cloud_job_details2") rescue rr = 0

#ScraperWiki::sqliteexecute("delete from cloud_possitions where search_keyword in ('AWS+EC2', 'AWS+C3')")
#ScraperWiki::sqliteexecute("delete from cloud_job_details where id not in (select id from cloud_possitions)")

#ScraperWiki::commit()

