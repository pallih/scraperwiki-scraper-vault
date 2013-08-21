<?php

$url = "http://www.healthwatch.co.uk/find-your-local-organisation";
$handle = @fopen($url, "r");
if ($handle) {
    $count = 0;
    $line = "";
    while($count<91){
        $line = fgets($handle);
        $count++;
    }
    $json = str_replace("<script>jQuery.extend(Drupal.settings, ", "", $line);
    $json = str_replace(");</script>", "", $json);
    $data = json_decode($json, true);
    $data = json_decode($data["lho_map_search"]["data"], true);
    
    $orgs_count = 0;
    foreach($data as $data_key=>$data_item){
        scraperwiki::save_sqlite(array('nid'), $data_item);
        $orgs_count++;
    }
    print number_format($orgs_count) . " organisations added to database.";
} else {
    print "Cannot open file.";
}

?>
