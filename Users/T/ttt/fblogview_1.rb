ScraperWiki.attach("fblog")

data = ScraperWiki.select(
    "* from fblog.swdata where year < 2013"
)


puts "<html>
  <head>
    <script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>"


   
puts "<script type=\"text/javascript\">
      google.load(\"visualization\", \"1\", {packages:[\"corechart\"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        data.addColumn('number', 'posts');
      
        data.addRows("

puts data.size
puts ");"
        
counter = 0;
   data.each do |d|
    puts "data.setValue(" + counter.to_s + ", 0, '" + d['year'].to_s + " " + d['month'].to_s+ "');"
    puts "data.setValue(" + counter.to_s + ", 1, " + d['count_posts'].to_s + ");"

counter = counter +1
   end
   

       puts "var chart = new google.visualization.LineChart(document.getElementById('chart_div1'));
        chart.draw(data, {width: 1200, height: 480, title: 'Company Performance'});
      }
    </script>"



   
puts "<script type=\"text/javascript\">
      google.load(\"visualization\", \"1\", {packages:[\"corechart\"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        data.addColumn('number', 'ehemalige');
      
        data.addRows("

puts data.size
puts ");"
        
counter = 0;
   data.each do |d|
    puts "data.setValue(" + counter.to_s + ", 0, '" + d['year'].to_s + " " + d['month'].to_s+ "');"
    puts "data.setValue(" + counter.to_s + ", 1, " + d['count_ehemalige'].to_s + ");"

counter = counter +1
   end
   

       puts "var chart = new google.visualization.LineChart(document.getElementById('chart_div2'));
        chart.draw(data, {width: 1200, height: 480, title: 'Company Performance'});
      }
    </script>"


   
puts "<script type=\"text/javascript\">
      google.load(\"visualization\", \"1\", {packages:[\"corechart\"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        data.addColumn('number', 'terror');
      
        data.addRows("

puts data.size
puts ");"
        
counter = 0;
   data.each do |d|
    puts "data.setValue(" + counter.to_s + ", 0, '" + d['year'].to_s + " " + d['month'].to_s+ "');"
    puts "data.setValue(" + counter.to_s + ", 1, " + d['count_terror'].to_s + ");"

counter = counter +1
   end
   

       puts "var chart = new google.visualization.LineChart(document.getElementById('chart_div3'));
        chart.draw(data, {width: 1200, height: 480, title: 'Company Performance'});
      }
    </script>"


puts " </head>

  <body>
number of posts per month
    <div id=\"chart_div1\"></div>
usage count of the word ehemalige
    <div id=\"chart_div2\"></div>
usage count of the word terror
    <div id=\"chart_div3\"></div>
  </body>
</html>"
