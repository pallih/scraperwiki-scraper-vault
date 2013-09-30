<?php
// SCRAPING DEPOZYTY ZŁOTOWE - WIBID, WIBOR
require 'scraperwiki/simple_html_dom.php';           

$wikis = "https://scraperwiki.com/";
$money = 'http://www.money.pl/pieniadze/depozyty/zlotowe/';
$html = scraperWiki::scrape($money);

$dom = new simple_html_dom();
$dom->load($html);

// get WIBRO
$wibor_data = $wibid_data = array();
foreach($dom->find('table', 0)->find('tbody tr') as $id => $tr) {
    if($id==0) {
        continue;
    }

    $termin = $tr->find('a.link', 0)->innertext;
    if(!empty($termin)) {
        $wibor_data[] = array(
            'id' => $id,
            'termin' =>     trim($termin),
            'WIBOR' =>      trim($tr->find('td',1)->innertext),
            'change' =>     trim($tr->find('td span', 0)->innertext),
            'change3M' =>   trim($tr->find('td span', 1)->innertext),
            'change12M' =>  trim($tr->find('td span', 2)->innertext),
            'date' =>       trim($tr->find('td', 5)->innertext)
        );
    }

}
scraperwiki::save_sqlite(array('id'), $wibor_data, 'wibor');


// get WIBID
foreach($dom->find('table', 1)->find('tbody tr') as $id => $tr) {
    if($id==0) {
        continue;
    }

    $termin = $tr->find('a.link', 0)->innertext;
    if(!empty($termin)) {
        $wibid_data[] = array(
            'id' => $id,
            'termin' =>     trim($termin),
            'WIBID' =>      trim($tr->find('td',1)->innertext),
            'change' =>     trim($tr->find('td span', 0)->innertext),
            'change3M' =>   trim($tr->find('td span', 1)->innertext),
            'change12M' =>  trim($tr->find('td span', 2)->innertext),
            'date' =>       trim($tr->find('td', 5)->innertext)
        );
    }

}
scraperwiki::save_sqlite(array('id'), $wibid_data, 'wibid');


?>
<?php
// SCRAPING DEPOZYTY ZŁOTOWE - WIBID, WIBOR
require 'scraperwiki/simple_html_dom.php';           

$wikis = "https://scraperwiki.com/";
$money = 'http://www.money.pl/pieniadze/depozyty/zlotowe/';
$html = scraperWiki::scrape($money);

$dom = new simple_html_dom();
$dom->load($html);

// get WIBRO
$wibor_data = $wibid_data = array();
foreach($dom->find('table', 0)->find('tbody tr') as $id => $tr) {
    if($id==0) {
        continue;
    }

    $termin = $tr->find('a.link', 0)->innertext;
    if(!empty($termin)) {
        $wibor_data[] = array(
            'id' => $id,
            'termin' =>     trim($termin),
            'WIBOR' =>      trim($tr->find('td',1)->innertext),
            'change' =>     trim($tr->find('td span', 0)->innertext),
            'change3M' =>   trim($tr->find('td span', 1)->innertext),
            'change12M' =>  trim($tr->find('td span', 2)->innertext),
            'date' =>       trim($tr->find('td', 5)->innertext)
        );
    }

}
scraperwiki::save_sqlite(array('id'), $wibor_data, 'wibor');


// get WIBID
foreach($dom->find('table', 1)->find('tbody tr') as $id => $tr) {
    if($id==0) {
        continue;
    }

    $termin = $tr->find('a.link', 0)->innertext;
    if(!empty($termin)) {
        $wibid_data[] = array(
            'id' => $id,
            'termin' =>     trim($termin),
            'WIBID' =>      trim($tr->find('td',1)->innertext),
            'change' =>     trim($tr->find('td span', 0)->innertext),
            'change3M' =>   trim($tr->find('td span', 1)->innertext),
            'change12M' =>  trim($tr->find('td span', 2)->innertext),
            'date' =>       trim($tr->find('td', 5)->innertext)
        );
    }

}
scraperwiki::save_sqlite(array('id'), $wibid_data, 'wibid');


?>
