<?php

$data = scraperWiki::scrape('https://docs.google.com/spreadsheet/pub?key=0AlzYR-LjR-j9dGVBU2ktd3RPUjFGNFppU0lMNnAzR3c&single=true&gid=0&output=csv');
$lines = explode("\n", $data);

for($i=0;$i<count($lines);$i++){  
    $columns;      
    
    if($i == 0){ //loop over all columns
        $columns = str_getcsv($lines[0]);   
    }else{
        $row = str_getcsv($lines[$i]);
        $record = array(
            $columns[0] => $row[0],
            $columns[1] => $row[1],
            $columns[2] => $row[2],
            $columns[3] => $row[3],
            $columns[4] => $row[4],
            $columns[5] => $row[5],
            $columns[6] => $row[6],
            $columns[7] => $row[7],
            $columns[8] => $row[8],
            $columns[9] => $row[9],
            $columns[10] => $row[10],
            $columns[11] => $row[11]
        );
        print_r($record);
        scraperwiki::save($columns, $record);
    }
}

?>
<?php

$data = scraperWiki::scrape('https://docs.google.com/spreadsheet/pub?key=0AlzYR-LjR-j9dGVBU2ktd3RPUjFGNFppU0lMNnAzR3c&single=true&gid=0&output=csv');
$lines = explode("\n", $data);

for($i=0;$i<count($lines);$i++){  
    $columns;      
    
    if($i == 0){ //loop over all columns
        $columns = str_getcsv($lines[0]);   
    }else{
        $row = str_getcsv($lines[$i]);
        $record = array(
            $columns[0] => $row[0],
            $columns[1] => $row[1],
            $columns[2] => $row[2],
            $columns[3] => $row[3],
            $columns[4] => $row[4],
            $columns[5] => $row[5],
            $columns[6] => $row[6],
            $columns[7] => $row[7],
            $columns[8] => $row[8],
            $columns[9] => $row[9],
            $columns[10] => $row[10],
            $columns[11] => $row[11]
        );
        print_r($record);
        scraperwiki::save($columns, $record);
    }
}

?>
