require 'hpricot'

starting_url = 'http://twitter.com/Directgov/ukgov/members'
html = ScraperWiki.scrape(starting_url)

doc = Hpricot(html)
doc.search('.label.screenname/a').each do |a|
  screen_name = a.inner_html
  label = a.at('../..').at('.label.fullname')
  full_name = label ? label.inner_text : nil
  uri = a['href']

  img = a.at('../../../..').at('img')
  thumb_image = img ? img['src'] : nil

  record = {'uri' => uri, 'screen_name' => screen_name, 'full_name' => full_name, 'thumb_image' => thumb_image}
  ScraperWiki.save(['uri'], record)
end
require 'hpricot'

starting_url = 'http://twitter.com/Directgov/ukgov/members'
html = ScraperWiki.scrape(starting_url)

doc = Hpricot(html)
doc.search('.label.screenname/a').each do |a|
  screen_name = a.inner_html
  label = a.at('../..').at('.label.fullname')
  full_name = label ? label.inner_text : nil
  uri = a['href']

  img = a.at('../../../..').at('img')
  thumb_image = img ? img['src'] : nil

  record = {'uri' => uri, 'screen_name' => screen_name, 'full_name' => full_name, 'thumb_image' => thumb_image}
  ScraperWiki.save(['uri'], record)
end
