require 'mechanize'

agent = Mechanize.new

page = agent.get("http://www.directory.nsw.gov.au/completelist.asp")

links = {}
page.search('#cim_content-wrapper ul').each do |ul|
  ul.search('li a').each do |a|
    name = a.inner_html
    link = "http://www.directory.nsw.gov.au/" + a["href"]
    links[name] = link
  end
end

links.each do |name, link|
  page = agent.get(link)
  record = {:name => name}
  page.search('.bCard tr').each do |tr|
    label = tr.search('td')[0].inner_text
    value = tr.search('td')[1].inner_text if tr.search('td')[1]
    case(label)
    when /Email/
      record[:email] = value
    when /Website/
      record[:website] = value
    end
  end
  ScraperWiki.save_sqlite(['name'], record)
end