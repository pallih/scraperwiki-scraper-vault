# Blank Ruby

require 'nokogiri'

skip_urls = ["http://www.angelfire.com/tn/plath/dears.html", "http://www.angelfire.com/tn/plath/babysitters.html",
"http://www.angelfire.com/tn/plath/spa.html",
"http://www.angelfire.com/tn/plath/death.html",
"http://www.angelfire.com/tn/plath/finisterre.html",
"http://www.angelfire.com/tn/plath/lesbos.html",
"http://www.angelfire.com/tn/plath/yad.html"]

# persist urls that have already been scraped.
if (ScraperWiki.get_metadata('urls') != nil)
  done_urls = ScraperWiki.get_metadata('urls').split(",") || [];
else
  done_urls = []
end

urls = []
list = ScraperWiki.scrape("http://www.stanford.edu/class/engl187/docs/plathpoem.html")
doc = Nokogiri::HTML(list)
doc.search('a').each do |a|
  if (a['href'].index("angelfire.com/tn/plath") != nil)
    urls << a['href']
  end
end

if (done_urls == nil)
  done_urls = []
end

puts done_urls
urls = urls - done_urls - skip_urls

urls.each do |url|
  puts "scraping #{url}"
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.search('p').each do |p|
    if (p.inner_html != nil && p.inner_html != "")
      p.inner_html.split('<br>').each do |line|
        puts line
        ScraperWiki.save(unique_keys=['line',], data={'line' => line})
      end
    end
  end
  done_urls << url
  ScraperWiki.save_metadata('urls', done_urls.join(","))
  puts "done with: #{url}"
end

# Blank Ruby

require 'nokogiri'

skip_urls = ["http://www.angelfire.com/tn/plath/dears.html", "http://www.angelfire.com/tn/plath/babysitters.html",
"http://www.angelfire.com/tn/plath/spa.html",
"http://www.angelfire.com/tn/plath/death.html",
"http://www.angelfire.com/tn/plath/finisterre.html",
"http://www.angelfire.com/tn/plath/lesbos.html",
"http://www.angelfire.com/tn/plath/yad.html"]

# persist urls that have already been scraped.
if (ScraperWiki.get_metadata('urls') != nil)
  done_urls = ScraperWiki.get_metadata('urls').split(",") || [];
else
  done_urls = []
end

urls = []
list = ScraperWiki.scrape("http://www.stanford.edu/class/engl187/docs/plathpoem.html")
doc = Nokogiri::HTML(list)
doc.search('a').each do |a|
  if (a['href'].index("angelfire.com/tn/plath") != nil)
    urls << a['href']
  end
end

if (done_urls == nil)
  done_urls = []
end

puts done_urls
urls = urls - done_urls - skip_urls

urls.each do |url|
  puts "scraping #{url}"
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.search('p').each do |p|
    if (p.inner_html != nil && p.inner_html != "")
      p.inner_html.split('<br>').each do |line|
        puts line
        ScraperWiki.save(unique_keys=['line',], data={'line' => line})
      end
    end
  end
  done_urls << url
  ScraperWiki.save_metadata('urls', done_urls.join(","))
  puts "done with: #{url}"
end

