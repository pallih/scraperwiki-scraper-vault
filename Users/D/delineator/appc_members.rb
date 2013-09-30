###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
starting_url = 'http://www.appc.org.uk/index.cfm/pcms/site.membership_code_etc.membership/'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <td> tags
doc = Hpricot(html)
doc.search('a').each do |a|
  if a.inner_html[/font/]
    name = a.at('font').inner_html
    if name.strip.size > 0
      puts name
      puts url = a['href']
      record = {'name' => name, 'url' => url}
#      ScraperWiki.save(['name','url'], record)
    end
  end
end
###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
starting_url = 'http://www.appc.org.uk/index.cfm/pcms/site.membership_code_etc.membership/'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <td> tags
doc = Hpricot(html)
doc.search('a').each do |a|
  if a.inner_html[/font/]
    name = a.at('font').inner_html
    if name.strip.size > 0
      puts name
      puts url = a['href']
      record = {'name' => name, 'url' => url}
#      ScraperWiki.save(['name','url'], record)
    end
  end
end
