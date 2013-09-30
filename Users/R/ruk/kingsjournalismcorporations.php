<?php
require 'scraperwiki/simple_html_dom.php';

for ($regnumber = 1 ; $regnumber <= 20000 ; $regnumber++) {
    $html = scraperWiki::scrape("http://immigrate.kingsjournalism.com/?page_id=71&bRegNumber=" . $regnumber);
    $dom = new simple_html_dom();
    $dom->load($html);
    $cells = $dom->find('table tr td[colspan="4"]');
    if ($cells[0]) {
        if ($cells[0]->plaintext <> '') {
            $record = array('name' => html_entity_decode($cells[0]->plaintext),
                    'regnumber' => $cells[1]->plaintext,
                    'regdate' => $cells[2]->plaintext,
                    'status' => $cells[3]->plaintext,
                    'lastreturn' => $cells[4]->plaintext,
                    'businessin' => html_entity_decode($cells[5]->plaintext),
                    'address' => html_entity_decode($cells[6]->plaintext));
    
            scraperwiki::save(array('regnumber'), $record);
        }
    }
}




<?php
require 'scraperwiki/simple_html_dom.php';

for ($regnumber = 1 ; $regnumber <= 20000 ; $regnumber++) {
    $html = scraperWiki::scrape("http://immigrate.kingsjournalism.com/?page_id=71&bRegNumber=" . $regnumber);
    $dom = new simple_html_dom();
    $dom->load($html);
    $cells = $dom->find('table tr td[colspan="4"]');
    if ($cells[0]) {
        if ($cells[0]->plaintext <> '') {
            $record = array('name' => html_entity_decode($cells[0]->plaintext),
                    'regnumber' => $cells[1]->plaintext,
                    'regdate' => $cells[2]->plaintext,
                    'status' => $cells[3]->plaintext,
                    'lastreturn' => $cells[4]->plaintext,
                    'businessin' => html_entity_decode($cells[5]->plaintext),
                    'address' => html_entity_decode($cells[6]->plaintext));
    
            scraperwiki::save(array('regnumber'), $record);
        }
    }
}




