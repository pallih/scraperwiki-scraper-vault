<?php
$html = scraperWiki::scrape("http://103.6.239.114/pru13/senarai_penamaan.php?bhgn=02&selectneg=12&txtNegIndex=&txtselectedlevel=M&ddyear=2013");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div table table table tr") as $data){
    $tds = $data->find("td");
    if($tds){
        if(count($tds)==1){
            if($tds[0] != ''){
                $region = $tds[0]->plaintext;
            } else {
                $region = $region;
            }
        }
        else if(count($tds)==5){
            if($tds[2] != '&nbsp;'){
                $region = $region;
                $state = $tds[1]->plaintext;
                $calon = $tds[2]->plaintext;
                $parti = $tds[3]->plaintext;
                $record = array(
                    'region' => $region,
                    'dun' => $state,
                    'calon' => $calon,
                    'parti' => $parti, 
                );
            } else {
                $region = $region;
                $state = $state;
                $calon = $tds[2]->plaintext;
                $parti = $tds[3]->plaintext;
                $record = array(
                    'region' => $region,
                    'dun' => $state,
                    'calon' => $calon,
                    'parti' => $parti, 
                );
            }
        }
    }
    scraperwiki::save(array('calon'), $record);
}
?>
<?php
$html = scraperWiki::scrape("http://103.6.239.114/pru13/senarai_penamaan.php?bhgn=02&selectneg=12&txtNegIndex=&txtselectedlevel=M&ddyear=2013");
//print $html . "\n";
require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div table table table tr") as $data){
    $tds = $data->find("td");
    if($tds){
        if(count($tds)==1){
            if($tds[0] != ''){
                $region = $tds[0]->plaintext;
            } else {
                $region = $region;
            }
        }
        else if(count($tds)==5){
            if($tds[2] != '&nbsp;'){
                $region = $region;
                $state = $tds[1]->plaintext;
                $calon = $tds[2]->plaintext;
                $parti = $tds[3]->plaintext;
                $record = array(
                    'region' => $region,
                    'dun' => $state,
                    'calon' => $calon,
                    'parti' => $parti, 
                );
            } else {
                $region = $region;
                $state = $state;
                $calon = $tds[2]->plaintext;
                $parti = $tds[3]->plaintext;
                $record = array(
                    'region' => $region,
                    'dun' => $state,
                    'calon' => $calon,
                    'parti' => $parti, 
                );
            }
        }
    }
    scraperwiki::save(array('calon'), $record);
}
?>
