# Blank Ruby
# encoding: utf-8

#ScraperWiki::attach("cloud_jobs_in_bg")
ScraperWiki::attach("open_cloud_jobs_possitions")
ScraperWiki::attach("cloud_jobs_in_jobtiger_bg")
ScraperWiki::attach("cloud_job_details_jobbg")


jobsbg_data_all = ScraperWiki::select( "br, type from open_cloud_jobs_possitions.ALL_POSITIONS" )
jobtiger_data_all = ScraperWiki::select( "br, type from cloud_jobs_in_jobtiger_bg.ALL_POSITIONS" )

jobsbg_data_year = ScraperWiki::select("year, all_jobs, cloud_jobs from open_cloud_jobs_possitions.JOIN_POSITIONS_YEAR order by year")
jobtiger_data_year = ScraperWiki::select("year, all_jobs, cloud_jobs from cloud_jobs_in_jobtiger_bg.JOIN_POSITIONS_YEAR order by year")

jobsbg_data_month = ScraperWiki::select("year, month, all_jobs_unique, all_jobs, cloud_jobs_unique, cloud_jobs, ROUND(cloud_jobs_unique*1.0/(all_jobs_unique/100), 2) as percentage from open_cloud_jobs_possitions.JOIN_POSITIONS_MONTH order by year, month" )
jobtiger_data_month = ScraperWiki::select("year, month, all_jobs_unique, all_jobs, cloud_jobs_unique, cloud_jobs, ROUND(cloud_jobs_unique*1.0/(all_jobs_unique/100), 2) as percentage from cloud_jobs_in_jobtiger_bg.JOIN_POSITIONS_MONTH order by year, month" )

jobsbg_data_week = ScraperWiki::select("(year * 100 + week) as year, week, all_jobs, cloud_jobs from open_cloud_jobs_possitions.JOIN_POSITIONS_WEEK order by 1 " )
jobtiger_data_week = ScraperWiki::select("(year * 100 + week) as year, week, all_jobs, cloud_jobs from cloud_jobs_in_jobtiger_bg.JOIN_POSITIONS_WEEK order by 1" )

jobsbg_key_word = ScraperWiki::select("search_keyword, br from open_cloud_jobs_possitions.CLOUD_POSITIONS_COND order by br desc" )
jobtiger_key_word = ScraperWiki::select("search_keyword, br from cloud_jobs_in_jobtiger_bg.CLOUD_POSITIONS_COND order by br desc" )

jobsbg_company = ScraperWiki::select("company_name, br_cloud_unique, br_cloud, br_all_unique, br_all from open_cloud_jobs_possitions.JOIN_POSITIONS_COMPANY_UNIQUE LIMIT 10" )
jobtiger_company = ScraperWiki::select("company_name, br_cloud_unique, br_cloud, br_all_unique, br_all from cloud_jobs_in_jobtiger_bg.JOIN_POSITIONS_COMPANY_UNIQUE LIMIT 10" )

jobsbg_pos = ScraperWiki::select("poss_name, poss_count, poss_count_all, comp_count, comp_count_all, companies from open_cloud_jobs_possitions.JOIN_JOB_TOP_POSSITIONS LIMIT 5" )
jobtiger_pos = ScraperWiki::select("poss_name, poss_count, poss_count_all, comp_count, comp_count_all, companies from cloud_jobs_in_jobtiger_bg.JOIN_JOB_TOP_POSSITIONS LIMIT 5" )


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


#puts data_all
puts "<p>1. Unique jobs </p>"

puts "<table class='myTable' align='center'>"
puts "<tr><th>Domain</th><th>IT job possitions</th><th>Unique job possitions</th><th>Cloud job possitions</th><th>Unique Cloud job possitions</th></tr>"
puts "<tr> <td width='150'><b>www.jobs.bg</b></td>"
for d in jobsbg_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
end
puts "</tr>"
puts "<tr> <td><b>www.jobtiger.bg</b></td>"
for d in jobtiger_data_all
  puts "<td align='center'>", d["br"].to_s, "</td>"
end
puts "</tr>"
puts "</table>"

puts "<p>2. Group by years</p>"

puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobs.bg</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>IT job possitions</th><th>Cloud job possitions</th></tr>"
for d in jobsbg_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["all_jobs"].to_s, "</td>"
  puts "<td align='center'>", d["cloud_jobs"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='3'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobtiger.bg</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th>IT job possitions</th><th>Cloud job possitions</th></tr>"
for d in jobtiger_data_year
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td align='center'>", d["all_jobs"].to_s, "</td>"
  puts "<td align='center'>", d["cloud_jobs"].to_s, "</td>"
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
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobs.bg</FONT></th></tr>"
  puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>IT job possitions</th><th>Cloud job possitions</th><th>%</th></tr>"
for d in jobsbg_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'><b>", d["all_jobs_unique"].to_s, "</b>/", d["all_jobs"].to_s,"</td>"
  puts "<td align='center'><b>", d["cloud_jobs_unique"].to_s, "</b>/", d["cloud_jobs"].to_s,"</td>"
  puts "<td>", d["percentage"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobtiger.bg</FONT></th></tr>"
puts "<tr><th width='60'>Year</th><th width='60'>Month</th><th>IT job possitions</th><th>Cloud job possitions</th><th>%</th></tr>"
for d in jobtiger_data_month
  puts "<tr>"
  puts "<td>", d["year"].to_s, "</td>"
  puts "<td>", d["month"].to_s, "</td>"
  puts "<td align='center'><b>", d["all_jobs_unique"].to_s, "</b>/", d["all_jobs"].to_s,"</td>"
  puts "<td align='center'><b>", d["cloud_jobs_unique"].to_s, "</b>/", d["cloud_jobs"].to_s,"</td>"
  puts "<td>", d["percentage"].to_s, "% </td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "</tr>"
puts "</table>"

puts '  <script type="text/javascript" src="https://www.google.com/jsapi"></script>'
puts '    <script type="text/javascript">'
puts '      google.load("visualization", "1", {packages:["corechart","geochart"]});'
puts '      google.setOnLoadCallback(drawChart);'
puts '      google.setOnLoadCallback(drawChart2);'
puts '      google.setOnLoadCallback(drawChartMonth);'
puts '      google.setOnLoadCallback(drawChartMonth2);'
puts '      google.setOnLoadCallback(drawChartJobsBGPie);'
puts '      google.setOnLoadCallback(drawChartJobTigerBGPie);'
puts '      google.setOnLoadCallback(drawRegionsMapJobsBG);'
puts '      google.setOnLoadCallback(drawRegionsMapJobTigerBG);'

puts "      function drawChart() {"
puts "        var data = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 1000, 52],"
for d in jobsbg_data_week
puts "          ['" + d["week"].to_s + "', " + d["all_jobs"].to_s + ", " + d["cloud_jobs"].to_s + "],"
end
puts "        ], false);"
puts "        var options = {"
puts "          title: 'www.jobs.bg',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));"
puts "        chart.draw(data, options);"
puts "    };"

puts "      function drawChart2() {"
puts "        var data2 = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 650, 18],"
for d in jobtiger_data_week
puts "          ['" + d["week"].to_s + "', " + d["all_jobs"].to_s + ", " + d["cloud_jobs"].to_s + "],"
end
puts "        ], false);"
puts "        var options2 = {"
puts "          title: 'www.jobtiger.bg',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chart2 = new google.visualization.AreaChart(document.getElementById('chart_div2'));"
puts "        chart2.draw(data2, options2);"
puts "    };"

puts "      function drawChartJobsBGPie() {"
puts "        var dataJobsBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in jobsbg_key_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobsBGPie = {"
puts "          title: 'www.jobs.bg'"
puts "        };"

puts "        var chartJobsBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobsBGPie'));"
puts "        chartJobsBGPie.draw(dataJobsBGPie, optionsJobsBGPie);"
puts "      };"

puts "      function drawChartJobTigerBGPie() {"
puts "        var dataJobTigerBGPie = google.visualization.arrayToDataTable(["
puts "          ['Cloud', 'Jobs'],"
for d in jobtiger_key_word
puts "          ['" + d["search_keyword"].to_s + "', " + d["br"].to_s + "],"
end
puts "        ], false);"

puts "        var optionsJobTigerBGPie = {"
puts "          title: 'www.jobtiger.bg'"
puts "        };"

puts "        var chartJobTigerBGPie = new google.visualization.PieChart(document.getElementById('chart_div_JobTigerBGPie'));"
puts "        chartJobTigerBGPie.draw(dataJobTigerBGPie, optionsJobTigerBGPie);"
puts "    };"


puts "    function drawRegionsMapJobsBG() {"
puts "      var dataRegionsMapJobsBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'All', 'Cloud'],"
puts "          ['Sofia',   1452,    85],"
puts "          ['Varna',    109,     9],"
puts "          ['Plovdiv',   98,    11],"
puts "          ['Burgas',    17,     2],"
puts "          ['Ruse',      23,     1],"
puts "          ['Yambol',     3,     0]"
puts "        ], false);"

puts "      var optionsRegionsMapJobsBG = {"
puts "        region: 'BG',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobs.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobsBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobsBG'));"
puts "        chartRegionsMapJobsBG.draw(dataRegionsMapJobsBG, optionsRegionsMapJobsBG);"
puts "    };"

puts "    function drawRegionsMapJobTigerBG() {"
puts "      var dataRegionsMapJobTigerBG = google.visualization.arrayToDataTable(["
puts "          ['City',   'All', 'Cloud'],"
puts "          ['Sofia',   515,    16],"
puts "          ['Varna',    39,     3],"
puts "          ['Plovdiv',   18,    4],"
puts "          ['Ruse',      7,     1],"
puts "          ['Veliko Tarnovo',      7,     1],"
puts "        ], false);"

puts "      var optionsRegionsMapJobTigerBG = {"
puts "        region: 'BG',"
puts "        displayMode: 'markers',"
puts "        title: 'www.jobtiger.bg',"
puts "        colorAxis: {colors: ['green', 'blue']}"
puts "      };"

puts "        var chartRegionsMapJobTigerBG = new google.visualization.GeoChart(document.getElementById('chart_div_RegionsMapJobTigerBG'));"
puts "        chartRegionsMapJobTigerBG.draw(dataRegionsMapJobTigerBG, optionsRegionsMapJobTigerBG);"
puts "    };"

puts "      function drawChartMonth() {"
puts "        var dataMonth = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 650, 18],"
for d in jobsbg_data_month
puts "          ['" + d["week"].to_s + "', " + d["all_jobs_unique"].to_s + ", " + d["cloud_jobs_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var optionsMonth = {"
puts "          title: 'www.jobs.bg',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chartMonth = new google.visualization.AreaChart(document.getElementById('chart_divMonth'));"
puts "        chartMonth.draw(dataMonth, optionsMonth);"
puts "    };"

puts "      function drawChartMonth2() {"
puts "        var dataMonth2 = google.visualization.arrayToDataTable(["
puts "          ['Week', 'All jobs', 'Cloud jobs'],"
#puts "          ['2012/48', 650, 18],"
for d in jobtiger_data_month
puts "          ['" + d["week"].to_s + "', " + d["all_jobs_unique"].to_s + ", " + d["cloud_jobs_unique"].to_s + "],"
end
puts "        ], false);"
puts "        var optionsMonth2 = {"
puts "          title: 'www.jobtiger.bg',"
puts "          hAxis: {title: 'Year',  titleTextStyle: {color: 'red'}}"
puts "        };"
puts "        var chartMonth2 = new google.visualization.AreaChart(document.getElementById('chart_divMonth2'));"
puts "        chartMonth2.draw(dataMonth2, optionsMonth2);"
puts "    };"
puts "    </script>"


puts "<table align='center'>"
puts "<tr>"
puts "<td>"
puts '<div id="chart_divMonth" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "<td>"
puts '<div id="chart_divMonth2" style="width: 600px; height: 350px;"></div>'
puts "</td>"
puts "</tr>"
puts "</table>"

puts "<p>4. Group by weeks</p>"


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
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobs.bg</FONT></th></tr>"
puts "<tr><th width='240px'>Company name</th><th>Cloud job unique (all)</th><th>IT job unique (all)</th></tr>"
for d in jobsbg_company
  puts "<tr>"
  puts "<td width='240px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_cloud_unique"].to_s, "(", d["br_cloud"].to_s, ")</td>"
  puts "<td align='center'>", d["br_all_unique"].to_s, "(", d["br_all"].to_s, ")</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='5'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobtiger.bg</FONT></th></tr>"
puts "<tr><th width='240px'>Company name</th><th>Cloud job unique</th><th>IT job unique</th></tr>"
for d in jobtiger_company
  puts "<tr>"
  puts "<td width='240px'>", d["company_name"], "</td>"
  puts "<td align='center'>", d["br_cloud_unique"].to_s, "(", d["br_cloud"].to_s, ")</td>"
  puts "<td align='center'>", d["br_all_unique"].to_s, "(", d["br_all"].to_s, ")</td>"
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
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobs.bg</FONT></th></tr>"
puts "<tr><th width='160px'>Job title</th><th width='60px'>Job cloud (all)</th><th width='60px'>Companies unique (all)</th><th width='240px'>Companie names</th></tr>"
for d in jobsbg_pos
  puts "<tr>"
  puts "<td width='160px'>", d["poss_name"], "</td>"
  puts "<td align='center'>", d["poss_count"].to_s, "(", d["poss_count_all"].to_s, ")</td>"
  puts "<td align='center'>", d["comp_count"].to_s, "(", d["comp_count_all"].to_s, ")</td>"
  puts "<td width='240px'>", d["companies"], "</td>"
  puts "</tr>"
end
puts "</table>"
puts "</td>"
puts "<td>"
puts "<table class='myTable' align='center'>"
puts "<tr><th colspan='4'><FONT COLOR=WHITE FACE='Geneva, Arial' SIZE=4>www.jobtiger.bg</FONT></th></tr>"
puts "<tr><th width='160px'>Job title</th><th width='60px'>Job cloud (all)</th><th width='60px'>Companies unique (all)</th><th width='240px'>Companie names</th></tr>"
for d in jobtiger_pos
  puts "<tr>"
  puts "<td width='160px'>", d["poss_name"], "</td>"
  puts "<td align='center'>", d["poss_count"].to_s, "(", d["poss_count_all"].to_s, ")</td>"
  puts "<td align='center'>", d["comp_count"].to_s, "(", d["comp_count_all"].to_s, ")</td>"
  puts "<td width='240px'>", d["companies"], "</td>"
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
