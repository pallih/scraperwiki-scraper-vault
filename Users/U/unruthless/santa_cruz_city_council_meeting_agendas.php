<?php

// Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://64.175.136.240/sirepub/cache/2/zgy404rmabudi4ipwfbcd355/25202252012040342743.htm");

$html = str_replace('&nbsp;',' ',$html);
while (substr_count($html,"  ") != 0) {
  $html = str_replace("  "," ",$html);
}

$dom = new simple_html_dom();
$dom->load($html);

$paragraphs = array();

foreach ($dom->find('body') as $body) {

  print($body->innertext);
/*
  if (isset($p) && !empty($p)) {
    array_push($paragraphs, $p->plaintext);
  }
*/

}

/*
print_r($paragraphs);
*/


/* foreach($dom->find("div[@align='left'] tr.tcont") as $data){
    $tds = $data->find("td");
    $record = array(
        'country' => $tds[0]->plaintext, 
        'years_in_school' => intval($tds[4]->plaintext)
    );
    print_r($record);
} */

?>
