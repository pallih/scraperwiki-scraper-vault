require 'nokogiri'
require 'open-uri'

contents_base="http://omnimagindex.wordpress.com/tables-of-contents-2"

volume_slugs = ["volume-1-october-1978-to-september-1979"]

16.times do |i|
  volume_slugs << "volume-#{i+2}"
end

volume_slugs.each do |slug|
  puts "Processing #{contents_base}/#{slug}"
  page = Nokogiri::HTML( ScraperWiki.scrape( "#{contents_base}/#{slug}" ) ) 
  page.search("div.entry-content tr")[2..-1].each do |row|
    #columns are 
    # Vol.:No.  
    # YYYY:MM (occasionally has _ rather than :)
    # Page (start page only) 
    # Title  
    # Section  
    # Author (may not be present)
    vol_no = row.element_children[0]
    if vol_no.content.include?(":")
      volume, number = vol_no.content.split(":")
    else
      volume, number = vol_no.content.split("_")
    end

    year_month = row.element_children[1]
    if year_month.content.include?(":")
      year, month = year_month.content.split(":")
    else
      year, month = year_month.content.split("_")
    end

    page = row.element_children[2].content
    title = row.element_children[3].content
    section = row.element_children[4].content
    author = row.element_children[5].content
    article = {
       "id" => "#{year}/#{month}/#{page}",
       "year" => year,
       "month" => month,
       "volume" => volume,
       "number" => number,
       "page" => page,
       "title" => title,
       "section" => section,
       "author" => author
    }
    ScraperWiki.save_sqlite(unique_keys=['id'], data=article) 
  end
end
