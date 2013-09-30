require 'hpricot'
require 'date'

def scrape_table(table)
  rows = table.search("tr")
  region = rows[0].at("th").inner_text.strip
  years = rows[0].search("th").map { |x| x.inner_text.gsub(/\D/,'') }
  puts "Region:" + region

  last_key = ""

  rows[1..-1].each do |row|
    cells = row.search("td")

    comment = cells[0].inner_text.strip
    comment.gsub!("(", " (")
    comment.squeeze!(" ")
    comment.strip!

    puts "  Row:" + comment

    # puts cells.inspect
    (1..cells.size - 1).each do |i|
      col = cells[i]
      year = years[i]

      puts "    " + year + "::" + col.inner_html

      day_month = col.inner_text.sub('*','')
      next if day_month =~ /-/
      next if day_month == ""
      date = Date.parse(day_month + " " + year)
      substitute = !!(col.inner_text =~ /\*/)
      ScraperWiki.save(["region", "date"], { "region" => region, "date" => date, "comment" => comment, "substitute" => substitute}, date)
    end
  end
end


url = 'http://www.direct.gov.uk/en/Governmentcitizensandrights/LivingintheUK/DG_073741'
html = ScraperWiki.scrape(url)
doc = Hpricot(html)
doc.search('table.markuptable').take(2).each do |t|
    scrape_table(t)
end

url = 'http://www.nidirect.gov.uk/index/government-citizens-and-rights/living-in-northern-ireland/bank-holidays.htm'
html = ScraperWiki.scrape(url)
doc = Hpricot(html)
scrape_table(doc.search('table.simple').take(1))


require 'hpricot'
require 'date'

def scrape_table(table)
  rows = table.search("tr")
  region = rows[0].at("th").inner_text.strip
  years = rows[0].search("th").map { |x| x.inner_text.gsub(/\D/,'') }
  puts "Region:" + region

  last_key = ""

  rows[1..-1].each do |row|
    cells = row.search("td")

    comment = cells[0].inner_text.strip
    comment.gsub!("(", " (")
    comment.squeeze!(" ")
    comment.strip!

    puts "  Row:" + comment

    # puts cells.inspect
    (1..cells.size - 1).each do |i|
      col = cells[i]
      year = years[i]

      puts "    " + year + "::" + col.inner_html

      day_month = col.inner_text.sub('*','')
      next if day_month =~ /-/
      next if day_month == ""
      date = Date.parse(day_month + " " + year)
      substitute = !!(col.inner_text =~ /\*/)
      ScraperWiki.save(["region", "date"], { "region" => region, "date" => date, "comment" => comment, "substitute" => substitute}, date)
    end
  end
end


url = 'http://www.direct.gov.uk/en/Governmentcitizensandrights/LivingintheUK/DG_073741'
html = ScraperWiki.scrape(url)
doc = Hpricot(html)
doc.search('table.markuptable').take(2).each do |t|
    scrape_table(t)
end

url = 'http://www.nidirect.gov.uk/index/government-citizens-and-rights/living-in-northern-ireland/bank-holidays.htm'
html = ScraperWiki.scrape(url)
doc = Hpricot(html)
scrape_table(doc.search('table.simple').take(1))


