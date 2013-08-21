puts '<html>
<head>
<title>Fixmystreet</title>
<style type="text/css">
body {
font:0.8em/1.5em "Lucida Grande", "Lucida Sans Unicode", Helvetica, Arial, sans-serif;
}

</style>
</head>
<body>'

puts "<h1>Fixmystreet Dashboard</h1>"

puts "<div style='float:left;'>"

puts "<h2>Reports from the past 6 months</h2>"

ScraperWiki::attach("lichfield_district_council_fixmystreet_reports") 

reports = ScraperWiki::select("* from lichfield_district_council_fixmystreet_reports.swdata WHERE updated > '#{(Date.today-210).strftime('%F')}' ORDER BY updated DESC")

puts "<ul>"

reports.each do |report|

  puts "<li><h3><a href='#{report['url']}' targe='_blank'>#{report['title']}</a></h3>
            <strong>Status:</strong> #{report['status']}<br />
            <strong>Requested:</strong> #{Date.parse(report['requested']).strftime('%d %B %Y')}<br />
            <strong>Updated:</strong> #{Date.parse(report['updated']).strftime('%d %B %Y')}

 </li>"

end

puts "</ul>"
puts "</div>"

puts "<div style='float:right;'>"

puts "<h2 style='text-align: center;'>Reports by month</h2>"
puts "<img src='https://views.scraperwiki.com/run/fixmystreet_reports_by_month/?' />"
puts "</div>"

puts "<div style='float:left; clear: both;'></div<"

puts "</body>
</html>"