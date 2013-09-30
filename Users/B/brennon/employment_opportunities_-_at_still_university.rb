require 'nokogiri'

html = ScraperWiki.scrape("http://www.atsu.edu/contact/jobs/display.asp")

doc = Nokogiri::HTML(html)

for v in doc.search("div.container tr[@valign=top]")

  cells = v.search('td')

  department = cells[0].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  title = cells[1].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  base_pay = cells[2].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  shift = cells[3].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  week_hours = cells[4].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  requirements = cells[5].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  additional_information = cells[6].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')

  data = {
    'department' => department,
    'title' => title,
    'base_pay' => base_pay,
    'shift' => shift,
    'week_hours' => week_hours,
    'requirements' => requirements,
    'additional_information' => additional_information,
    'link' => 'http://www.atsu.edu/contact/jobs/display.asp'
  }

  ScraperWiki.save_sqlite(unique_keys=['department','title','base_pay','shift','week_hours','requirements','additional_information'], data=data)
end


require 'nokogiri'

html = ScraperWiki.scrape("http://www.atsu.edu/contact/jobs/display.asp")

doc = Nokogiri::HTML(html)

for v in doc.search("div.container tr[@valign=top]")

  cells = v.search('td')

  department = cells[0].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  title = cells[1].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  base_pay = cells[2].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  shift = cells[3].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  week_hours = cells[4].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  requirements = cells[5].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')
  additional_information = cells[6].inner_html.gsub(/&amp;nbsp/i, '').gsub(/^\*\*$/,'NULL')

  data = {
    'department' => department,
    'title' => title,
    'base_pay' => base_pay,
    'shift' => shift,
    'week_hours' => week_hours,
    'requirements' => requirements,
    'additional_information' => additional_information,
    'link' => 'http://www.atsu.edu/contact/jobs/display.asp'
  }

  ScraperWiki.save_sqlite(unique_keys=['department','title','base_pay','shift','week_hours','requirements','additional_information'], data=data)
end


