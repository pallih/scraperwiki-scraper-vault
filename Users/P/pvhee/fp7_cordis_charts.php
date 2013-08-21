<?php


scraperwiki::attach("cordis_fp7");
$data = scraperwiki::select("* from `swdata`");
//print_r($data);

$countries = array();
foreach($data as $p) {
    $c = $p['country'];
    if (isset($countries[$c])) {
        $countries[$c]['count'] ++;
    } else {
        $countries[$c]['count'] = 1;
        $countries[$c]['site'] = 0;
        $countries[$c]['val'] = array();
    }
    $countries[$c]['site'] += $p['site'];
    $countries[$c]['data'][] = $p;
}
#print_r($countries);


?><!DOCTYPE html>
<html>
    <head>
        <title>FP7 People ITN</title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
        <script type="text/javascript" src="http://tablesorter.com/__jquery.tablesorter.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">


google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Country', 'Number of projects', 'Has site?'],
<?php 
foreach ($countries as $country => $val) {
    echo "['" . $country . "', " . $val['count'] . ", " . $val['site'] . "],";
}
?>
    ]);

    var options = {
        title: 'FP7-PEOPLE-2011-ITN: number of project coordinated by country',
        hAxis: {title: 'Country', titleTextStyle: {color: 'red'}}
     };

    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

$(function() {
    $("#table_projects").tablesorter({sortList:[[0,0],[1,0]]});
});
</script>
<style type="text/css">
tr.contacted {
  background-color:#CDCDCD;
}
</style>
    </head>
    <body>
<div id="chart_div" style="width: 900px; height: 500px;"></div>
<p>
    <table id="table_projects" class="tablesorter">
        <thead>
            <tr>
                <th>Country</th>
                <th>Acronym</th>
                <th>Site</th>
                <th>Project</th>
            </tr>
        </thead>
        <tbody>
<?php
foreach ($countries as $country => $val) {
    foreach ($val['data'] as $data) {
        
        if ($data['contacted']) {
            echo '<tr class="contacted">';
        } else {
            echo '<tr>';
        }
        echo '<td>' . $country . '</td>';
        echo '<td>' . $data['acronym'] . '</td>';
        echo '<td>';
        if ($data['site']) {
            echo '<a href="' . $data['site_url'] . '">' . $data['site_url'] . '</a>';
        } else {
            echo '-';
        }
        echo '</td>';
        echo '<td><a href="' . $data['url'] . '">' . $data['title'] . '</a></td>';

        echo '</tr>';
    }
}
?>
        </tbody>
    </table>
</p> 
    <p>Data scraped from Cordis</p>
</body>
</html>
