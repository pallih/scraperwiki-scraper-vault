require 'hpricot'
require 'open-uri'

def url
  "http://www.useit.com/alertbox/"
end

def parse_alertbox_page(page)
  div = page.search("div.maintext")

  # Retrieve content and remove unecessary stuff
  title = div.search("h1").remove.inner_html
  date = parse_date_paragraph(div.search("p.overline").remove)
  content = div.inner_html

  # Fix image urls
  content.gsub!(/src="(\/.*)"/, "src=\"#{url.gsub("alertbox/","")}\\1\"")
  content.gsub!(/src="(.*)"/, "src=\"#{url}\\1\"")

  [title, date, content]
end

# Parses the date from the top paragraph of the Alertbox article
def parse_date_paragraph(p)
  s = p.search("strong").inner_html.split("Alertbox, ").last
  date = ParseDate.parsedate(s)
  Time.mktime(*date)
end

def scrape_it
  Hpricot(open(url)).search("li")[0..3].each do |e|
    page_url = url + e.at("a")[:href]
    page = Hpricot(open(page_url))
    title, date, content = parse_alertbox_page(page)
    
    ScraperWiki.save(unique_keys=['link'], {
        "link" => page_url,
        "title" => title,
        "date" => date,
        "description" => content})
  end
end

# Currently disabled
#scrape_it
