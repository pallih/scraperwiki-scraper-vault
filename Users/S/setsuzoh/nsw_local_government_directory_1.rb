require 'mechanize'

def extract_council(start)
  record = {:name => start.inner_text}
  line = start.next_sibling
  until line.nil? || line["class"] == "txtStandardTitle" do
    #puts line
    case(line)
    when /Email/i
      record[:email] = line.next_sibling.inner_text
    when /Web/i
      record[:website] = line.next_sibling.inner_text
    end
    line = line.next_sibling
  end
  ScraperWiki.save_sqlite(['name'], record)
end

agent = Mechanize.new
page = agent.get("http://www.dlg.nsw.gov.au/dlg/dlghome/dlg_LocalGovDirectory.asp?index=1&CN=ALL")

page.search('.txtStandardTitle').each do |start|
  extract_council(start)
end

