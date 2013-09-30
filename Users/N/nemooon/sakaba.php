<?php
require 'scraperwiki/simple_html_dom.php';

//mb_internal_encoding( 'Shift_JIS' );

$html = scraperWiki::scrape("http://w3.bs-tbs.co.jp/sakaba/map/index.html");
$html = mb_convert_encoding( $html, 'UTF-8', 'Shift_JIS' );
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("a.kihon5") as $a){
    preg_match( '/\.\.\/shop\/([0-9]+)\.html/', $a->href, $maches );
    $id = $maches[1];
    $html = scraperWiki::scrape("http://w3.bs-tbs.co.jp/sakaba/shop/{$id}.html");
    $html = mb_convert_encoding( $html, 'UTF-8', 'Shift_JIS' );
    $domm = new simple_html_dom();
    $domm->load($html);
    print_r( $domm->find('住　所') );
    exit();
    scraperwiki::save( array('link'), array(
        'id' => $id,
        'link' => "http://w3.bs-tbs.co.jp/sakaba/shop/{$id}.html",
        'title' => $a->text(),
    ) );
    print $a->text() . PHP_EOL;
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';

//mb_internal_encoding( 'Shift_JIS' );

$html = scraperWiki::scrape("http://w3.bs-tbs.co.jp/sakaba/map/index.html");
$html = mb_convert_encoding( $html, 'UTF-8', 'Shift_JIS' );
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("a.kihon5") as $a){
    preg_match( '/\.\.\/shop\/([0-9]+)\.html/', $a->href, $maches );
    $id = $maches[1];
    $html = scraperWiki::scrape("http://w3.bs-tbs.co.jp/sakaba/shop/{$id}.html");
    $html = mb_convert_encoding( $html, 'UTF-8', 'Shift_JIS' );
    $domm = new simple_html_dom();
    $domm->load($html);
    print_r( $domm->find('住　所') );
    exit();
    scraperwiki::save( array('link'), array(
        'id' => $id,
        'link' => "http://w3.bs-tbs.co.jp/sakaba/shop/{$id}.html",
        'title' => $a->text(),
    ) );
    print $a->text() . PHP_EOL;
}

?>
