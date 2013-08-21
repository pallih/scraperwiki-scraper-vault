<?php


//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

//original url: http://www.psp.cz/sqw/hlasy.sqw?G=50000
//G= id of division
//there are empty ids!
//some divisions have errors - mps are printed twice (under different parties)!
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
scraperwiki::save_var('last_i',55939);
scraperwiki::sqliteexecute("delete from swdata where id>55939");//55939
scraperwiki::sqlitecommit();
//print_r($tmp);
die();

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.psp.cz/sqw/hlasy.sqw?G=" . $i;
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ($titles[0]->plaintext == 'Hlasování nenalezeno') {
    $consecutive_empty ++;
  } else {
    if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or (strpos($html,'ErrNo:') > 0) or ($titles[0]->plaintext == 'Error response') or ($html == '') or ($titles[0]->plaintext == '503 Service Temporarily Unavailable') or ($titles[0]->plaintext == 'Hlasování nenalezeno')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {
      $consecutive_empty = 0;
      //find date
      $h2s = $dom->find('h2');
      $h2 = str_replace('&nbsp;','',$h2s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h2,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    }
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 50))  {
    $continue = false;
    //scraperwiki::save_var('last_i',$i-51); //probably no new divisions so far
  }
}
?>
<?php


//2012-05-30: they changed a lot at psp.cz websites!! The scraper has been changed starting 55900 !
//it is kept for Czechoslovakia (cs_parliament_voting_records_retrieval)

//original url: http://www.psp.cz/sqw/hlasy.sqw?G=50000
//G= id of division
//there are empty ids!
//some divisions have errors - mps are printed twice (under different parties)!
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
scraperwiki::save_var('last_i',55939);
scraperwiki::sqliteexecute("delete from swdata where id>55939");//55939
scraperwiki::sqlitecommit();
//print_r($tmp);
die();

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.psp.cz/sqw/hlasy.sqw?G=" . $i;
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ($titles[0]->plaintext == 'Hlasování nenalezeno') {
    $consecutive_empty ++;
  } else {
    if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or (strpos($html,'ErrNo:') > 0) or ($titles[0]->plaintext == 'Error response') or ($html == '') or ($titles[0]->plaintext == '503 Service Temporarily Unavailable') or ($titles[0]->plaintext == 'Hlasování nenalezeno')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {
      $consecutive_empty = 0;
      //find date
      $h2s = $dom->find('h2');
      $h2 = str_replace('&nbsp;','',$h2s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h2,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    }
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 50))  {
    $continue = false;
    //scraperwiki::save_var('last_i',$i-51); //probably no new divisions so far
  }
}
?>
