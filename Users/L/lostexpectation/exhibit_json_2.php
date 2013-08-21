<?php
# Blank PHP
#$sourcescraper = 'fys_apinonodata';

 # scraperwiki::attach('irish-epa-licenses', 'lic');
 #   $licenses = scraperwiki::select("* from lic.swdata");
//    $licenses = scraperwiki::getData('irish-epa-licenses');
header('Content-type: application/json');
#header('Content-type: application/json');
#scraperwiki.utils.httpresponseheader("Content-Type", "application/json");

$data = array();
#print "{ \"items\": [";
for ($i = 110; $i <= 120; $i++ ) { 
    $data .= file_get_contents('http://www.fixyourstreet.ie/api?task=incidents&by=incidentid&id=' . $i);
$data = str_replace("{\"payload\":{\"domain\":\"http:\/\/www.fixyourstreet.ie\/\","," ",$data);
$data = str_replace("\"incidents\":["," ",$data);
$data = str_replace("\"media\":[]}]","\"media\":[]",$data);
$data = str_replace("\"No Error\"}}","\"No Error\"},",$data);
#$data = str_replace("\"success\"","{\"success\"",$data);
$data = str_replace("\"success\":\"true\"},\"error\":{\"code\":\"007\",\"message\":\"No data. There are no results to show.\"}} ","",$data);
$data = str_replace("\"error\":{\"code\":\"0\",\"message\":\"No Error\"},","",$data);
$data = str_replace("incidenttitle", "label",$data);
#$data = rtrim($data,",");
#"error":{"code":"0","message":"No Error"},
#"No Error"}}
#"media":[]}]

}
$data = str_replace("Array", "",$data);


$data = str_replace("\"media\":[]},", "\"media\":[]}",$data);

$data = str_replace("}  {\"incident\":", "}, {\"incident\":",$data);
#print $data;
#} {"incident":
#} {"incident":
#}} {
#{"payload":{"domain":"http:\/\/www.fixyourstreet.ie\/",
#"incidents":[
#print "] }";
#str_replace("-"," ",$subpage)

#$s = scraperwiki::attach($sourcescraper, $limit=250);
#header('Content-type: application/json');
#print "{ \"items\": ". $data ."}";
print "{ \"items\": ".json_encode($data) ."}";

?>
