<?php
    $sourcescraper = 'mr_no_vote'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = $keys[$keyindex]; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=250); 

$real_data = array();

$parties = array();
    foreach ($s as $c => $row)
    {
        if(($row->type) == 'result'){
            $parties[$row->party] = 1;
            $real_data[$row->area][$row->party] = $row->real_perc;
        }
    }

    unset($s);


    $raw_data = array();
    $raw_keys = array();
    foreach($real_data as $k => $rd){
        
        foreach($parties as $vk=>$v){
            $parties[$vk] = 0;
        }

        $raw_keys[] = $k;
        foreach($rd as $kp => $rp){
            $parties[$kp] = 1;
            $raw_data[$kp][] = $rp;
        }

        foreach($parties as $vk=>$v){
            if($parties[$vk] != 1){
                $raw_data[$vk][] = 0;
            }
        }

    }


?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['corechart']});

if(google == 'undefined')
    alert('Google failed to connect');

function makechart()
{
    var data = new google.visualization.DataTable();
    /*data.addRows(<?php echo count($raw_keys) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');*/

   <?php 
        
        $st_raw = array();

       foreach($raw_data as $p => $arp){
            $st_raw[] = "'".($p)."'," . implode(',',$arp);
       }

       $st_raw = 'var raw_data = [[' . implode("],\n[",$st_raw) . ']];';

        $st_areas = "var areas = ['" . implode("','", $raw_keys) . "']";

    /* $r = 0; 
    $i = 0;
    foreach ($real_data as $k => $value)
    {
        foreach($value as $vk => $val){
            
            echo "data.setValue($r, 0, '{$value->name}');";
            echo "data.setValue($r, 1, $value->real_perc);";
               
        }
        $r++; 
        $i++;
}*/
    ?>
        
        /* var chart = new google.visualization.BarChart(document.getElementById('visualization'));
        chart.draw(data, {width: 1200, height: 300, title: '<?php echo "$key from $sourcescraper" ?>'});*/

    <?php
        print $st_raw ."\n" . $st_areas;
    ?>


  data.addColumn('string', 'Area');
  for (var i = 0; i  < raw_data.length; ++i) {
    data.addColumn('number', raw_data[i][0]);    
  }
  data.addRows(areas.length);

  for (var j = 0; j < areas.length; ++j) {    
    data.setValue(j, 0, areas[j].toString());    
  }
  for (var i = 0; i  < raw_data.length; ++i) {
    for (var j = 1; j  < raw_data[i].length; ++j) {
      data.setValue(j-1, i+1, raw_data[i][j]);    
    }
  }
  
  // Create and draw the visualization.
  new google.visualization.ColumnChart(document.getElementById('visualization')).
      draw(data,
           {title:"Real percentage",
            width:600, height:400,
            hAxis: {title: "Area of Belfast"}}
      );
  
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>

<br>
<!--<p><a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a></p> 

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>    -->    
    

<?php
    $sourcescraper = 'mr_no_vote'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = $keys[$keyindex]; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=250); 

$real_data = array();

$parties = array();
    foreach ($s as $c => $row)
    {
        if(($row->type) == 'result'){
            $parties[$row->party] = 1;
            $real_data[$row->area][$row->party] = $row->real_perc;
        }
    }

    unset($s);


    $raw_data = array();
    $raw_keys = array();
    foreach($real_data as $k => $rd){
        
        foreach($parties as $vk=>$v){
            $parties[$vk] = 0;
        }

        $raw_keys[] = $k;
        foreach($rd as $kp => $rp){
            $parties[$kp] = 1;
            $raw_data[$kp][] = $rp;
        }

        foreach($parties as $vk=>$v){
            if($parties[$vk] != 1){
                $raw_data[$vk][] = 0;
            }
        }

    }


?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['corechart']});

if(google == 'undefined')
    alert('Google failed to connect');

function makechart()
{
    var data = new google.visualization.DataTable();
    /*data.addRows(<?php echo count($raw_keys) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');*/

   <?php 
        
        $st_raw = array();

       foreach($raw_data as $p => $arp){
            $st_raw[] = "'".($p)."'," . implode(',',$arp);
       }

       $st_raw = 'var raw_data = [[' . implode("],\n[",$st_raw) . ']];';

        $st_areas = "var areas = ['" . implode("','", $raw_keys) . "']";

    /* $r = 0; 
    $i = 0;
    foreach ($real_data as $k => $value)
    {
        foreach($value as $vk => $val){
            
            echo "data.setValue($r, 0, '{$value->name}');";
            echo "data.setValue($r, 1, $value->real_perc);";
               
        }
        $r++; 
        $i++;
}*/
    ?>
        
        /* var chart = new google.visualization.BarChart(document.getElementById('visualization'));
        chart.draw(data, {width: 1200, height: 300, title: '<?php echo "$key from $sourcescraper" ?>'});*/

    <?php
        print $st_raw ."\n" . $st_areas;
    ?>


  data.addColumn('string', 'Area');
  for (var i = 0; i  < raw_data.length; ++i) {
    data.addColumn('number', raw_data[i][0]);    
  }
  data.addRows(areas.length);

  for (var j = 0; j < areas.length; ++j) {    
    data.setValue(j, 0, areas[j].toString());    
  }
  for (var i = 0; i  < raw_data.length; ++i) {
    for (var j = 1; j  < raw_data[i].length; ++j) {
      data.setValue(j-1, i+1, raw_data[i][j]);    
    }
  }
  
  // Create and draw the visualization.
  new google.visualization.ColumnChart(document.getElementById('visualization')).
      draw(data,
           {title:"Real percentage",
            width:600, height:400,
            hAxis: {title: "Area of Belfast"}}
      );
  
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>

<br>
<!--<p><a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a></p> 

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>    -->    
    

