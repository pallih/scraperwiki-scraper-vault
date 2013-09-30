scraper = 'w3schools-browser-stats'
limit = 20
offset = 0

hd = {
  "ymo" => "Year, Month",
  "tst" => "Timestamp",
  "iex" => "Internet Explorer",
  "ffx" => "Firefox",
  "chr" => "Chrome",
  "saf" => "Safari",
  "ope" => "Opera"
}

ScraperWiki.attach(scraper, "src")

sdata = ScraperWiki.sqliteexecute("select * from src.swdata limit ? offset ?", [limit, offset])
keys = sdata["keys"]
rows = sdata["data"]
l = rows.length-1

print <<-MULTILINE
<html><head>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Browser');
  data.addColumn('number', 'Percentage');
  data.addRows([
MULTILINE

puts "['#{hd['iex']}', #{rows[l][0].to_f}],"
puts "['#{hd['ffx']}', #{rows[l][1].to_f}],"
puts "['#{hd['saf']}', #{rows[l][2].to_f}],"
puts "['#{hd['ope']}', #{rows[l][3].to_f}],"
puts "['#{hd['chr']}', #{rows[l][4].to_f}],"
puts "['', #{100 - rows[l][0].to_f - rows[l][1].to_f - rows[l][2].to_f - rows[l][3].to_f - rows[l][4].to_f}]]);"

puts <<-MULTILINE
var options = {'title':'#{rows[l][6].to_s}', 'width':400, 'height':300, 'slices': [{}, {}, {}, {}, {}, {color: 'white'}]};
var chart = new google.visualization.PieChart(document
MULTILINE
print ".getElementById('chart_div'));"
print <<-MULTILINE
chart.draw(data, options);}
</script></head><body>
MULTILINE

print '<h2>The latest browser statistics from w3schools.com:  (' + keys.size.to_s + ' columns)</h2>'
print '<div id="chart_div" style="height:300px;width:400px;"></div>'
print '<table border="1" style="border-collapse:collapse;">'

print "<tr>"
keys.each do |value|
  puts "<th>#{hd[value]}</th>"
end
puts "</tr>"

rows.each do |row|
  puts "<tr>"
  row.each do |value|
    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end

puts "</table></body></html>"scraper = 'w3schools-browser-stats'
limit = 20
offset = 0

hd = {
  "ymo" => "Year, Month",
  "tst" => "Timestamp",
  "iex" => "Internet Explorer",
  "ffx" => "Firefox",
  "chr" => "Chrome",
  "saf" => "Safari",
  "ope" => "Opera"
}

ScraperWiki.attach(scraper, "src")

sdata = ScraperWiki.sqliteexecute("select * from src.swdata limit ? offset ?", [limit, offset])
keys = sdata["keys"]
rows = sdata["data"]
l = rows.length-1

print <<-MULTILINE
<html><head>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawChart);
function drawChart() {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Browser');
  data.addColumn('number', 'Percentage');
  data.addRows([
MULTILINE

puts "['#{hd['iex']}', #{rows[l][0].to_f}],"
puts "['#{hd['ffx']}', #{rows[l][1].to_f}],"
puts "['#{hd['saf']}', #{rows[l][2].to_f}],"
puts "['#{hd['ope']}', #{rows[l][3].to_f}],"
puts "['#{hd['chr']}', #{rows[l][4].to_f}],"
puts "['', #{100 - rows[l][0].to_f - rows[l][1].to_f - rows[l][2].to_f - rows[l][3].to_f - rows[l][4].to_f}]]);"

puts <<-MULTILINE
var options = {'title':'#{rows[l][6].to_s}', 'width':400, 'height':300, 'slices': [{}, {}, {}, {}, {}, {color: 'white'}]};
var chart = new google.visualization.PieChart(document
MULTILINE
print ".getElementById('chart_div'));"
print <<-MULTILINE
chart.draw(data, options);}
</script></head><body>
MULTILINE

print '<h2>The latest browser statistics from w3schools.com:  (' + keys.size.to_s + ' columns)</h2>'
print '<div id="chart_div" style="height:300px;width:400px;"></div>'
print '<table border="1" style="border-collapse:collapse;">'

print "<tr>"
keys.each do |value|
  puts "<th>#{hd[value]}</th>"
end
puts "</tr>"

rows.each do |row|
  puts "<tr>"
  row.each do |value|
    puts "<td>#{value.to_s}</td>"
  end
  puts "</tr>"
end

puts "</table></body></html>"