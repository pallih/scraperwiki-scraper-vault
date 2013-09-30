<?php
//original url: http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=11942
//G= id of division
//there are empty ids!
// the original is in windows-1250 !!

//corrections:
//scraperwiki::save_var('last_id',12651); //55150
//scraperwiki::sqliteexecute("update swvariables set value_blob=12651");
//scraperwiki::sqliteexecute("delete from swdata where id>12651");
//scraperwiki::sqlitecommit();
//die();

require 'scraperwiki/simple_html_dom.php'; 

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//echo $i;die();

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=" . $i;
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ((count($titles) == 0) or ($titles[0]->plaintext == '')) {
    $consecutive_empty ++;
  } else {
      $consecutive_empty = 0;
      //find date
      $h1s = $dom->find('h1');
      $h1 = str_replace('&nbsp;','',$h1s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h1,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      scraperwiki::save_var('last_i',$i);
  }
  //scraperwiki::save_var('last_i',$i);
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%a') < 180) $date_condition = true; //always continue when the division is more than 6 months old
  else $date_condition = false;
  if ($date_condition and ($consecutive_empty > 100)) { 
    $continue = false;
  }
}
?>
<?php
//original url: http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=11942
//G= id of division
//there are empty ids!
// the original is in windows-1250 !!

//corrections:
//scraperwiki::save_var('last_id',12651); //55150
//scraperwiki::sqliteexecute("update swvariables set value_blob=12651");
//scraperwiki::sqliteexecute("delete from swdata where id>12651");
//scraperwiki::sqlitecommit();
//die();

require 'scraperwiki/simple_html_dom.php'; 

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//echo $i;die();

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=" . $i;
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ((count($titles) == 0) or ($titles[0]->plaintext == '')) {
    $consecutive_empty ++;
  } else {
      $consecutive_empty = 0;
      //find date
      $h1s = $dom->find('h1');
      $h1 = str_replace('&nbsp;','',$h1s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h1,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      scraperwiki::save_var('last_i',$i);
  }
  //scraperwiki::save_var('last_i',$i);
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%a') < 180) $date_condition = true; //always continue when the division is more than 6 months old
  else $date_condition = false;
  if ($date_condition and ($consecutive_empty > 100)) { 
    $continue = false;
  }
}
?>
<?php
//original url: http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=11942
//G= id of division
//there are empty ids!
// the original is in windows-1250 !!

//corrections:
//scraperwiki::save_var('last_id',12651); //55150
//scraperwiki::sqliteexecute("update swvariables set value_blob=12651");
//scraperwiki::sqliteexecute("delete from swdata where id>12651");
//scraperwiki::sqlitecommit();
//die();

require 'scraperwiki/simple_html_dom.php'; 

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//echo $i;die();

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=" . $i;
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ((count($titles) == 0) or ($titles[0]->plaintext == '')) {
    $consecutive_empty ++;
  } else {
      $consecutive_empty = 0;
      //find date
      $h1s = $dom->find('h1');
      $h1 = str_replace('&nbsp;','',$h1s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h1,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      scraperwiki::save_var('last_i',$i);
  }
  //scraperwiki::save_var('last_i',$i);
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%a') < 180) $date_condition = true; //always continue when the division is more than 6 months old
  else $date_condition = false;
  if ($date_condition and ($consecutive_empty > 100)) { 
    $continue = false;
  }
}
?>
<?php
//original url: http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=11942
//G= id of division
//there are empty ids!
// the original is in windows-1250 !!

//corrections:
//scraperwiki::save_var('last_id',12651); //55150
//scraperwiki::sqliteexecute("update swvariables set value_blob=12651");
//scraperwiki::sqliteexecute("delete from swdata where id>12651");
//scraperwiki::sqlitecommit();
//die();

require 'scraperwiki/simple_html_dom.php'; 

//get last i
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//echo $i;die();

//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.senat.cz/xqw/xervlet/pssenat/hlasy?G=" . $i;
  $html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");
  if ((count($titles) == 0) or ($titles[0]->plaintext == '')) {
    $consecutive_empty ++;
  } else {
      $consecutive_empty = 0;
      //find date
      $h1s = $dom->find('h1');
      $h1 = str_replace('&nbsp;','',$h1s[0]->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h1,$matches);
      $last_date = new DateTime($matches[0]);
      //save it
      $out = array(
        'id' => $i,
        'html' => $html,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      scraperwiki::save_var('last_i',$i);
  }
  //scraperwiki::save_var('last_i',$i);
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%a') < 180) $date_condition = true; //always continue when the division is more than 6 months old
  else $date_condition = false;
  if ($date_condition and ($consecutive_empty > 100)) { 
    $continue = false;
  }
}
?>
