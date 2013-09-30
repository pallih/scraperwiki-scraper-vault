ScraperWiki.attach("all_dot_contracts")
years = ["98","99","00","01","02","03","04","05","06","07","08","09","10"]
years = ["98"]
puts RUBY_VERSION
years.each do |fy|
  (1..4).each do |q|

    data = ScraperWiki.select( "* from all_dot_contracts.swdata where fy='#{fy}' and q='#{q}' order by projectno desc" ).first(3)
    full_year = fy.to_i > 50 ? "19" : "20"
    full_year << fy
    puts "<h2>FY #{full_year} Quarter #{q}</h2>"
    puts "<table border=1>"
    puts "<tr><th>Project Number</th><th>Project Title</th><th>Bid Opening</th><th>Estimate</th></tr>"
    data.each do |row|
      puts "<tr>"
      puts "<td>", row["projectno"], "</td>"
      file_url = row["projectno"].gsub(' and ','-').gsub(/[ .)]/,'').gsub('(','-')
      puts "<td><a href='http://hawaii.gov/dot/administration/con/bidopen/FY#{full_year}/Q#{q}/#{file_url}.pdf/view'>"
      puts row["projecttitle"].split(' ').collect{|x| x.capitalize}.join(' ')
      puts "</a></td>"
      puts "<td>", row["bidopening"], "</td>"
      puts "<td>", row["estimate"], "</td>"
      puts "</tr>"
    end
    puts "</table>"

  end
end
ScraperWiki.attach("all_dot_contracts")
years = ["98","99","00","01","02","03","04","05","06","07","08","09","10"]
years = ["98"]
puts RUBY_VERSION
years.each do |fy|
  (1..4).each do |q|

    data = ScraperWiki.select( "* from all_dot_contracts.swdata where fy='#{fy}' and q='#{q}' order by projectno desc" ).first(3)
    full_year = fy.to_i > 50 ? "19" : "20"
    full_year << fy
    puts "<h2>FY #{full_year} Quarter #{q}</h2>"
    puts "<table border=1>"
    puts "<tr><th>Project Number</th><th>Project Title</th><th>Bid Opening</th><th>Estimate</th></tr>"
    data.each do |row|
      puts "<tr>"
      puts "<td>", row["projectno"], "</td>"
      file_url = row["projectno"].gsub(' and ','-').gsub(/[ .)]/,'').gsub('(','-')
      puts "<td><a href='http://hawaii.gov/dot/administration/con/bidopen/FY#{full_year}/Q#{q}/#{file_url}.pdf/view'>"
      puts row["projecttitle"].split(' ').collect{|x| x.capitalize}.join(' ')
      puts "</a></td>"
      puts "<td>", row["bidopening"], "</td>"
      puts "<td>", row["estimate"], "</td>"
      puts "</tr>"
    end
    puts "</table>"

  end
end
