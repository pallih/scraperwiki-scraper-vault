<?php

$html = scraperWiki::scrape("http://www.state.il.us/lcc/owners.asp?fn=271937028");
# print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==3 && $tds[0]->plaintext != 'Owner Name'){
        foreach($tds as $k => $v){
            print '$tds[' . $k . '] = ' . $v->plaintext . "\n";
        }
        $record = array(
            'owner_name' => $tds[0]->plaintext, 
            'title' => $tds[1]->plaintext, 
            'pct_owned' => $tds[2]->plaintext
        );
        print $record;
        scraperwiki::save(array('owner_name'), $record);

    }
}

?>
<?php

$html = scraperWiki::scrape("http://www.state.il.us/lcc/owners.asp?fn=271937028");
# print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==3 && $tds[0]->plaintext != 'Owner Name'){
        foreach($tds as $k => $v){
            print '$tds[' . $k . '] = ' . $v->plaintext . "\n";
        }
        $record = array(
            'owner_name' => $tds[0]->plaintext, 
            'title' => $tds[1]->plaintext, 
            'pct_owned' => $tds[2]->plaintext
        );
        print $record;
        scraperwiki::save(array('owner_name'), $record);

    }
}

?>
