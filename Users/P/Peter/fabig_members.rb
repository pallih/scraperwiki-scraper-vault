# FABIG members are derived from a broad spectrum of the oil and gas industry and include oil and gas companies, consultants, contractors, regulators, verifiers, manufacturers and university researchers. FABIG membership provides an opportunity to network with the relevant people in the industry through participation in FABIG technical meetings, FABIG steering committee, FABIG projects and FABIG newsletters.



require 'mechanize'


begin

agent = Mechanize.new
agent.get("http://www.fabig.com/About/Members.htm")

page = agent.page

#Scrape data here...
    data_table = Nokogiri::HTML(page.body).css('tr').collect do |row|
        record = {}
        record['Company']       = row.css('td.MemberInfo').inner_text.strip
        record['Contact']       = row.css('td.MemberContact').inner_text.strip
        record['Link']   = row.css('td.MemberLink a').map {|link| link['href'].strip}
        record['Link'] = record['Link'].first

        ScraperWiki.save(["Company"], record)

        puts record
    end



rescue
retry
rescue Timeout::Error
retry
end# FABIG members are derived from a broad spectrum of the oil and gas industry and include oil and gas companies, consultants, contractors, regulators, verifiers, manufacturers and university researchers. FABIG membership provides an opportunity to network with the relevant people in the industry through participation in FABIG technical meetings, FABIG steering committee, FABIG projects and FABIG newsletters.



require 'mechanize'


begin

agent = Mechanize.new
agent.get("http://www.fabig.com/About/Members.htm")

page = agent.page

#Scrape data here...
    data_table = Nokogiri::HTML(page.body).css('tr').collect do |row|
        record = {}
        record['Company']       = row.css('td.MemberInfo').inner_text.strip
        record['Contact']       = row.css('td.MemberContact').inner_text.strip
        record['Link']   = row.css('td.MemberLink a').map {|link| link['href'].strip}
        record['Link'] = record['Link'].first

        ScraperWiki.save(["Company"], record)

        puts record
    end



rescue
retry
rescue Timeout::Error
retry
end