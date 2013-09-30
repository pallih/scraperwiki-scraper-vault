<html>
<head>
  <script type="text/javascript" src="https://www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['corechart']});
    var visualization;

    function draw() {
      drawVisualization();
    }

    function drawVisualization() {
      var container = document.getElementById('visualization_div');
      visualization = new google.visualization.PieChart(container);
      var query = new google.visualization.Query('https://spreadsheets.google.com/tq?key=pCQbetd-CptHnwJEfo8tALA&tqx=out:html;');
          query.setQuery('SELECT A,B  WHERE B > 5 ORDER BY B DESC');
          query.send(queryCallback);
    }

    function queryCallback(response) {
      visualization.draw(response.getDataTable(), {is3D: true});
    }


    google.setOnLoadCallback(draw);
  </script>
</head>
<body>
  <div id="visualization_div" style="width: 270px; height: 200px;"></div>
  <div id="toolbar_div"></div>
</body>
</html><html>
<head>
  <script type="text/javascript" src="https://www.google.com/jsapi"></script>
  <script type="text/javascript">
    google.load('visualization', '1', {packages: ['corechart']});
    var visualization;

    function draw() {
      drawVisualization();
    }

    function drawVisualization() {
      var container = document.getElementById('visualization_div');
      visualization = new google.visualization.PieChart(container);
      var query = new google.visualization.Query('https://spreadsheets.google.com/tq?key=pCQbetd-CptHnwJEfo8tALA&tqx=out:html;');
          query.setQuery('SELECT A,B  WHERE B > 5 ORDER BY B DESC');
          query.send(queryCallback);
    }

    function queryCallback(response) {
      visualization.draw(response.getDataTable(), {is3D: true});
    }


    google.setOnLoadCallback(draw);
  </script>
</head>
<body>
  <div id="visualization_div" style="width: 270px; height: 200px;"></div>
  <div id="toolbar_div"></div>
</body>
</html>