<?php
scraperwiki::httpresponseheader("Content-Type","text/json");
# Blank PHP 57450
for ($i=57225;$i<57250;$i++){
$html = scraperWiki::scrape("https://www.carqueryapi.com/api/0.3/?cmd=getModel&model=".$i);           
$specs = json_decode($html);
//print_r($specs[0]['model_id']);
scraperwiki::save(array("model_id"),array("model_id"=>$i,"data"=>$html));
}
?>
