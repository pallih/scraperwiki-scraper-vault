<?php header('text/html'); ?>
<html>
<head>
<script src="http://d3js.org/d3.v2.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<style type="text/css">
    #chart {
        width: 960px;
        height: 500px;
    }

    .black path {
        fill: none;
        stroke: #ccc;
        stroke-width: 3px;
    }

    .white path {
        fill: #fff;
        stroke: #fff;
    }

    .grey path {
        fill: #ccc;
        stroke: #666;
    } 
</style>
</head>
<?php

$regions = array(
   0 => array(
                    'id' => 11812,
                     'label' => 'North East',
                     'pop' => '2.6',
                     'geo' => ''
                   ),
   1 => array(
                     'id' => 11807,
                     'label' => 'North West',
                     'pop' => '7.1',
                     'geo' =>  ''
                   ),
   2 => array(
                     'id' => 11810,
                     'label' => 'Yorkshire and the Humber',
                     'pop' => '5.3',
                     'geo' =>  ''
                   ),
   3 => array(
                        'id' => 11805,
                        'label' => 'East Midlands',
                        'pop' => '4.5',
                        'geo' =>  ''
                    ),
   4 => array(
                        'id' => 11809,
                        'label' => 'West Midlands',
                        'pop' => '5.6',
                        'geo' =>  ''
                    ),
   5 => array(
                        'id' => 11804,
                        'label' => 'Eastern England',
                        'pop' => '5.8',
                        'geo' =>  ''
                    ),
   6 => array(
                        'id' => 11806,
                        'label' => 'London',
                        'pop' => '8.2',
                        'geo' =>  ''
                    ),
   7 => array(
                        'id' => 11811,
                        'label' => 'South East',
                        'pop' => '8.6',
                        'geo' =>  ''
                    ),
   8 => array(
                        'id' => 11814,
                        'label' => 'South West',
                        'pop' => '5.3',
                        'geo' =>  ''
                    ),
   9 => array(
                        'id' => 11813,
                        'label' => 'Wales',
                        'pop' => '3.1',
                        'geo' =>  ''
                    ),
);

$total = 0;

foreach ($regions as $region) {
    $total = $total + $region['pop'];
}

//Get GeoJSON of regions
/*
foreach ($regions as $key => $region) {
    $regions[$key]['geo'] = file_get_contents('http://mapit.mysociety.org/area/' . $region['id'] . '.geojson?simplify_tolerance=0.03');
}

$json = array(
    'type' => 'FeatureCollection',
    'features' => array()
);

foreach ($regions as $key => $region) {
    $json['features'][] = array(
        'type' => 'Feature',
        'id' => $key,
        'properties' => array(
             'name' => $region['label']),
        'geometry' => $region['geo']     
    );
}*/
?>
<body>
    <div id="chart"></div>
    <script type="text/javascript">
var data = [
    <?php foreach ($regions as $region) echo $region['pop'] / 30  . ', '; ?>
];
/*var data = [
  , .187, .198, , .133, .175, .151, , .1, .125, .171, , .172, .133, , .108,
  .142, .167, .201, .175, .159, .169, .177, .141, .163, .117, .182, .153, .195,
  .189, .134, .163, .133, .151, .145, .13, .139, .169, .164, .175, .135, .152,
  .169, , .132, .167, .139, .184, .159, .14, .146, .157, , .139, .183, .16, .143
];*/


var svg = d3.select("#chart").append("svg")
    .attr("width", 960)
    .attr("height", 500);

jQuery.getJSON("http://dev.aendrew.com/eur.php?callback=?", function (json) {
  var path = d3.geo.path();
  var m = d3.geo.mercator();
  m.scale(16000);
  m.translate([480,3050]);
  path.projection(m);
console.dir(json);
  svg.append("g")
      .attr("class", "black")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path);

  svg.append("g")
      .attr("class", "white")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path);

  svg.append("g")
      .attr("class", "grey")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path)
      .attr("transform", function(d) {
        var centroid = path.centroid(d),
            x = centroid[0],
            y = centroid[1];
        return "translate(" + x + "," + y + ")"
            + "scale(" + Math.sqrt(data[+d.id] * 5 || 0) + ")"
            + "translate(" + -x + "," + -y + ")";
      })
      .style("stroke-width", function(d) {
        return 1 / Math.sqrt(data[+d.id] * 5 || 1);
      });

});


    </script>

</body>
</html>
<?php header('text/html'); ?>
<html>
<head>
<script src="http://d3js.org/d3.v2.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
<style type="text/css">
    #chart {
        width: 960px;
        height: 500px;
    }

    .black path {
        fill: none;
        stroke: #ccc;
        stroke-width: 3px;
    }

    .white path {
        fill: #fff;
        stroke: #fff;
    }

    .grey path {
        fill: #ccc;
        stroke: #666;
    } 
</style>
</head>
<?php

$regions = array(
   0 => array(
                    'id' => 11812,
                     'label' => 'North East',
                     'pop' => '2.6',
                     'geo' => ''
                   ),
   1 => array(
                     'id' => 11807,
                     'label' => 'North West',
                     'pop' => '7.1',
                     'geo' =>  ''
                   ),
   2 => array(
                     'id' => 11810,
                     'label' => 'Yorkshire and the Humber',
                     'pop' => '5.3',
                     'geo' =>  ''
                   ),
   3 => array(
                        'id' => 11805,
                        'label' => 'East Midlands',
                        'pop' => '4.5',
                        'geo' =>  ''
                    ),
   4 => array(
                        'id' => 11809,
                        'label' => 'West Midlands',
                        'pop' => '5.6',
                        'geo' =>  ''
                    ),
   5 => array(
                        'id' => 11804,
                        'label' => 'Eastern England',
                        'pop' => '5.8',
                        'geo' =>  ''
                    ),
   6 => array(
                        'id' => 11806,
                        'label' => 'London',
                        'pop' => '8.2',
                        'geo' =>  ''
                    ),
   7 => array(
                        'id' => 11811,
                        'label' => 'South East',
                        'pop' => '8.6',
                        'geo' =>  ''
                    ),
   8 => array(
                        'id' => 11814,
                        'label' => 'South West',
                        'pop' => '5.3',
                        'geo' =>  ''
                    ),
   9 => array(
                        'id' => 11813,
                        'label' => 'Wales',
                        'pop' => '3.1',
                        'geo' =>  ''
                    ),
);

$total = 0;

foreach ($regions as $region) {
    $total = $total + $region['pop'];
}

//Get GeoJSON of regions
/*
foreach ($regions as $key => $region) {
    $regions[$key]['geo'] = file_get_contents('http://mapit.mysociety.org/area/' . $region['id'] . '.geojson?simplify_tolerance=0.03');
}

$json = array(
    'type' => 'FeatureCollection',
    'features' => array()
);

foreach ($regions as $key => $region) {
    $json['features'][] = array(
        'type' => 'Feature',
        'id' => $key,
        'properties' => array(
             'name' => $region['label']),
        'geometry' => $region['geo']     
    );
}*/
?>
<body>
    <div id="chart"></div>
    <script type="text/javascript">
var data = [
    <?php foreach ($regions as $region) echo $region['pop'] / 30  . ', '; ?>
];
/*var data = [
  , .187, .198, , .133, .175, .151, , .1, .125, .171, , .172, .133, , .108,
  .142, .167, .201, .175, .159, .169, .177, .141, .163, .117, .182, .153, .195,
  .189, .134, .163, .133, .151, .145, .13, .139, .169, .164, .175, .135, .152,
  .169, , .132, .167, .139, .184, .159, .14, .146, .157, , .139, .183, .16, .143
];*/


var svg = d3.select("#chart").append("svg")
    .attr("width", 960)
    .attr("height", 500);

jQuery.getJSON("http://dev.aendrew.com/eur.php?callback=?", function (json) {
  var path = d3.geo.path();
  var m = d3.geo.mercator();
  m.scale(16000);
  m.translate([480,3050]);
  path.projection(m);
console.dir(json);
  svg.append("g")
      .attr("class", "black")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path);

  svg.append("g")
      .attr("class", "white")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path);

  svg.append("g")
      .attr("class", "grey")
    .selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path)
      .attr("transform", function(d) {
        var centroid = path.centroid(d),
            x = centroid[0],
            y = centroid[1];
        return "translate(" + x + "," + y + ")"
            + "scale(" + Math.sqrt(data[+d.id] * 5 || 0) + ")"
            + "translate(" + -x + "," + -y + ")";
      })
      .style("stroke-width", function(d) {
        return 1 / Math.sqrt(data[+d.id] * 5 || 1);
      });

});


    </script>

</body>
</html>
