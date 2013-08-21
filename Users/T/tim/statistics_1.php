<?php

#Don't know how to use sql directly; maybe I need to save it in a diffrent way first?....
#http://scraperwiki.com/api/1.0/explore/scraperwiki.datastore.sqlite
#anyway it's got no tables 
#$sql="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;";
#$x = scraperwiki::sqlitecommand("execute", $sql);
#print_r($x); 
#exit(0);

#pull everything # crazy slow #bad idea
$short_name="wwwclimateweatherofficegcca";
scraperwiki::attach($short_name, 'src');
$data = scraperwiki::select("* from swdata");
$key= array('year', 'month', 'day', 'hour');
foreach ($data as $row){
    $newData = array();
    foreach ($row as $k => $value){
        $newData[$k]=$value;
    }
    scraperwiki::save_sqlite($key, $data);
}
#$sql="SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;";
#$x = scraperwiki::sqlitecommand("execute", $sql);
#print_r($x);
$sql="SELECT count(*) as number FROM swdata;";
$x = scraperwiki::sqlitecommand("execute", $sql);
echo "rows:".$x->data[0][0]."<br/>\n";

$sql="SELECT COUNT(*) as n, MAX(direction) as d FROM swdata GROUP BY direction;";
$x = scraperwiki::sqlitecommand("execute", $sql);
$x=$x->data;
echo "totals by direction:";
foreach ($x as $row){
    foreach ($row as $cell){
         echo $cell." ";
    }
    echo ",";
}
echo "<br/>\n";

$sql="SELECT COUNT(*) as n, MAX(hour) as h FROM swdata WHERE direction='N' GROUP BY hour;";
 $x = scraperwiki::sqliteexecute($sql);
 $x=$x->data;
 echo "N totals by hour:";
 foreach ($x as $row){
      foreach ($row as $cell){
           echo $cell." ";
      }
      echo ",";
 }
 echo "<br/>\n";
  
$sql="SELECT COUNT(*) as n, MAX(hour) as h FROM swdata WHERE direction='E' GROUP BY hour;";
  $x = scraperwiki::sqliteexecute($sql);
  $x=$x->data;
  echo "E totals by hour:";
  foreach ($x as $row){
       foreach ($row as $cell){
            echo $cell." ";
       }
       echo ",";
  }
  echo "<br/>\n";
  
$sql="SELECT COUNT(*) as n, MAX(hour) as h FROM swdata WHERE direction='S' GROUP BY hour;";
  $x = scraperwiki::sqliteexecute($sql);
  $x=$x->data;
  echo "S totals by hour:";
  foreach ($x as $row){
       foreach ($row as $cell){
            echo $cell." ";
       }
       echo ",";
  }
  echo "<br/>\n";
  
$sql="SELECT COUNT(*) as n, MAX(hour) as h FROM swdata WHERE direction='W' GROUP BY hour;";
  $x = scraperwiki::sqliteexecute($sql);
  $x=$x->data;
  echo "W totals by hour:";
  foreach ($x as $row){
       foreach ($row as $cell){
            echo $cell." ";
       }
       echo ",";
  }
  echo "<br/>\n";
  
$sql="SELECT COUNT(*) as n, MAX(hour) as h FROM swdata WHERE direction='' GROUP BY hour;";
  $x = scraperwiki::sqliteexecute($sql);
  $x=$x->data;
  echo "Still totals by hour:";
  foreach ($x as $row){
       foreach ($row as $cell){
            echo $cell." ";
       }
       echo ",";
  }
  echo "<br/>\n";
  
?>


