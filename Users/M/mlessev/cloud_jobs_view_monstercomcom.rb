# encoding: utf-8

ScraperWiki::attach("cloud_jobs_summary_details_monstercouk_in_uk")
ScraperWiki::attach("cloud_jobs_summary_details_monstercom_in_usa")
#ScraperWiki::attach("cloud_jobs_in_monstercom")
#ScraperWiki::attach("cloud_jobs_details_monstercom")
#ScraperWiki::attach("cloud_jobs_details_in_bulgaria_monstercom")


uk_data_all = ScraperWiki::select( "count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions" )
us_data_all = ScraperWiki::select( "count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent  from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions" )

uk_data_year = ScraperWiki::select("year, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year order by year")
us_data_year = ScraperWiki::select("year, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year order by year")

uk_data_month = ScraperWiki::select("year, month, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year, month order by year, month")
us_data_month = ScraperWiki::select("year, month, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year, month order by year, month")

uk_data_week = ScraperWiki::select("year, week, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year, week order by year, week")
us_data_week = ScraperWiki::select("year, week, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year, week order by year, week")

uk_data_kew_word = ScraperWiki::select("k.Provider as search_keyword, count(distinct j.text_body || ' - ' || j.company_name || ' - ' || j.location) as br from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by k.Provider order by br desc")
us_data_kew_word = ScraperWiki::select("k.Provider as search_keyword, count(distinct j.text_body || ' - ' || j.company_name || ' - ' || j.location) as br from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k  where j.search_keyword = k.keyword group by k.Provider order by br desc")

uk_company = ScraperWiki::select("j.company_name as company_name, count(distinct j.id) as br, count(distinct j.text_body || ' - ' || j.location) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by j.company_name order by br_unique desc, br desc limit 10")
us_company = ScraperWiki::select("j.company_name as company_name, count(distinct j.id) as br, count(distinct j.text_body || ' - ' || j.location) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k  where j.search_keyword = k.keyword group by j.company_name order by br_unique desc, br desc limit 10")

uk_pos = ScraperWiki::select("j.text_body as company_name, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words, count(distinct j.company_name) as company_count, replace(GROUP_CONCAT(distinct' - ' || company_name), ',', '<br>') as companies from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by j.text_body order by br_unique desc, br desc limit 5")
us_pos = ScraperWiki::select("j.text_body as company_name, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words, count(distinct j.company_name) as company_count, replace(GROUP_CONCAT(distinct' - ' || company_name), ',', '<br>') as companies from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k where j.search_keyword = k.keyword group by j.text_body order by br_unique desc, br desc limit 5")


uk_location = ScraperWiki::select("j.location, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j where j.location not like 'Location:%' group by j.location having count(distinct j.id) > 20 order by br_unique desc")
us_location = ScraperWiki::select("j.location, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j where j.location not like 'Location:%' group by j.location having count(distinct j.id) > 20 order by br_unique desc")

puts "<head>"
puts "  <title>Title</title>"
puts '  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'

puts "This is a <em>fragment</em> of HTML."
puts "<style type='text/css'>"
puts ".myTable { background-color:#FFFFE0;border-collapse:collapse; }"
puts ".myTable th { background-color:#BDB76B;color:white; }"
puts ".myTable td, .myTable th { padding:5px;border:1px solid #BDB76B; }"
puts "</style>"
puts "<!-- Place the above styles between the document's <head></head> tags -->"

puts "</head>"
puts "<body>"

# start Java script

puts '  <script type="text/javascript" src="https://www.google.com/jsapi"></script>'
puts '    <script type="text/javascript">'
puts '      google.load("visualization", "1", {packages:["corechart","geochart"]});'
puts '      google.setOnLoadCallback(drawChart);'
puts '      google.setOnLoadCallback(drawChart2);'
puts '      google.setOnLoadCallback(drawChartJobsBGPie);'
puts '      google.setOnLoadCallback(drawChartJobTigerBGPie);'
puts '      google.setOnLoadCallback(drawRegionsMapJobsBG);'
puts '      google.setOnLoadCallback(drawRegionsMapJobTigerBG);'

puts "      function drawChart() {"
puts "        var data = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 1000, 52],"
for d in uk_data_week
puts "          ['" + d["week"].to_s + "', " + d["br"].to_s + ", " + d["br_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var options = {"
puts "          title: 'UK cloud jobs',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));"
puts "        chart.draw(data, options);"
puts "    };"

puts "      function drawChart2() {"
puts "        var data2 = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 650, 18],"
for d in us_data_week
puts "          ['" + d["week"].to_s + "', " + d["br"].to_s + ", " + d["br_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var options2 = {"
puts "          title: 'USA cloud jobs',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart2 = new google.visualization.AreaChart(document.getElementById('chart_div2'));"
puts "        chart2.draw(data2, options2);"
puts "    };"

puts "      function drawChartJobsBGPie() {"
puts "        var dataJobsBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in uk_data_kew_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobsBGPie = {"
puts "          title: 'UK cloud jobs'"
puts "        };"

puts "        var chartJobsBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobsBGPie'));"
puts "        chartJobsBGPie.draw(dataJobsBGPie, optionsJobsBGPie);"
puts "      };"

puts "      function drawChartJobTigerBGPie() {"
puts "        var dataJobTigerBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in us_data_kew_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobTigerBGPie = {"
puts "          title: 'USA cloud jobs'"
puts "        };"

puts "        var chartJobTigerBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobTigerBGPie'));"
puts "        chartJobTigerBGPie.draw(dataJobTigerBGPie, optionsJobTigerBGPie);"
puts "    };"


puts "    function drawRegionsMapJobsBG() {"
puts "      var dataRegionsMapJobsBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'Unique', 'All'],"
for d in uk_location
puts "          ['" + d["location"].to_s + "', " + d["br_unique"].to_s + ", " + d["br"].to_s + "],"
#puts "          ['London',   1452,    85],"
#puts "          ['Manchester',    109,     9],"
#puts "          ['Liverpool',   98,    11],"
#puts "          ['Glasgow',    17,     2],"
#puts "          ['Aberdeen',      23,     1],"
end
puts "          ['Leeds',     3,     0]"
puts "        ], false);"

puts "      var optionsRegionsMapJobsBG = {"
puts "        region: 'GB',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobs.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobsBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobsBG'));"
puts "        chartRegionsMapJobsBG.draw(dataRegionsMapJobsBG, optionsRegionsMapJobsBG);"
puts "    };"

puts "    function drawRegionsMapJobTigerBG() {"
puts "      var dataRegionsMapJobTigerBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'Unique', 'All'],"
for d in us_location
puts "          ['" + d["location"].to_s + "', " + d["br_unique"].to_s + ", " + d["br"].to_s + "],"
#puts "          ['New York, NY',   515,    16],"
#puts "          ['Boston, MA',    39,     3],"
end
puts "        ], false);"

puts "      var optionsRegionsMapJobTigerBG = {"
puts "        region: 'US',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobtiger.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobTigerBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobTigerBG'));"
puts "        chartRegionsMapJobTigerBG.draw(dataRegionsMapJobTigerBG, optionsRegionsMapJobTigerBG);"
puts "    };"

puts "    </script>"

# end Java script


#puts data_all
puts "<p>1. Unique jobs </p>"

puts "<table class='myTable' align='center'>"
puts "<tr><th>Country</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
puts "<tr> <td width='150'><b>UK cloud jobs</b></td>"
for d in uk_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
end
puts "</tr>"
puts "<tr> <td><b>USA cloud jobs</b></td>"
for d in us_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
end
puts "</tr>"
puts "</table>"

puts "<p>2. Group by years</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>3. Group by months</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>4. Group by weeks</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Week</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_week
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["week"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Week</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_week
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["week"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"



puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div2" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>5. Group by key word</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div_JobsBGPie" style="width: 650px; height: 400px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div_JobTigerBGPie" style="width: 650px; height: 400px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>6. Group by Company</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='120px'>Company name</th><th width='80px'>unique (all)</th><th width='240px'>Knowledges</th></tr>"
for d in uk_company
  puts "<tr>"
  puts "<td width='120px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='240px'>", d["key_words"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='120px'>Company name</th><th width='60px'>unique (all)</th><th width='280px'>Knowledges</th></tr>"
for d in us_company
  puts "<tr>"
  puts "<td width='120px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='300px'>", d["key_words"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>7. Top 5 jobs with cloud skills</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='80px'>Job name</th><th width='80px'>unique (all)</th><th width='120px'>Knowledges</th><th width='220px'>Companies</th></tr>"
for d in uk_pos
  puts "<tr>"
  puts "<td width='80px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='120px'>", d["key_words"], "</td>"
  puts "<td width='220px'>", d["companies"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='80px'>Job name</th><th width='60px'>unique (all)</th><th width='120px'>Knowledges</th><th width='220px'>Companies</th></tr>"
for d in us_pos
  puts "<tr>"
  puts "<td width='80px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='120px'>", d["key_words"], "</td>"
  puts "<td width='220px'>", d["companies"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"


puts "<p>8. Group by city</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div_RegionsMapJobsBG" style="width: 600px; height: 450px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div_RegionsMapJobTigerBG" style="width: 600px; height: 450px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "</body>"

# encoding: utf-8

ScraperWiki::attach("cloud_jobs_summary_details_monstercouk_in_uk")
ScraperWiki::attach("cloud_jobs_summary_details_monstercom_in_usa")
#ScraperWiki::attach("cloud_jobs_in_monstercom")
#ScraperWiki::attach("cloud_jobs_details_monstercom")
#ScraperWiki::attach("cloud_jobs_details_in_bulgaria_monstercom")


uk_data_all = ScraperWiki::select( "count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions" )
us_data_all = ScraperWiki::select( "count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent  from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions" )

uk_data_year = ScraperWiki::select("year, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year order by year")
us_data_year = ScraperWiki::select("year, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year order by year")

uk_data_month = ScraperWiki::select("year, month, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year, month order by year, month")
us_data_month = ScraperWiki::select("year, month, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year, month order by year, month")

uk_data_week = ScraperWiki::select("year, week, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions group by year, week order by year, week")
us_data_week = ScraperWiki::select("year, week, count(distinct id) as br, count(distinct text_body || ' - ' || company_name || ' - ' || location) as br_unique, ROUND(count(distinct text_body || ' - ' || company_name || ' - ' || location)*0.01/(count(distinct id)/100), 2) as percent from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions group by year, week order by year, week")

uk_data_kew_word = ScraperWiki::select("k.Provider as search_keyword, count(distinct j.text_body || ' - ' || j.company_name || ' - ' || j.location) as br from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by k.Provider order by br desc")
us_data_kew_word = ScraperWiki::select("k.Provider as search_keyword, count(distinct j.text_body || ' - ' || j.company_name || ' - ' || j.location) as br from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k  where j.search_keyword = k.keyword group by k.Provider order by br desc")

uk_company = ScraperWiki::select("j.company_name as company_name, count(distinct j.id) as br, count(distinct j.text_body || ' - ' || j.location) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by j.company_name order by br_unique desc, br desc limit 10")
us_company = ScraperWiki::select("j.company_name as company_name, count(distinct j.id) as br, count(distinct j.text_body || ' - ' || j.location) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k  where j.search_keyword = k.keyword group by j.company_name order by br_unique desc, br desc limit 10")

uk_pos = ScraperWiki::select("j.text_body as company_name, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words, count(distinct j.company_name) as company_count, replace(GROUP_CONCAT(distinct' - ' || company_name), ',', '<br>') as companies from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j, cloud_jobs_summary_details_monstercouk_in_uk.search_keyword k where j.search_keyword = k.keyword group by j.text_body order by br_unique desc, br desc limit 5")
us_pos = ScraperWiki::select("j.text_body as company_name, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique, GROUP_CONCAT(distinct ' ' || k.Provider) as key_words, count(distinct j.company_name) as company_count, replace(GROUP_CONCAT(distinct' - ' || company_name), ',', '<br>') as companies from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j, cloud_jobs_summary_details_monstercom_in_usa.search_keyword k where j.search_keyword = k.keyword group by j.text_body order by br_unique desc, br desc limit 5")


uk_location = ScraperWiki::select("j.location, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique from cloud_jobs_summary_details_monstercouk_in_uk.cloud_possitions j where j.location not like 'Location:%' group by j.location having count(distinct j.id) > 20 order by br_unique desc")
us_location = ScraperWiki::select("j.location, count(distinct j.id) as br, count(distinct j.company_name || ' - ' || j.location || ' - ' || j.salary) as br_unique from cloud_jobs_summary_details_monstercom_in_usa.cloud_possitions j where j.location not like 'Location:%' group by j.location having count(distinct j.id) > 20 order by br_unique desc")

puts "<head>"
puts "  <title>Title</title>"
puts '  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'

puts "This is a <em>fragment</em> of HTML."
puts "<style type='text/css'>"
puts ".myTable { background-color:#FFFFE0;border-collapse:collapse; }"
puts ".myTable th { background-color:#BDB76B;color:white; }"
puts ".myTable td, .myTable th { padding:5px;border:1px solid #BDB76B; }"
puts "</style>"
puts "<!-- Place the above styles between the document's <head></head> tags -->"

puts "</head>"
puts "<body>"

# start Java script

puts '  <script type="text/javascript" src="https://www.google.com/jsapi"></script>'
puts '    <script type="text/javascript">'
puts '      google.load("visualization", "1", {packages:["corechart","geochart"]});'
puts '      google.setOnLoadCallback(drawChart);'
puts '      google.setOnLoadCallback(drawChart2);'
puts '      google.setOnLoadCallback(drawChartJobsBGPie);'
puts '      google.setOnLoadCallback(drawChartJobTigerBGPie);'
puts '      google.setOnLoadCallback(drawRegionsMapJobsBG);'
puts '      google.setOnLoadCallback(drawRegionsMapJobTigerBG);'

puts "      function drawChart() {"
puts "        var data = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 1000, 52],"
for d in uk_data_week
puts "          ['" + d["week"].to_s + "', " + d["br"].to_s + ", " + d["br_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var options = {"
puts "          title: 'UK cloud jobs',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));"
puts "        chart.draw(data, options);"
puts "    };"

puts "      function drawChart2() {"
puts "        var data2 = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 650, 18],"
for d in us_data_week
puts "          ['" + d["week"].to_s + "', " + d["br"].to_s + ", " + d["br_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var options2 = {"
puts "          title: 'USA cloud jobs',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart2 = new google.visualization.AreaChart(document.getElementById('chart_div2'));"
puts "        chart2.draw(data2, options2);"
puts "    };"

puts "      function drawChartJobsBGPie() {"
puts "        var dataJobsBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in uk_data_kew_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobsBGPie = {"
puts "          title: 'UK cloud jobs'"
puts "        };"

puts "        var chartJobsBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobsBGPie'));"
puts "        chartJobsBGPie.draw(dataJobsBGPie, optionsJobsBGPie);"
puts "      };"

puts "      function drawChartJobTigerBGPie() {"
puts "        var dataJobTigerBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in us_data_kew_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobTigerBGPie = {"
puts "          title: 'USA cloud jobs'"
puts "        };"

puts "        var chartJobTigerBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobTigerBGPie'));"
puts "        chartJobTigerBGPie.draw(dataJobTigerBGPie, optionsJobTigerBGPie);"
puts "    };"


puts "    function drawRegionsMapJobsBG() {"
puts "      var dataRegionsMapJobsBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'Unique', 'All'],"
for d in uk_location
puts "          ['" + d["location"].to_s + "', " + d["br_unique"].to_s + ", " + d["br"].to_s + "],"
#puts "          ['London',   1452,    85],"
#puts "          ['Manchester',    109,     9],"
#puts "          ['Liverpool',   98,    11],"
#puts "          ['Glasgow',    17,     2],"
#puts "          ['Aberdeen',      23,     1],"
end
puts "          ['Leeds',     3,     0]"
puts "        ], false);"

puts "      var optionsRegionsMapJobsBG = {"
puts "        region: 'GB',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobs.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobsBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobsBG'));"
puts "        chartRegionsMapJobsBG.draw(dataRegionsMapJobsBG, optionsRegionsMapJobsBG);"
puts "    };"

puts "    function drawRegionsMapJobTigerBG() {"
puts "      var dataRegionsMapJobTigerBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'Unique', 'All'],"
for d in us_location
puts "          ['" + d["location"].to_s + "', " + d["br_unique"].to_s + ", " + d["br"].to_s + "],"
#puts "          ['New York, NY',   515,    16],"
#puts "          ['Boston, MA',    39,     3],"
end
puts "        ], false);"

puts "      var optionsRegionsMapJobTigerBG = {"
puts "        region: 'US',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobtiger.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobTigerBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobTigerBG'));"
puts "        chartRegionsMapJobTigerBG.draw(dataRegionsMapJobTigerBG, optionsRegionsMapJobTigerBG);"
puts "    };"

puts "    </script>"

# end Java script


#puts data_all
puts "<p>1. Unique jobs </p>"

puts "<table class='myTable' align='center'>"
puts "<tr><th>Country</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
puts "<tr> <td width='150'><b>UK cloud jobs</b></td>"
for d in uk_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
end
puts "</tr>"
puts "<tr> <td><b>USA cloud jobs</b></td>"
for d in us_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
end
puts "</tr>"
puts "</table>"

puts "<p>2. Group by years</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>3. Group by months</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>4. Group by weeks</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Week</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in uk_data_week
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["week"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Week</th><th>Cloud jobs</th><th>Unique cloud jobs</th><th>%</th></tr>"
for d in us_data_week
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["week"].to_s, "</td>"
  puts "<td align='center'>", d["br"].to_s, "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "</td>"
  puts "<td align='center'>", d["percent"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"



puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div2" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>5. Group by key word</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div_JobsBGPie" style="width: 650px; height: 400px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div_JobTigerBGPie" style="width: 650px; height: 400px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>6. Group by Company</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='120px'>Company name</th><th width='80px'>unique (all)</th><th width='240px'>Knowledges</th></tr>"
for d in uk_company
  puts "<tr>"
  puts "<td width='120px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='240px'>", d["key_words"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='120px'>Company name</th><th width='60px'>unique (all)</th><th width='280px'>Knowledges</th></tr>"
for d in us_company
  puts "<tr>"
  puts "<td width='120px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='300px'>", d["key_words"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>7. Top 5 jobs with cloud skills</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>UK cloud jobs</FONT></th></tr>"
puts "<tr><th width='80px'>Job name</th><th width='80px'>unique (all)</th><th width='120px'>Knowledges</th><th width='220px'>Companies</th></tr>"
for d in uk_pos
  puts "<tr>"
  puts "<td width='80px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='120px'>", d["key_words"], "</td>"
  puts "<td width='220px'>", d["companies"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>USA cloud jobs</FONT></th></tr>"
puts "<tr><th width='80px'>Job name</th><th width='60px'>unique (all)</th><th width='120px'>Knowledges</th><th width='220px'>Companies</th></tr>"
for d in us_pos
  puts "<tr>"
  puts "<td width='80px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_unique"].to_s, "(", d["br"].to_s, ")</td>"
  puts "<td width='120px'>", d["key_words"], "</td>"
  puts "<td width='220px'>", d["companies"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"


puts "<p>8. Group by city</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_div_RegionsMapJobsBG" style="width: 600px; height: 450px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_div_RegionsMapJobTigerBG" style="width: 600px; height: 450px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "</body>"

