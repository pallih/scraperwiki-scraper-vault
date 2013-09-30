<?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about historical clubs
// there are no information about 'Nezarazeni'

require 'scraperwiki/simple_html_dom.php'; 

//find first _current_ club_id
$url = "http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
sort($matches[1]);
$first_current_id = $matches[1][0];

//historical clubs
for($i=1 ;$i<$first_current_id; $i++) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {

      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
    
      //mps
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs)>0) {
        foreach ($trs as $tr) {
          $mp = array();
          $tds = $tr->find('td');
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //term
          preg_match('/CisObdobia=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['term'] = $matches[1];
          //name
          $mp['name'] = $tds[0]->plaintext;
          $mp['membership'] = str_replace('&nbsp;','',$tds[1]->plaintext);
          //club id
          $mp['club_id'] = $i;
          scraperwiki::save_sqlite(array('mp_id','club_id'),$mp,'membership');
        }
      }
      //save club
      $club = array(
        'id' => $i,
        'term' => $mp['term'],
        'name' => $com_name,
      );
      scraperwiki::save_sqlite(array('id'),$club,'club');
  }
}

?>
<?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about historical clubs
// there are no information about 'Nezarazeni'

require 'scraperwiki/simple_html_dom.php'; 

//find first _current_ club_id
$url = "http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
sort($matches[1]);
$first_current_id = $matches[1][0];

//historical clubs
for($i=1 ;$i<$first_current_id; $i++) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {

      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
    
      //mps
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs)>0) {
        foreach ($trs as $tr) {
          $mp = array();
          $tds = $tr->find('td');
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //term
          preg_match('/CisObdobia=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['term'] = $matches[1];
          //name
          $mp['name'] = $tds[0]->plaintext;
          $mp['membership'] = str_replace('&nbsp;','',$tds[1]->plaintext);
          //club id
          $mp['club_id'] = $i;
          scraperwiki::save_sqlite(array('mp_id','club_id'),$mp,'membership');
        }
      }
      //save club
      $club = array(
        'id' => $i,
        'term' => $mp['term'],
        'name' => $com_name,
      );
      scraperwiki::save_sqlite(array('id'),$club,'club');
  }
}

?>
<?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about historical clubs
// there are no information about 'Nezarazeni'

require 'scraperwiki/simple_html_dom.php'; 

//find first _current_ club_id
$url = "http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
sort($matches[1]);
$first_current_id = $matches[1][0];

//historical clubs
for($i=1 ;$i<$first_current_id; $i++) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {

      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
    
      //mps
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs)>0) {
        foreach ($trs as $tr) {
          $mp = array();
          $tds = $tr->find('td');
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //term
          preg_match('/CisObdobia=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['term'] = $matches[1];
          //name
          $mp['name'] = $tds[0]->plaintext;
          $mp['membership'] = str_replace('&nbsp;','',$tds[1]->plaintext);
          //club id
          $mp['club_id'] = $i;
          scraperwiki::save_sqlite(array('mp_id','club_id'),$mp,'membership');
        }
      }
      //save club
      $club = array(
        'id' => $i,
        'term' => $mp['term'],
        'name' => $com_name,
      );
      scraperwiki::save_sqlite(array('id'),$club,'club');
  }
}

?>
<?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about historical clubs
// there are no information about 'Nezarazeni'

require 'scraperwiki/simple_html_dom.php'; 

//find first _current_ club_id
$url = "http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
sort($matches[1]);
$first_current_id = $matches[1][0];

//historical clubs
for($i=1 ;$i<$first_current_id; $i++) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {

      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
    
      //mps
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs)>0) {
        foreach ($trs as $tr) {
          $mp = array();
          $tds = $tr->find('td');
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //term
          preg_match('/CisObdobia=([0-9]{1,})/' ,$tds[0]->innertext,$matches);
          $mp['term'] = $matches[1];
          //name
          $mp['name'] = $tds[0]->plaintext;
          $mp['membership'] = str_replace('&nbsp;','',$tds[1]->plaintext);
          //club id
          $mp['club_id'] = $i;
          scraperwiki::save_sqlite(array('mp_id','club_id'),$mp,'membership');
        }
      }
      //save club
      $club = array(
        'id' => $i,
        'term' => $mp['term'],
        'name' => $com_name,
      );
      scraperwiki::save_sqlite(array('id'),$club,'club');
  }
}

?>
