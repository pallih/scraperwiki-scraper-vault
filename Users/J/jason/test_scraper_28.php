<?php 
    $url = "http://10layer.com/files/CapeOrdinarySchools.csv";
    $data=scraperWiki::scrape($url);
    $lines = explode("\n", $data);
    print "Found ".sizeof($lines)." records";
    $header = str_getcsv(array_shift($lines)); 
    foreach($lines as $row) {           
        $row = str_getcsv($row);
        $record = array_combine($header, $row);
        scraperwiki::save(array("NatEmis"), $record);
    }
?>
<?php 
    $url = "http://10layer.com/files/CapeOrdinarySchools.csv";
    $data=scraperWiki::scrape($url);
    $lines = explode("\n", $data);
    print "Found ".sizeof($lines)." records";
    $header = str_getcsv(array_shift($lines)); 
    foreach($lines as $row) {           
        $row = str_getcsv($row);
        $record = array_combine($header, $row);
        scraperwiki::save(array("NatEmis"), $record);
    }
?>
