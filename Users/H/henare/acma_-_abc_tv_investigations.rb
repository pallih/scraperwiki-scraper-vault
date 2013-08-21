require 'rubygems'
require 'mechanize'

agent = Mechanize.new
url = 'http://www.acma.gov.au/WEB/STANDARD/pc=PC_310290'

page = agent.get(url)

page.at('table tbody').search('tr').each do |r|
  # Some cells have empty links to download Acrobat. Bizzare
  links = r.search('td')[1].search('a')
  report_id = links.size > 1 ? links[-1].inner_text : links[0].inner_text
  # And one or two have links that say "Word" or "PDF" so we try this
  report_id = r.search('td')[1].inner_text.scan(/\d+\d+\d/)[0] if report_id.to_i.zero? 

  # Do the same to get the report URL
  relative_url = links.size > 1 ? links[-1].attribute('href') : links[0].attribute('href')
  report_url = page.uri + URI.parse(relative_url.to_s.gsub(' ', '%20'))

  investigation = {
    'report_id' => report_id,
    'call_sign' => r.search('td')[0].inner_text.strip,
    'broadcaster' => 'ABC',
    'programme' => r.search('td')[1].at('em').inner_text.strip,
    'report_url' => report_url,
    'date_published' => Date.parse(r.search('td')[3].inner_text.strip).to_s
  }

  # Get all the outcomes for a report
  r.search('td')[2].inner_text.strip.scan(/No Breach .*|Breach .*/i).each do |o|
    # Check if this was determined to be a breach or not
    breach = case o.split("\u2013")[0].strip.downcase
    when "breach"
      true
    when "no breach"
      false
    # Handle unusual scenario where it's a normal '-'
    when /no breach -/
      outcomes = o.split(' - ')[1..-1].join
      false
    else
      raise "Could not understand this outcome's determination: #{o.split('\342\200\223')[0].strip}"
    end

    outcomes = o.split("\u2013")[1..-1].join('-').strip.split(';') if !outcomes

    # When outcomes have semicolons, it's different sections being
    # referred to so we create multiple outcomes
    outcomes.each do |s|
      outcome = {
        'key' => report_id + s.strip.downcase.gsub(' ', '_'),
        'report_id' => report_id,
        'section' => s.strip,
        'breach' => breach
      }

      ScraperWiki.save_sqlite(['key'], outcome, 'outcomes')
    end
  end

  ScraperWiki.save_sqlite(['report_id'], investigation, 'investigations')
end
