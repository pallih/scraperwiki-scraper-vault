# Blank Ruby
require 'open-uri'
require 'pdf/reader'
require 'nokogiri'


#ScraperWiki.sqliteexecute('DELETE from notice_ids')
#ScraperWiki.commit
#exit
#pdf_url = 'http://www.etat.lu/memorial/2012/C/Pdf/c1750127.pdf'
#notice_id = '2012081701/2490'
#edition = '1750'
#year = '2012'
#data = {:full_notice_id => "#{year}-#{edition}-#{notice_id}", :notice_id => notice_id, :date_scraped => #Time.now, :pdf_url => pdf_url}
#ScraperWiki.save_sqlite([:full_notice_id], data, "notice_ids") 
#ScraperWiki.save_var('latest_edition_parsed', year + edition)
#exit

def extract_notice_pdfs_for(year)
  doc = Nokogiri.HTML(open "http://www.legilux.public.lu/entr/archives/index.php?year=#{year}")
  links = doc.search('table[@width="614"] a[@href*=".pdf"]')
  data = links.collect do |link| 
    edition_no = link.inner_text.scan(/\d+$/).flatten.first; 
    {:url => link[:href], :id => "#{year}#{edition_no}".to_i}
  end
  ScraperWiki.save_sqlite([:id], data, "editions")
end

def extract_notice_ids_from_pdf(pdf_url, edition_id)
  io     = open(pdf_url, 'r', :read_timeout=>600) # sometimes very big slow files

  reader = PDF::Reader.new(io)
  notice_ids = []
  year, edition = edition_id.to_s[0..3], edition_id.to_s[4..-1]

  puts "About to starting parsing notice_urls from pdf at #{pdf_url}"
  reader.pages.each do |page|
    new_ids = page.text.scan(/R.f.rence de publication: ([\d\/]+)\./).flatten
    next if new_ids.nil? 
    notice_ids += new_ids
  end

  puts "Found #{notice_ids.size} notice ids, #{notice_ids.uniq.size} of which are unique"
  notice_ids.each do |notice_id|  
    data = {:full_notice_id => "#{year}-#{edition}-#{notice_id}", :notice_id => notice_id, :date_scraped => Time.now, :pdf_url => pdf_url}
    ScraperWiki.save_sqlite([:full_notice_id], data, "notice_ids", 3) 
  end
end

extract_notice_pdfs_for(Date.today.year)

if latest_edition_parsed = ScraperWiki.get_var('latest_edition_parsed')
  editions = ScraperWiki.select("* FROM editions WHERE id > #{latest_edition_parsed} ORDER BY id LIMIT 20")
else
  puts "Didn't find latest_edition_parsed"
  editions = ScraperWiki.select('* FROM editions ORDER BY id LIMIT 20')
end

editions.each do |edition|
  puts "About to start extracting notice_ids for #{edition['id']} from #{edition['url']}"
  extract_notice_ids_from_pdf(edition['url'], edition['id'])
  ScraperWiki.save_var('latest_edition_parsed', edition['id'])
end
