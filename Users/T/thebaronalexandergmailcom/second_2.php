<?php

# Blank PHP
$html = scraperWiki::scrape("http://casesearch.courts.state.md.us/inquiry/inquiryDetail.jis?caseId=1D00292923&loc=23&detailLoc=DSCR");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div class=BodyWindow") as $data){
    $tds = $data->find("tr");
    if(count($tds)==12){
        $record = array(
            'Case Number:' => $tds[0]->plaintext, 
            'Case Type:' => intval($tds[4]->plaintext)
        );
        scraperwiki::save(array('country'), $record);

    }
}


?>
<?php

# Blank PHP
$html = scraperWiki::scrape("http://casesearch.courts.state.md.us/inquiry/inquiryDetail.jis?caseId=1D00292923&loc=23&detailLoc=DSCR");
print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div class=BodyWindow") as $data){
    $tds = $data->find("tr");
    if(count($tds)==12){
        $record = array(
            'Case Number:' => $tds[0]->plaintext, 
            'Case Type:' => intval($tds[4]->plaintext)
        );
        scraperwiki::save(array('country'), $record);

    }
}


?>
