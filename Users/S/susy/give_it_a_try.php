<?php

$header=array('int1','int2','score');
$lines_int = file('http://160.80.36.72:8080/HIserver/getInteractome');
foreach($lines_int as $line){
    $row = str_getcsv($line,";");
    #$row = explode(";", $line);
    #echo $row[0]." - ".$row[1]." - ".$row[2]."\n";
    #print_r($row);
    $record = array_combine($header, $row);
    scraperwiki::save(array('int1','int2','score'),$record);
    echo $row[0]." - ".$row[1]." - ".$row[2]."\n";
}


?>
<?php

$header=array('int1','int2','score');
$lines_int = file('http://160.80.36.72:8080/HIserver/getInteractome');
foreach($lines_int as $line){
    $row = str_getcsv($line,";");
    #$row = explode(";", $line);
    #echo $row[0]." - ".$row[1]." - ".$row[2]."\n";
    #print_r($row);
    $record = array_combine($header, $row);
    scraperwiki::save(array('int1','int2','score'),$record);
    echo $row[0]." - ".$row[1]." - ".$row[2]."\n";
}


?>
