<?php

require 'scraperwiki/simple_html_dom.php';
$base = 'http://www.reviersport.de';
$html = scraperWiki::scrape($base . '/fussball/landesligawestfalen3-spieltag.html');
$dom = new simple_html_dom();
$dom->load($html);
$dom = $dom->find('table', 1);

$i = 0;

foreach($dom->find("tr") as $data){
  
  // Skip first $dom->find("tr"), because it contains the table's headers
  if ($i>0) {
    
    // remove the trailing dot from Platz and add 0 before the number if it is <10
    // Don't know why I did this :D
    $platz = substr($data->find('td', 1)->innertext,0,-1);
    $platz_laenge = strlen($platz);
    if ($platz_laenge<2){
      $platz = "0".$platz;
    }
    
    // Get the url to the club's detail page
    $link = $data->find('td', 2);
    $link = $link->find('a', 0);
    if($link->href){
      $link = $link->href;
    }
    
    // Get the club's detail page
    $html = scraperWiki::scrape($base . $link);
    $dom_logo = new simple_html_dom();
    $dom_logo->load($html);
    
    // Get the url to the club's logo from it's detail page
    foreach($dom_logo->find('h2') as $h2){
      if ($h2->next_sibling()->next_sibling()->next_sibling()->children(1)->children(0)->src){
        $logo = $base . $h2->next_sibling()->next_sibling()->next_sibling()->children(1)->children(0)->src;
      }
    }
    
    // Prepare the record for the database
    $record = array(
      'Platz' => $platz,
      'Mannschaft' => $data->find('td', 2)->plaintext,
      'Spiele' => $data->find('td', 3)->innertext,
      'gewonnen' => $data->find('td', 4)->innertext,
      'unentschieden' => $data->find('td', 5)->innertext,
      'verloren' => $data->find('td', 6)->innertext,
      'Tore_1' => $data->find('td', 7)->innertext,
      'Tore_2' => $data->find('td', 9)->innertext,
      'Tordifferenz' => $data->find('td', 10)->innertext,
      'Punkte' => $data->find('td', 11)->innertext,
      'Logo' => $logo,
    );
    // clear $logo, because some clubs don't have one
    $logo = '';
    
    // save $record, use Platz as unique key
    scraperwiki::save_sqlite(array('Platz'), $record);
  }
  $i++;
}
?>