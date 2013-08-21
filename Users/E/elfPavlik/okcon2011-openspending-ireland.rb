require 'rubygems'
require 'nokogiri'
require 'open-uri'

# get page with links to time periods                                                                                         
root_url = 'http://www.bmwassembly.ie/beneficiaries/'
start_url = root_url + 'Beneficiary%20List.html'

doc = Nokogiri::HTML(open(start_url))

years_ln = doc.css('#content_text a')

# get pages for given time periods                                                                                            
years_ln.each do |t_link|
  mid_url = URI.encode(t_link['href'])
  puts root_url + mid_url
  year_doc = Nokogiri::HTML(open(root_url + mid_url))

  # save counys                                                                                                               
  counys_ln = year_doc.css('#CEB a')
  counys_names = counys_ln.map{|c_ln| c_ln.inner_html }


  # get pages for given counys                                                                                                
  counys_ln.each do |c_link|

    # clean mid_url                                                                                                           
    mid_url.sub!(/\/.*/, '/')
    mid_url.sub!('beneficiaries.html', '')

    tail_url = URI.encode(c_link['href'])
    request_url = root_url + mid_url + tail_url
    puts request_url
    couny_doc = Nokogiri::HTML(open(request_url))

    # get data table rows                                                                                                     
    rows = couny_doc.css('#content_text table tr')

    header_row = rows.shift
    headers = header_row.css('td').map {|cell| cell.inner_html}


    data = []

    rows.each do |row|
      data << row.css('td').map {|cell| cell.inner_html}
    end
   puts data.size

  end

end


