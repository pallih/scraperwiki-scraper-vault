<?php

$html = scraperWiki::scrape("https://rakendused.vm.ee/akta/andmed_vaata.php?id=2063");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$dom->load($html);
$temprecord=array();


foreach($dom->find("div tr") as $data){ 
    $tds = $data->find("td"); 
    $counter==0;
    if(count($tds)==2){ 
        $temprecord[$counter]=$tds[1]->plaintext; 
        if($counter<6 && $counter>2) {
        $temprecord[$counter]=$tds[0]->plaintext.'-'.$tds[1]->plaintext;
    }
    $counter++;
print json_encode($temprecord) . "\n"; } }


$record = array("reg"=>$temprecord[0], "year"=>$temprecord[1], "tegevusvaldkond_1"=>$temprecord[3], 
                "tegevusvaldkond_2"=>$temprecord[4], "tegevusvaldkond_3"=>$temprecord[5],
                "donor"=>$temprecord[6], "donors_contact"=>$temprecord[7],
                "implementor_group"=>$temprecord[8], "implementor"=>$temprecord[9], 
                "activity_statium"=>$temprecord[10], "aid_recipient"=>$temprecord[11],
                "riikide_grupid"=>$temprecord[12], "organisation"=>$temprecord[13], 
                "organisatsioonide_grupid"=>$temprecord[14], "percent"=>$temprecord[15],
                "toetuse_summa"=>$temprecord[16], "aid_sum"=>$temprecord[17], "teema"=>$temprecord[18], 
                "project_name"=>$temprecord[19], "description"=>$temprecord[20], 
                "co-financier"=>$temprecord[21], "type_of_aid"=>$temprecord[22], 
                "project_duration"=>$temprecord[23],
                "project_data"=>$temprecord[24], "project_file"=>$temprecord[25]);

scraperwiki::save(array('year'), $record);




?>
<?php

$html = scraperWiki::scrape("https://rakendused.vm.ee/akta/andmed_vaata.php?id=2063");
//print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$dom->load($html);
$temprecord=array();


foreach($dom->find("div tr") as $data){ 
    $tds = $data->find("td"); 
    $counter==0;
    if(count($tds)==2){ 
        $temprecord[$counter]=$tds[1]->plaintext; 
        if($counter<6 && $counter>2) {
        $temprecord[$counter]=$tds[0]->plaintext.'-'.$tds[1]->plaintext;
    }
    $counter++;
print json_encode($temprecord) . "\n"; } }


$record = array("reg"=>$temprecord[0], "year"=>$temprecord[1], "tegevusvaldkond_1"=>$temprecord[3], 
                "tegevusvaldkond_2"=>$temprecord[4], "tegevusvaldkond_3"=>$temprecord[5],
                "donor"=>$temprecord[6], "donors_contact"=>$temprecord[7],
                "implementor_group"=>$temprecord[8], "implementor"=>$temprecord[9], 
                "activity_statium"=>$temprecord[10], "aid_recipient"=>$temprecord[11],
                "riikide_grupid"=>$temprecord[12], "organisation"=>$temprecord[13], 
                "organisatsioonide_grupid"=>$temprecord[14], "percent"=>$temprecord[15],
                "toetuse_summa"=>$temprecord[16], "aid_sum"=>$temprecord[17], "teema"=>$temprecord[18], 
                "project_name"=>$temprecord[19], "description"=>$temprecord[20], 
                "co-financier"=>$temprecord[21], "type_of_aid"=>$temprecord[22], 
                "project_duration"=>$temprecord[23],
                "project_data"=>$temprecord[24], "project_file"=>$temprecord[25]);

scraperwiki::save(array('year'), $record);




?>
