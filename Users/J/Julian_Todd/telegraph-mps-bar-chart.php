<?php
// Warning: this View is buggy (doesn't seem to count all the candidates).  My PHP coding is not very good -- JT 
    $sourcescraper = 'telegraph-candidate-info'; 

    $party = 'Conservative'; 
    //$party = 'Liberal Democrat';
    //$party = 'Labour';

    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 11; 

    $key = $keys[$keyindex]; 
    $counts = array();
    $countselect = array();
    $totalcandidates = 0; 
    $totalelected = 0; 
    $s = scraperwiki::getData($sourcescraper, $limit=2000); 
    foreach ($s as $c => $row)
    {
        $elected = false; 
        $svalue = 0; 
        $arr = array('status'=>'', $key=>0, 'party'=>0); 
        foreach ($row as $k => $value) 
            $arr[$k] = $value; 
        if ($party && ($arr['party'] !== $party))
            continue; 

        if ($arr[$key] !== 0)
        {
            $svalue = $arr[$key]; 
            if (!array_key_exists($svalue, $counts))
            {
                $counts[$svalue] =  0; 
                $countselect[$svalue] = 0; 
            }
            $counts[$svalue] += 1; 
            $totalcandidates += 1; 
        }
        if (($arr['status'] == 'ELECTED MP 2010') && ($svalue !== 0))
        {
            $countselect[$svalue] += 1;
            $totalelected += 1;
        }
    }
?>
<h2>Thinned by party: <b><?php echo $party ?></b></h2>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['BarChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of candidates');
    data.addColumn('number', 'Number of elected');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $evalue = $countselect[$k]; 
        echo "data.setValue($i, 2, $evalue);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 500, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    
<p>Total candidates <?php echo $totalcandidates ?>, Total elected <?php echo $totalelected ?> </p>
<?php
// Warning: this View is buggy (doesn't seem to count all the candidates).  My PHP coding is not very good -- JT 
    $sourcescraper = 'telegraph-candidate-info'; 

    $party = 'Conservative'; 
    //$party = 'Liberal Democrat';
    //$party = 'Labour';

    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 11; 

    $key = $keys[$keyindex]; 
    $counts = array();
    $countselect = array();
    $totalcandidates = 0; 
    $totalelected = 0; 
    $s = scraperwiki::getData($sourcescraper, $limit=2000); 
    foreach ($s as $c => $row)
    {
        $elected = false; 
        $svalue = 0; 
        $arr = array('status'=>'', $key=>0, 'party'=>0); 
        foreach ($row as $k => $value) 
            $arr[$k] = $value; 
        if ($party && ($arr['party'] !== $party))
            continue; 

        if ($arr[$key] !== 0)
        {
            $svalue = $arr[$key]; 
            if (!array_key_exists($svalue, $counts))
            {
                $counts[$svalue] =  0; 
                $countselect[$svalue] = 0; 
            }
            $counts[$svalue] += 1; 
            $totalcandidates += 1; 
        }
        if (($arr['status'] == 'ELECTED MP 2010') && ($svalue !== 0))
        {
            $countselect[$svalue] += 1;
            $totalelected += 1;
        }
    }
?>
<h2>Thinned by party: <b><?php echo $party ?></b></h2>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['BarChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of candidates');
    data.addColumn('number', 'Number of elected');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $evalue = $countselect[$k]; 
        echo "data.setValue($i, 2, $evalue);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 500, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    
<p>Total candidates <?php echo $totalcandidates ?>, Total elected <?php echo $totalelected ?> </p>
<?php
// Warning: this View is buggy (doesn't seem to count all the candidates).  My PHP coding is not very good -- JT 
    $sourcescraper = 'telegraph-candidate-info'; 

    $party = 'Conservative'; 
    //$party = 'Liberal Democrat';
    //$party = 'Labour';

    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 11; 

    $key = $keys[$keyindex]; 
    $counts = array();
    $countselect = array();
    $totalcandidates = 0; 
    $totalelected = 0; 
    $s = scraperwiki::getData($sourcescraper, $limit=2000); 
    foreach ($s as $c => $row)
    {
        $elected = false; 
        $svalue = 0; 
        $arr = array('status'=>'', $key=>0, 'party'=>0); 
        foreach ($row as $k => $value) 
            $arr[$k] = $value; 
        if ($party && ($arr['party'] !== $party))
            continue; 

        if ($arr[$key] !== 0)
        {
            $svalue = $arr[$key]; 
            if (!array_key_exists($svalue, $counts))
            {
                $counts[$svalue] =  0; 
                $countselect[$svalue] = 0; 
            }
            $counts[$svalue] += 1; 
            $totalcandidates += 1; 
        }
        if (($arr['status'] == 'ELECTED MP 2010') && ($svalue !== 0))
        {
            $countselect[$svalue] += 1;
            $totalelected += 1;
        }
    }
?>
<h2>Thinned by party: <b><?php echo $party ?></b></h2>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['BarChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of candidates');
    data.addColumn('number', 'Number of elected');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $evalue = $countselect[$k]; 
        echo "data.setValue($i, 2, $evalue);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 500, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    
<p>Total candidates <?php echo $totalcandidates ?>, Total elected <?php echo $totalelected ?> </p>
<?php
// Warning: this View is buggy (doesn't seem to count all the candidates).  My PHP coding is not very good -- JT 
    $sourcescraper = 'telegraph-candidate-info'; 

    $party = 'Conservative'; 
    //$party = 'Liberal Democrat';
    //$party = 'Labour';

    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 11; 

    $key = $keys[$keyindex]; 
    $counts = array();
    $countselect = array();
    $totalcandidates = 0; 
    $totalelected = 0; 
    $s = scraperwiki::getData($sourcescraper, $limit=2000); 
    foreach ($s as $c => $row)
    {
        $elected = false; 
        $svalue = 0; 
        $arr = array('status'=>'', $key=>0, 'party'=>0); 
        foreach ($row as $k => $value) 
            $arr[$k] = $value; 
        if ($party && ($arr['party'] !== $party))
            continue; 

        if ($arr[$key] !== 0)
        {
            $svalue = $arr[$key]; 
            if (!array_key_exists($svalue, $counts))
            {
                $counts[$svalue] =  0; 
                $countselect[$svalue] = 0; 
            }
            $counts[$svalue] += 1; 
            $totalcandidates += 1; 
        }
        if (($arr['status'] == 'ELECTED MP 2010') && ($svalue !== 0))
        {
            $countselect[$svalue] += 1;
            $totalelected += 1;
        }
    }
?>
<h2>Thinned by party: <b><?php echo $party ?></b></h2>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['BarChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of candidates');
    data.addColumn('number', 'Number of elected');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $evalue = $countselect[$k]; 
        echo "data.setValue($i, 2, $evalue);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 500, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    
<p>Total candidates <?php echo $totalcandidates ?>, Total elected <?php echo $totalelected ?> </p>
<?php
// Warning: this View is buggy (doesn't seem to count all the candidates).  My PHP coding is not very good -- JT 
    $sourcescraper = 'telegraph-candidate-info'; 

    $party = 'Conservative'; 
    //$party = 'Liberal Democrat';
    //$party = 'Labour';

    $keys = scraperwiki::getKeys($sourcescraper); 
    $keyindex = getenv("URLQUERY"); 
    if ($keyindex == False)
        $keyindex = 11; 

    $key = $keys[$keyindex]; 
    $counts = array();
    $countselect = array();
    $totalcandidates = 0; 
    $totalelected = 0; 
    $s = scraperwiki::getData($sourcescraper, $limit=2000); 
    foreach ($s as $c => $row)
    {
        $elected = false; 
        $svalue = 0; 
        $arr = array('status'=>'', $key=>0, 'party'=>0); 
        foreach ($row as $k => $value) 
            $arr[$k] = $value; 
        if ($party && ($arr['party'] !== $party))
            continue; 

        if ($arr[$key] !== 0)
        {
            $svalue = $arr[$key]; 
            if (!array_key_exists($svalue, $counts))
            {
                $counts[$svalue] =  0; 
                $countselect[$svalue] = 0; 
            }
            $counts[$svalue] += 1; 
            $totalcandidates += 1; 
        }
        if (($arr['status'] == 'ELECTED MP 2010') && ($svalue !== 0))
        {
            $countselect[$svalue] += 1;
            $totalelected += 1;
        }
    }
?>
<h2>Thinned by party: <b><?php echo $party ?></b></h2>

  <script type="text/javascript" src="http://www.google.com/jsapi"></script>
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
  <script type="text/javascript">

google.load('visualization', '1', {packages: ['BarChart']});

function makechart()
{
    var data = new google.visualization.DataTable();
    data.addRows(<?php echo count($counts) ?>);
    data.addColumn('string', '<?php echo $key ?>');
    data.addColumn('number', 'Number of candidates');
    data.addColumn('number', 'Number of elected');

    <?php 
    $i = 0; 
    foreach ($counts as $k => $value)
    {
        echo "data.setValue($i, 0, '$k');";
        echo "data.setValue($i, 1, $value);";
        $evalue = $countselect[$k]; 
        echo "data.setValue($i, 2, $evalue);";
        $i += 1; 
    }
    ?>
        
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    chart.draw(data, {width: 1200, height: 500, title: '<?php echo "$key from $sourcescraper" ?>'});
}
    
google.setOnLoadCallback(makechart);
      
</script>
<div id="visualization" style="width: 800px; height: 500px;"></div>
<a href="http://code.google.com/apis/visualization/documentation/gallery/barchart.html">Google bar chart vizualization documentation</a>

<p><b>Other keys:</b> 
<?php for ($i = 0; $i < count($keys); $i++)
    echo '<a href="?'.$i.'">'.$keys[$i]."</a> "
?>   
</p>        
    
<p>Total candidates <?php echo $totalcandidates ?>, Total elected <?php echo $totalelected ?> </p>
