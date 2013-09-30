###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
starting_url = 'http://epaca.org/en/about-epaca/epaca-members/'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <td> tags
doc = Hpricot(html)
(doc/ 'tr').each do |row|
  cells = (row/ 'td')
  if cells[0]
    company = cells[0].inner_text
    uri = cells[0].at('a')['href']
    contact = cells[1].inner_text
    puts cells[1]
    email = cells[2].at('a')['href']
    record = {'company' => company, 'website' => uri, 'contact' => contact, 'email' => email}
    ScraperWiki.save(['company','website','contact','email'], record)
  end
end
###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
starting_url = 'http://epaca.org/en/about-epaca/epaca-members/'
html = ScraperWiki.scrape(starting_url)

# use Hpricot to get all <td> tags
doc = Hpricot(html)
(doc/ 'tr').each do |row|
  cells = (row/ 'td')
  if cells[0]
    company = cells[0].inner_text
    uri = cells[0].at('a')['href']
    contact = cells[1].inner_text
    puts cells[1]
    email = cells[2].at('a')['href']
    record = {'company' => company, 'website' => uri, 'contact' => contact, 'email' => email}
    ScraperWiki.save(['company','website','contact','email'], record)
  end
end
