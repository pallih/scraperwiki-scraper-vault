<?php

# Blank PHP
# print "I started to run";

$city_param="HKI";

$html = scraperWiki::scrape("http://ext-service.vr.fi/juku/asema.action?lang=fi&junalaji=ll&asema=".$city_param);

# print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
           
$dom = new simple_html_dom();
$dom->load($html);

$depature_dom = $dom->find("table.kulkutiedot",0);
$arrival_dom  = $dom->find("table.kulkutiedot",1);
#print $arrival_dom;

$onnistuiko = date_default_timezone_set('Europe/Helsinki');
#print $onnistuiko."\n";

$current_day = date("dmy");
#print $current_day;

foreach($arrival_dom->find("tr[class!=table_header]") as $data){
   #print "luupissa \n";
    
    $tds = $data->find("td");
    

        
    $record = array(
            'id' => $tds[0]->plaintext . $current_day . $tds[1]->plaintext,
            'juna' => $tds[0]->plaintext,
            'aikataulu' => $tds[1]->plaintext,
            'saapui' => $tds[2]->plaintext,
            'arvioitu' => $tds[3]->plaintext,
            'lahtoasema' => $tds[4]->plaintext,
            'huomautus' => $tds[5]->plaintext
    );
    
    #$id = $record['juna'].$current_day.$record['aikataulu'];
    
    scraperwiki::save(array('id'), $record);
    #scraperwiki::save('id', $record);
    #print json_encode($record) . "\n";

}

?>
