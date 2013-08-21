###############################################################################
# ASP.Net Scraper
###############################################################################

require 'mechanize'

agent = Mechanize.new { |a| 
  a.user_agent_alias = 'Mac Safari'
}

page = agent.get('http://www.bcct.ca/MemberServices/FindATeacher.aspx')

('A'..'Z').each do |letter|
  
  postback = ""
  until postback == nil
    f = page.form_with(:name => 'Form1')
    f.txtboxSurname = letter
    f['btnSearch'] = 'Search' if postback == ""
    f['__EVENTTARGET'] = postback
    page = f.submit

    doc = Nokogiri::HTML(page.body)
    doc.search('div#divSearchResult tr').each_with_index do |row,i|
      next unless row
      next if row['class'] and row['class'] == "headerRegister"   # header
      next if row['align'] and row['align'] == "center"           # footer
      next unless row.css('td').length == 2
    
      last_name = row.css('td')[0].inner_html.strip
      first_name = row.css('td')[1].inner_html.strip
      puts "#{first_name} #{last_name}"
      ScraperWiki.save(['first_name','last_name'], {'first_name' => first_name, 'last_name' => last_name})
    end
    
    if link = page.link_with(:text => /\[Next\]/)
      postback = link.href.match(/PostBack\('([^']+)'/)[1]
    else
      postback = nil
    end
      
  end
end
