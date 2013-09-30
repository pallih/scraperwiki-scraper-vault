<?php
$json_output = json_decode(file_get_contents("https://api.twitter.com/1/trends/1.json"));
foreach ($json_output->trends as $datetime=>$vals ) {

    foreach($vals as $trend){
        $record = array(
        'name' => $trend->name, 
        'promoted_content' => $trend->promoted_content);
   scraperwiki::save_sqlite("",$record); 
}
}





?>
<?php
$json_output = json_decode(file_get_contents("https://api.twitter.com/1/trends/1.json"));
foreach ($json_output->trends as $datetime=>$vals ) {

    foreach($vals as $trend){
        $record = array(
        'name' => $trend->name, 
        'promoted_content' => $trend->promoted_content);
   scraperwiki::save_sqlite("",$record); 
}
}





?>
