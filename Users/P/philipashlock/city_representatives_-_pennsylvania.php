<?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';

    $csv_file_path = '/Users/philipashlock/Sites/test.dev/scraper/csv_tmp/city_pa.csv';

} 

if ($run_environment == 'prod') {
    $csv_file_path = '/tmp/city_pa.csv';        
}

require 'scraperwiki/simple_html_dom.php';


/// -------------------------------- First download the file --------------------------------

$url  = 'http://munstatspa.dced.state.pa.us/ReportViewer.axd?R=LocalOfficial&F=C';


if ($run_environment == 'prod') {
 $ch = curl_init($url);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 curl_setopt($ch, CURLOPT_ENCODING, 'UTF-8');
 
 $data = curl_exec($ch);
 
 curl_close($ch);
 
// solving for weird encoding issues
 $data = iconv('utf-16le', 'utf-8', $data);

 file_put_contents($csv_file_path, $data);

 unset($data);

}
                                          
/// ------------------------------------------------------------------------------------------



$output = get_sources($csv_file_path);


if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($output);
}

function get_sources($csv_file_path) {
    
global $run_environment;
global $max_records;

    if(($handle = fopen($csv_file_path, 'r')) !== false)
    {
        // get the first row, which contains the column-titles (if necessary)
        $header = fgetcsv($handle);

        $header = rmBOM($header[0]);
        $header = explode("\t", $header);

        $count = 1;

        // loop through the file line-by-line
        while(($data = fgetcsv($handle)) !== false)
        {
            // resort/rewrite data and insert into DB here
            // try to use conditions sparingly here, as those will cause slow-performance
            
             //$data = iconv('utf-16le', 'utf-8', $data[0]);                                                 
            $data = explode("\t", $data[0]);    
            
            foreach ($data as $key => $value) {
                
                $row[$header[$key]] = $value;
                
            }
            
            if ($run_environment == 'dev') {
                $rows[] = $row;
                if($count > $max_records) break;// { var_dump($rows); exit;}
                $count++;
            }
            
            if ($run_environment == 'prod') {            
                scraperwiki::save(array('MUNICIPALITY_NAME', 'TITLE', 'NAME'), $row);
            }
            

            unset($row);
        }
        fclose($handle);
    }

if ($run_environment == 'dev') {    
    return $rows;    
} else {
    return true;
}
    
}


function rmBOM($data){
    if(substr($data, 0, 3) == pack('CCC', 239, 187, 191)) {
        return substr($data, 3);
    }
    return $data;
}



?><?php

$run_environment = 'prod'; // either 'dev' or 'prod'
$max_records = 4; // only used for testing

if ($run_environment == 'dev') {
    error_reporting(E_ALL);
    ini_set('display_errors','On');    

    require 'scraperwiki.php';

    $csv_file_path = '/Users/philipashlock/Sites/test.dev/scraper/csv_tmp/city_pa.csv';

} 

if ($run_environment == 'prod') {
    $csv_file_path = '/tmp/city_pa.csv';        
}

require 'scraperwiki/simple_html_dom.php';


/// -------------------------------- First download the file --------------------------------

$url  = 'http://munstatspa.dced.state.pa.us/ReportViewer.axd?R=LocalOfficial&F=C';


if ($run_environment == 'prod') {
 $ch = curl_init($url);
 curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
 curl_setopt($ch, CURLOPT_ENCODING, 'UTF-8');
 
 $data = curl_exec($ch);
 
 curl_close($ch);
 
// solving for weird encoding issues
 $data = iconv('utf-16le', 'utf-8', $data);

 file_put_contents($csv_file_path, $data);

 unset($data);

}
                                          
/// ------------------------------------------------------------------------------------------



$output = get_sources($csv_file_path);


if ($run_environment == 'dev') {
    header('Content-type: application/json');
    print json_encode($output);
}

function get_sources($csv_file_path) {
    
global $run_environment;
global $max_records;

    if(($handle = fopen($csv_file_path, 'r')) !== false)
    {
        // get the first row, which contains the column-titles (if necessary)
        $header = fgetcsv($handle);

        $header = rmBOM($header[0]);
        $header = explode("\t", $header);

        $count = 1;

        // loop through the file line-by-line
        while(($data = fgetcsv($handle)) !== false)
        {
            // resort/rewrite data and insert into DB here
            // try to use conditions sparingly here, as those will cause slow-performance
            
             //$data = iconv('utf-16le', 'utf-8', $data[0]);                                                 
            $data = explode("\t", $data[0]);    
            
            foreach ($data as $key => $value) {
                
                $row[$header[$key]] = $value;
                
            }
            
            if ($run_environment == 'dev') {
                $rows[] = $row;
                if($count > $max_records) break;// { var_dump($rows); exit;}
                $count++;
            }
            
            if ($run_environment == 'prod') {            
                scraperwiki::save(array('MUNICIPALITY_NAME', 'TITLE', 'NAME'), $row);
            }
            

            unset($row);
        }
        fclose($handle);
    }

if ($run_environment == 'dev') {    
    return $rows;    
} else {
    return true;
}
    
}


function rmBOM($data){
    if(substr($data, 0, 3) == pack('CCC', 239, 187, 191)) {
        return substr($data, 3);
    }
    return $data;
}



?>