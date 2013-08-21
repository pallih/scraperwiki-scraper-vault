<?php
    $sourcescraper = 'courts-ni-judicial-decisions'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = 'judgename'; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=950); 
    foreach ($s as $c => $row)
    {
        foreach ($row as $k => $value) 
        {
            if ($k == $key)
            {
                if (!array_key_exists($value, $counts))
                    $counts[$value] =  0; 
                $counts[$value] += 1; 
            }
        }
    }
?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['PieChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.PieChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 800, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 800px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    

<?php
    $sourcescraper = 'courts-ni-judicial-decisions'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = 'judgename'; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=950); 
    foreach ($s as $c => $row)
    {
        foreach ($row as $k => $value) 
        {
            if ($k == $key)
            {
                if (!array_key_exists($value, $counts))
                    $counts[$value] =  0; 
                $counts[$value] += 1; 
            }
        }
    }
?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['PieChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.PieChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 800, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 800px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    

<?php
    $sourcescraper = 'courts-ni-judicial-decisions'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = 'judgename'; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=950); 
    foreach ($s as $c => $row)
    {
        foreach ($row as $k => $value) 
        {
            if ($k == $key)
            {
                if (!array_key_exists($value, $counts))
                    $counts[$value] =  0; 
                $counts[$value] += 1; 
            }
        }
    }
?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['PieChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.PieChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 800, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 800px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    

<?php
    $sourcescraper = 'courts-ni-judicial-decisions'; 
    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 4; 
    $key = 'judgename'; 
    $counts = array();
    $s = scraperwiki::getData($sourcescraper, $limit=950); 
    foreach ($s as $c => $row)
    {
        foreach ($row as $k => $value) 
        {
            if ($k == $key)
            {
                if (!array_key_exists($value, $counts))
                    $counts[$value] =  0; 
                $counts[$value] += 1; 
            }
        }
    }
?>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['PieChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of data points');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.PieChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 800, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 800px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    

