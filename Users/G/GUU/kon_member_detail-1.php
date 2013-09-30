<?php
    $sourcescraper = 'kon_member_detail'; 
    $data = scraperwiki::getData($sourcescraper); 
    $chars = array();
    $cols = array();

    function lvl_range($level) 
    {
        $lvl = intval($level);
        $range = $lvl - ( $lvl % 10 );
        if( $lvl <= 10 ) { $st = 0; $en = 10; }
        elseif( $lvl >= 60 ) { $st = 60; $en = 66; }
        else { $st = $range; $en = $range+10; }
    
        return "Level $st-".($en-1);
    }
    foreach( $data as $member )
    {
        $stats = array();
        $stats[] = "{v:'{$member->name}'}";
        $stats[] = "{v:'{$member->class}'}";
        $stats[] = "{v:{$member->level}}";
        $stats[] = "{v:'". lvl_range($member->level)."'}";
        $stats[] = "{v:'{$member->race}'}";
        $stats[] = "{v:{$member->morale}}";
        $stats[] = "{v:{$member->power}}";
        $stats[] = "{v:{$member->armour}}";
        $chars[] = "{c:[". join($stats,',') ."] }";
    }

    $cols[] = '{id:"name",label:"Name",type:"string"}';
    $cols[] = '{id:"class",label:"Class",type:"string"}';
    $cols[] = '{id:"level",label:"Level",type:"number"}';
    $cols[] = '{id:"level_range",label:"Level range",type:"string"}';
    $cols[] = '{id:"race",label:"Race",type:"string"}';
    $cols[] = '{id:"morale",label:"Morale",type:"number"}';
    $cols[] = '{id:"power",label:"Power",type:"number"}';
    $cols[] = '{id:"armour",label:"Armour",type:"number"}';
    
    $str = "{cols: [". join($cols,',') ."], rows: [". join($chars, ',') ."] }";

?>
<html>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
    google.load("visualization", "1", {packages:["table", "corechart"]});
    var JSONObject = <?=$str?>;
    var column_index = {name:0, cls:1, level:2, level_range:3, race:4, morale:5, power:6, armour:7};
    function drawVisualization() {
      // Create and populate the data table.
      var data = new google.visualization.DataTable(JSONObject, 0.5);

      var result = google.visualization.data.group(
          data, 
          [column_index.cls,column_index.race],
          [{'column': column_index.cls, 'aggregation': google.visualization.data.count, 'type': 'number', label: 'Members'},
           {'column': column_index.level, 'aggregation': google.visualization.data.min, 'type': 'number', label: 'Min lvl'},
           {'column': column_index.level, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max lvl'},
           {'column': column_index.morale, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max morale'},
           {'column': column_index.power, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max power'},
           {'column': column_index.morale, 'aggregation': google.visualization.data.avg, 'type': 'number', label: 'avg morale'},
           {'column': column_index.power, 'aggregation': google.visualization.data.avg, 'type': 'number', label: 'avg power'}  
          ]
        );

       var formatter = new google.visualization.NumberFormat({fractionDigits:0,groupingSymbol:''});
       formatter.format(result, 7);
       formatter.format(result, 8);


       var table = new google.visualization.Table(document.getElementById('table'));
       table.draw(result);

      var classes = google.visualization.data.group(
          data, 
          [column_index.cls],
          [{'column': column_index.cls , 'aggregation': google.visualization.data.count, 'type': 'number'}]
        );

       var view = new google.visualization.DataView(classes);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie1'));
       chart.draw(view, {width: 600, height: 500, is3D: true});


      var races = google.visualization.data.group(
          data, 
          [column_index.race],
          [{'column': column_index.race, 'aggregation': google.visualization.data.count, 'type': 'number'}]
        );

       var view = new google.visualization.DataView(races);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie2'));
       chart.draw(view, {width: 600, height: 500, is3D: true});

      var levels = google.visualization.data.group(
          data, 
          [column_index.level_range],
          [{'column':column_index.level_range, 'aggregation': google.visualization.data.count, 'type': 'number', label: 'Level range'}]
        );

       var view = new google.visualization.DataView(levels);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie3'));
       chart.draw(view, {width: 600, height: 500, is3D: true});


/*
       // GUARDIAN stats
       var view = new google.visualization.DataView(data);
       view.setRows(view.getFilteredRows([{column: 1, value: 'Guardian' }]));

      view.setColumns([0, 2]);
      data.sort([{column: 2}, {column: 0}]);
      var chart = new google.visualization.ColumnChart(document.getElementById('info'));
      chart.draw(view, {width: 900, height: 500});

      // LORE-MASTER stats
       var view = new google.visualization.DataView(data);
       view.setRows(view.getFilteredRows([{column: 1, value: 'Lore-master' }]));

      view.setColumns([0, 2]);
      data.sort([{column: 2}, {column: 0}]);
      var chart = new google.visualization.ColumnChart(document.getElementById('info2'));
      chart.draw(view, {width: 900, height: 500});
*/

    }
    google.setOnLoadCallback(drawVisualization);  
</script>
<br />
<h1> KoN stats</h1>
<div id="table" ></div>
<div id="pie1" ></div>
<div id="pie2" ></div>
<div id="pie3" ></div>
<div id="info" ></div>
<div id="info2" ></div>

<?php
    $sourcescraper = 'kon_member_detail'; 
    $data = scraperwiki::getData($sourcescraper); 
    $chars = array();
    $cols = array();

    function lvl_range($level) 
    {
        $lvl = intval($level);
        $range = $lvl - ( $lvl % 10 );
        if( $lvl <= 10 ) { $st = 0; $en = 10; }
        elseif( $lvl >= 60 ) { $st = 60; $en = 66; }
        else { $st = $range; $en = $range+10; }
    
        return "Level $st-".($en-1);
    }
    foreach( $data as $member )
    {
        $stats = array();
        $stats[] = "{v:'{$member->name}'}";
        $stats[] = "{v:'{$member->class}'}";
        $stats[] = "{v:{$member->level}}";
        $stats[] = "{v:'". lvl_range($member->level)."'}";
        $stats[] = "{v:'{$member->race}'}";
        $stats[] = "{v:{$member->morale}}";
        $stats[] = "{v:{$member->power}}";
        $stats[] = "{v:{$member->armour}}";
        $chars[] = "{c:[". join($stats,',') ."] }";
    }

    $cols[] = '{id:"name",label:"Name",type:"string"}';
    $cols[] = '{id:"class",label:"Class",type:"string"}';
    $cols[] = '{id:"level",label:"Level",type:"number"}';
    $cols[] = '{id:"level_range",label:"Level range",type:"string"}';
    $cols[] = '{id:"race",label:"Race",type:"string"}';
    $cols[] = '{id:"morale",label:"Morale",type:"number"}';
    $cols[] = '{id:"power",label:"Power",type:"number"}';
    $cols[] = '{id:"armour",label:"Armour",type:"number"}';
    
    $str = "{cols: [". join($cols,',') ."], rows: [". join($chars, ',') ."] }";

?>
<html>
  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">
    google.load("visualization", "1", {packages:["table", "corechart"]});
    var JSONObject = <?=$str?>;
    var column_index = {name:0, cls:1, level:2, level_range:3, race:4, morale:5, power:6, armour:7};
    function drawVisualization() {
      // Create and populate the data table.
      var data = new google.visualization.DataTable(JSONObject, 0.5);

      var result = google.visualization.data.group(
          data, 
          [column_index.cls,column_index.race],
          [{'column': column_index.cls, 'aggregation': google.visualization.data.count, 'type': 'number', label: 'Members'},
           {'column': column_index.level, 'aggregation': google.visualization.data.min, 'type': 'number', label: 'Min lvl'},
           {'column': column_index.level, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max lvl'},
           {'column': column_index.morale, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max morale'},
           {'column': column_index.power, 'aggregation': google.visualization.data.max, 'type': 'number', label: 'Max power'},
           {'column': column_index.morale, 'aggregation': google.visualization.data.avg, 'type': 'number', label: 'avg morale'},
           {'column': column_index.power, 'aggregation': google.visualization.data.avg, 'type': 'number', label: 'avg power'}  
          ]
        );

       var formatter = new google.visualization.NumberFormat({fractionDigits:0,groupingSymbol:''});
       formatter.format(result, 7);
       formatter.format(result, 8);


       var table = new google.visualization.Table(document.getElementById('table'));
       table.draw(result);

      var classes = google.visualization.data.group(
          data, 
          [column_index.cls],
          [{'column': column_index.cls , 'aggregation': google.visualization.data.count, 'type': 'number'}]
        );

       var view = new google.visualization.DataView(classes);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie1'));
       chart.draw(view, {width: 600, height: 500, is3D: true});


      var races = google.visualization.data.group(
          data, 
          [column_index.race],
          [{'column': column_index.race, 'aggregation': google.visualization.data.count, 'type': 'number'}]
        );

       var view = new google.visualization.DataView(races);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie2'));
       chart.draw(view, {width: 600, height: 500, is3D: true});

      var levels = google.visualization.data.group(
          data, 
          [column_index.level_range],
          [{'column':column_index.level_range, 'aggregation': google.visualization.data.count, 'type': 'number', label: 'Level range'}]
        );

       var view = new google.visualization.DataView(levels);
       view.setColumns([0, 1]);
       var chart = new google.visualization.PieChart(document.getElementById('pie3'));
       chart.draw(view, {width: 600, height: 500, is3D: true});


/*
       // GUARDIAN stats
       var view = new google.visualization.DataView(data);
       view.setRows(view.getFilteredRows([{column: 1, value: 'Guardian' }]));

      view.setColumns([0, 2]);
      data.sort([{column: 2}, {column: 0}]);
      var chart = new google.visualization.ColumnChart(document.getElementById('info'));
      chart.draw(view, {width: 900, height: 500});

      // LORE-MASTER stats
       var view = new google.visualization.DataView(data);
       view.setRows(view.getFilteredRows([{column: 1, value: 'Lore-master' }]));

      view.setColumns([0, 2]);
      data.sort([{column: 2}, {column: 0}]);
      var chart = new google.visualization.ColumnChart(document.getElementById('info2'));
      chart.draw(view, {width: 900, height: 500});
*/

    }
    google.setOnLoadCallback(drawVisualization);  
</script>
<br />
<h1> KoN stats</h1>
<div id="table" ></div>
<div id="pie1" ></div>
<div id="pie2" ></div>
<div id="pie3" ></div>
<div id="info" ></div>
<div id="info2" ></div>

