def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" def html():
    print """<html> 
  <head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>     
    <title>London Cycle Hire Locations</title> 
    <script type="text/javascript" src="http://www.google.com/jsapi"></script> 
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4/jquery.min.js"></script> 
    <script type="text/javascript">       
      google.load("visualization", "1", {packages:["imagepiechart", "imagebarchart"]});
      google.setOnLoadCallback(queryData);
 
      var the_response;
      var column1 = 1;
      var column2 = {calc:capacity, type:'number', label:'Capacity'};
      var chart_type = "pie";
 
      function queryData() {
         var query = new google.visualization.Query('http://api.scraperwiki.com/api/1.0/datastore/getdata?&format=gviz&name=jrrt-grants&limit=20');
         query.send(handleQueryResponse);
      }   
 
      function handleQueryResponse(response) {
         if (response.isError()) {
           alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
           return;
         }
 
         the_response = response;
 
         draw_table();
      } 
 
      function draw_table(){
         var data = the_response.getDataTable();
         var view = new google.visualization.DataView(data);
         view.setColumns([column1, column2]);
         if(chart_type == "pie"){
             var table = new google.visualization.ImagePieChart(document.getElementById('visualization_chart'));
         }else{
             var table = new google.visualization.ImageBarChart(document.getElementById('visualization_chart'));
         }
         table.draw(view, {});
      }
 
      function capacity(dataTable, rowNum){
          return parseInt(dataTable.getValue(rowNum, 0));
      }
 
      $(function(){
          $('#label1').click(function(){
              column1 = 4;
              draw_table();
          });
 
          $('#label2').click(function(){
              column1 = 1;
              draw_table();
          });
 
          $('#type1').click(function(){
              chart_type = "bar";
              draw_table();
          });
 
          $('#type2').click(function(){
              chart_type = "pie";
              draw_table();
          });
      });
    </script> 
  </head>     
  <body>            
    <div id="visualization_chart"></div> 
    <a href="#" id="label1">Title</a> <a href="#" id="label2">Name</a> 
    <br/> 
    <a href="#" id="type1">Bar</a> <a href="#" id="type2">Pie</a> 
  </body> 
</html>
""" 