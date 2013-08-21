require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'
require 'httparty'

#ScraperWiki.sqliteexecute('CREATE TABLE `swdata` (`url` text, `uid` text, `description` text, `date_scraped` text,`date` text)')
#ScraperWiki.sqliteexecute('CREATE INDEX updated ON swdata (updated)')
#exit
#ScraperWiki.sqliteexecute('CREATE TABLE `comments` (`problemid` text, `commentid` text, `author` text, `date` text,`time` text, `comment` text, `status` text)');
#exit

def search_for_new_reports(until_date=Date.today)

  url = "http://www.fixmystreet.com/open311/v2/requests.xml?jurisdiction_id=fiksgatami.no&agency_responsible=2434%7C2240&start_date=#{(until_date - 14).strftime('%Y-%m-%d')}&end_date=#{until_date.strftime('%Y-%m-%d')}"

  doc = Nokogiri::XML HTTParty.get(url).response.body

  rows = []
  count = 0

  doc.search('request').each do |i|
    rows << i.children.inject({}){|hsh,el| hsh[el.name] = el.inner_text;hsh}
  end

  rows.each do |row|

      if row["agency_responsible"].strip == "Staffordshire County Council"
        subdomain = "www"
      else
        subdomain = "lichfielddc"
      end

      details = {
        :uid => row["service_request_id"],
        :url => "http://#{subdomain}.fixmystreet.com/report/#{row['service_request_id']}",
        :council => row["agency_responsible"].strip,
        :description => row["description"],
        :detail => row["detail"],
        :sent => Date.parse(row["agency_sent_datetime"]),
        :lat => row["lat"],
        :lng => row["long"],
        :requested => Date.parse(row["requested_datetime"]),
        :service => row["service_name"],
        :title => row["title"],
        :status => row["status"],
        :updated => Date.parse(row["updated_datetime"])
      }

      ScraperWiki.save([:uid], details)

  end

end

def update_comments
  current_reports = ScraperWiki.select("* from swdata WHERE updated > '#{(Date.today-60).strftime('%F')}' LIMIT 500")
  current_reports.each do |report|
    get_comments(report)
  end
end

def get_comments(info)
  
  url = info['url']

  begin

    doc = Nokogiri.HTML(open(url))
  
    details = nil
  
    comments = doc.search('//*[@id="updates"]/div')
  
    comments.each do |comment|
      
      meta = comment.search('em')[0].inner_text.scan(/Posted [by ]*(.+) at ([0-9]+:[0-9]+),* ([a-zA-Z]+[ ]+*[0-9]+*[ ]+*[a-zA-Z]+*[ ]+*[0-9]+*)[, marked as ]*([a-z ]+)*/)[0]
  
      unless meta.nil? 
  
        details = {}
  
        details[:problemid] = info['uid']
        details[:commentid] = comment.search('a')[0][:name]
        details[:author] = meta[0]
  
        if meta[2] == "today"
          Date.today
        else
          details[:date] = Date.parse(meta[2])
        end
  
        details[:time] = meta[1]
        details[:comment] = comment.search('.update-text').inner_text.strip
        details[:status] = meta[3]
  
        ScraperWiki::save_sqlite([:commentid], details, table_name="comments")
  
      end
    end

  rescue Exception => e
    puts e.message  
    puts e.backtrace.inspect 
  end

  # Save problem with latest status
  unless details.nil? 
    info['status'] = details[:status]
    ScraperWiki::save_sqlite([:uid], info, table_name="swdata")
  end

end

#52.times do |i| 
 #search_for_new_reports(Date.today - (10*(i+i)))
#end

search_for_new_reports
update_comments
