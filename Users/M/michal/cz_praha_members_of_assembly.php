<?php

//retrieves data about voting members of assembly from https://scraperwiki.com/scrapers/cz_praha_voting_records_retrieval/
//2010-2014

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_praha_voting_records_retrieval", "src");

$rows = scraperwiki::select("distinct(mp_id) from src.mp_vote");

foreach ($rows as $row) {
  $url = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/slozeni_zastupitelstva/index.html?memberId=" . $row['mp_id'];
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);

  $part = get_first_string($html,'</h2>','<div>');
  $name = trim($dom->find('h2',0)->plaintext);

  $email = get_first_string($part,'mailto:','"');
  $party = trim(get_first_string($part,'Strana:</span>','<br'));
  $club = trim(get_first_string(get_first_string($part,'Klub:</span>','</a').'::','">','::'));

  $data[] = array(
    'id' => $row['mp_id'],
    'name' => $name,
    'party' => $party,
    'club' => $club
  );

  
}
  scraperwiki::save_sqlite(array('id'),$data,'info');

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}
?>
