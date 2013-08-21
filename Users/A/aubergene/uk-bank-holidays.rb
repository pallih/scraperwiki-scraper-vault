require 'nokogiri'
require 'date'

def scrape_table(table)
  rows = table.css("tr")
  region = rows[0].at_css("th").inner_text.tr("\302\240",' ').strip
  years = rows[0].css("th")[1..-1].map { |x| x.inner_text.gsub(/\D/,'') }
  puts region

  last_key = ""

  rows[1..-2].each do |row|
    cells = row.css("td")
    # puts cells.inspect
    years.each do |year|    
      comment = cells[0].inner_text.strip
      comment.gsub!("(", " (")
      comment.squeeze!(" ")
      comment.strip!

      day_month = cells[1].inner_text.sub('*','')
      next if day_month =~ /-/ || day_month == ""

      date = Date.parse(day_month + " " + year).to_s
      substitute = !!(cells[1].inner_text =~ /\*/)
      # ScraperWiki.save(["region", "date"], { "region" => region, "date" => date, "comment" => comment, "substitute" => substitute}, date)
      data = { "region-date" => "#{region} #{date}", "region" => region, "date" => date, "comment" => comment, "substitute" => substitute }
      # puts data.inspect
      # I created the composite string key region-date as it seemed there were issues with saving using two keys 
      ScraperWiki.save_sqlite(["region-date"], data)
    end
  end
end

url = 'http://www.direct.gov.uk/en/Governmentcitizensandrights/LivingintheUK/DG_073741'
doc = Nokogiri::HTML(ScraperWiki.scrape(url))
doc.css('table.markuptable').take(2).each do |t|
  scrape_table(t)
end

url = 'http://www.nidirect.gov.uk/index/government-citizens-and-rights/living-in-northern-ireland/bank-holidays.htm'
doc = Nokogiri::HTML(ScraperWiki.scrape(url))
scrape_table(doc.at_css('table.simple'))

