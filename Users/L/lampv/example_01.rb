# Blank Ruby
require 'rubygems'
require 'mechanize'

starting_url = 'http://www.eservices.lmc.nsw.gov.au/DATrackingUI/Modules/Applicationmaster/default.aspx?page=found&1=thismonth&6=F'
#starting_url = 'https://epathway.newengland.nsw.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySearch.aspx'
comment_url = 'mailto:leichhardt@lmc.nsw.gov.au?subject='

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def scrape_table(doc, comment_url)
  doc.search('table tbody tr').each do |tr|
    puts tr.inspect
    # Columns in table
    # Show  Number  Submitted  Details
    tds = tr.search('td')

    #puts tds.inspect
    #puts tds[0].inspect
    #puts doc.uri.to_s
    #puts (tds[0].at('a')['href']).to_s
    #puts (doc.uri + tds[0].at('a')['href']).to_s

    h = tds.map{|td| td.inner_html}

    #puts h.inspect
    #puts h[1].inspect
    #puts clean_whitespace(h[1])
  
    record = {
      'info_url' => (doc.uri + tds[0].at('a')['href']).to_s,
      'comment_url' => comment_url + CGI::escape("Development Application Enquiry: " + clean_whitespace(h[1])),
      'council_reference' => clean_whitespace(h[1]),
      'date_received' => Date.strptime(clean_whitespace(h[2]), '%d/%m/%Y').to_s,
      'address' => clean_whitespace(tds[3].at('b').inner_text),
      'description' => CGI::unescapeHTML(clean_whitespace(h[3].split('<br>')[1..-1].join)),
      'date_scraped' => Date.today.to_s
    }
    #puts record.inspect
    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      #puts "Skipping already saved record " + record['council_reference']
    end
  end
end

def scrape_and_follow_next_link(doc, comment_url)
  puts "doc"
  puts doc.inspect
  scrape_table(doc, comment_url)
  next_button = doc.at('.rgPageNext')
  puts   next_button

  puts next_button.inspect
  puts "pvlamkhtn"  
  puts (next_button['onclick'] =~ /return false/).nil? 
  
  if next_button.nil? || (next_button['onclick'] =~ /return false/).nil? 
    puts "aaaaaaa"
    return
  end
  
  while !next_button.nil? do
    puts "test"
    puts next_button.inspect
    form = doc.forms.first
    
    # The joy of dealing with ASP.NET
    form['__EVENTTARGET'] = next_button['name']
    form['__EVENTARGUMENT'] = ''
    # It doesn't seem to work without these stupid values being set.
    # Would be good to figure out where precisely in the javascript these values are coming from.
    form['ctl00%24RadScriptManager1']=
      'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
    form['ctl00_RadScriptManager1_HiddenField']=
      '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'
    doc = form.submit(form.button_with(:name => next_button['name']))
    scrape_table(doc, comment_url)
    next_button = doc.at('.rgPageNext')
  
    puts "bbbbb"
  end
  puts "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  
end

##
#
#
def get_list_of_da(doc, comment_url)
  list_page = []
  next_button = doc.at('.rgPageNext')
  flag = true
  while(flag) do
    unless next_button.nil? || next_button['onclick'] =~ /return false/
        scrape_table(doc, comment_url)
        form = doc.forms.first
      
      # The joy of dealing with ASP.NET
      form['__EVENTTARGET'] = next_button['name']
      form['__EVENTARGUMENT'] = ''
      # It doesn't seem to work without these stupid values being set.
      # Would be good to figure out where precisely in the javascript these values are coming from.
      form['ctl00%24RadScriptManager1']=
        'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
      form['ctl00_RadScriptManager1_HiddenField']=
          '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'

      list_page << doc

      doc = form.submit(form.button_with(:name => next_button['name']))
      next_button = doc.at('.rgPageNext')
    else
      puts "FALSE"
      flag = false
    end
  end
  puts list_da.length
end


agent = Mechanize.new

# Jump through bollocks agree screen
doc = agent.get(starting_url)
doc = doc.forms.first.submit(doc.forms.first.button_with(:value => "I Agree"))
doc = agent.get(starting_url)
puts doc.inspect

#puts doc.body.inspect
form = doc.forms.first
puts form.inspect
#next_button = doc.at('.rgPageNext')
#puts next_button



#get_list_of_da(doc, comment_url)

#scrape_and_follow_next_link(doc, comment_url)
# Blank Ruby
require 'rubygems'
require 'mechanize'

starting_url = 'http://www.eservices.lmc.nsw.gov.au/DATrackingUI/Modules/Applicationmaster/default.aspx?page=found&1=thismonth&6=F'
#starting_url = 'https://epathway.newengland.nsw.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquirySearch.aspx'
comment_url = 'mailto:leichhardt@lmc.nsw.gov.au?subject='

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def scrape_table(doc, comment_url)
  doc.search('table tbody tr').each do |tr|
    puts tr.inspect
    # Columns in table
    # Show  Number  Submitted  Details
    tds = tr.search('td')

    #puts tds.inspect
    #puts tds[0].inspect
    #puts doc.uri.to_s
    #puts (tds[0].at('a')['href']).to_s
    #puts (doc.uri + tds[0].at('a')['href']).to_s

    h = tds.map{|td| td.inner_html}

    #puts h.inspect
    #puts h[1].inspect
    #puts clean_whitespace(h[1])
  
    record = {
      'info_url' => (doc.uri + tds[0].at('a')['href']).to_s,
      'comment_url' => comment_url + CGI::escape("Development Application Enquiry: " + clean_whitespace(h[1])),
      'council_reference' => clean_whitespace(h[1]),
      'date_received' => Date.strptime(clean_whitespace(h[2]), '%d/%m/%Y').to_s,
      'address' => clean_whitespace(tds[3].at('b').inner_text),
      'description' => CGI::unescapeHTML(clean_whitespace(h[3].split('<br>')[1..-1].join)),
      'date_scraped' => Date.today.to_s
    }
    #puts record.inspect
    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      #puts "Skipping already saved record " + record['council_reference']
    end
  end
end

def scrape_and_follow_next_link(doc, comment_url)
  puts "doc"
  puts doc.inspect
  scrape_table(doc, comment_url)
  next_button = doc.at('.rgPageNext')
  puts   next_button

  puts next_button.inspect
  puts "pvlamkhtn"  
  puts (next_button['onclick'] =~ /return false/).nil? 
  
  if next_button.nil? || (next_button['onclick'] =~ /return false/).nil? 
    puts "aaaaaaa"
    return
  end
  
  while !next_button.nil? do
    puts "test"
    puts next_button.inspect
    form = doc.forms.first
    
    # The joy of dealing with ASP.NET
    form['__EVENTTARGET'] = next_button['name']
    form['__EVENTARGUMENT'] = ''
    # It doesn't seem to work without these stupid values being set.
    # Would be good to figure out where precisely in the javascript these values are coming from.
    form['ctl00%24RadScriptManager1']=
      'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
    form['ctl00_RadScriptManager1_HiddenField']=
      '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'
    doc = form.submit(form.button_with(:name => next_button['name']))
    scrape_table(doc, comment_url)
    next_button = doc.at('.rgPageNext')
  
    puts "bbbbb"
  end
  puts "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  
end

##
#
#
def get_list_of_da(doc, comment_url)
  list_page = []
  next_button = doc.at('.rgPageNext')
  flag = true
  while(flag) do
    unless next_button.nil? || next_button['onclick'] =~ /return false/
        scrape_table(doc, comment_url)
        form = doc.forms.first
      
      # The joy of dealing with ASP.NET
      form['__EVENTTARGET'] = next_button['name']
      form['__EVENTARGUMENT'] = ''
      # It doesn't seem to work without these stupid values being set.
      # Would be good to figure out where precisely in the javascript these values are coming from.
      form['ctl00%24RadScriptManager1']=
        'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
      form['ctl00_RadScriptManager1_HiddenField']=
          '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'

      list_page << doc

      doc = form.submit(form.button_with(:name => next_button['name']))
      next_button = doc.at('.rgPageNext')
    else
      puts "FALSE"
      flag = false
    end
  end
  puts list_da.length
end


agent = Mechanize.new

# Jump through bollocks agree screen
doc = agent.get(starting_url)
doc = doc.forms.first.submit(doc.forms.first.button_with(:value => "I Agree"))
doc = agent.get(starting_url)
puts doc.inspect

#puts doc.body.inspect
form = doc.forms.first
puts form.inspect
#next_button = doc.at('.rgPageNext')
#puts next_button



#get_list_of_da(doc, comment_url)

#scrape_and_follow_next_link(doc, comment_url)
