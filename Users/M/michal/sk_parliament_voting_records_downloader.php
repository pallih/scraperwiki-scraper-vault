<?php
//original url: http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=1000
//there are empty ids!


require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
//scraperwiki::save_var('last_i',19106);
//scraperwiki::sqliteexecute("delete from swdata where id>56000");
//scraperwiki::sqlitecommit();
//print_r($tmp);
//die();

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
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
    $consecutive_empty ++;
  } else {
    /*if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or ($titles[0]->plaintext == 'Error response')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {*/
      $consecutive_empty = 0;

      //extract useful html
      $part1 = $dom->find('div[class=voting_stats_summary_panel]');
      $part2 = $dom->find('div[id=_sectionLayoutContainer_ctl00_ctl00__resultsTablePanel]');
      $part3 = $dom->find('table[id=_sectionLayoutContainer_ctl00__resultsTable]');
      $text = $part1[0]->outertext . "\n" . $part2[0]->outertext . "\n" . $part3[0]->outertext;

      //find date
      $divs = $part1[0]->find('div[class=grid_4]');
      $dates = $divs[1]->find('span');
      $date = str_replace('&nbsp;','',str_replace('. ','.',$dates[0]->plaintext));
      $last_date = new DateTime($date);
      //save it
      $out = array(
        'id' => $i,
        'html' => $text,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    //}
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 150))  {
    $continue = false;
  }
}
?>
<?php
//original url: http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=1000
//there are empty ids!


require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
//scraperwiki::save_var('last_i',19106);
//scraperwiki::sqliteexecute("delete from swdata where id>56000");
//scraperwiki::sqlitecommit();
//print_r($tmp);
//die();

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
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
    $consecutive_empty ++;
  } else {
    /*if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or ($titles[0]->plaintext == 'Error response')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {*/
      $consecutive_empty = 0;

      //extract useful html
      $part1 = $dom->find('div[class=voting_stats_summary_panel]');
      $part2 = $dom->find('div[id=_sectionLayoutContainer_ctl00_ctl00__resultsTablePanel]');
      $part3 = $dom->find('table[id=_sectionLayoutContainer_ctl00__resultsTable]');
      $text = $part1[0]->outertext . "\n" . $part2[0]->outertext . "\n" . $part3[0]->outertext;

      //find date
      $divs = $part1[0]->find('div[class=grid_4]');
      $dates = $divs[1]->find('span');
      $date = str_replace('&nbsp;','',str_replace('. ','.',$dates[0]->plaintext));
      $last_date = new DateTime($date);
      //save it
      $out = array(
        'id' => $i,
        'html' => $text,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    //}
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 150))  {
    $continue = false;
  }
}
?>
<?php
//original url: http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=1000
//there are empty ids!


require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
//scraperwiki::save_var('last_i',19106);
//scraperwiki::sqliteexecute("delete from swdata where id>56000");
//scraperwiki::sqlitecommit();
//print_r($tmp);
//die();

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
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
    $consecutive_empty ++;
  } else {
    /*if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or ($titles[0]->plaintext == 'Error response')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {*/
      $consecutive_empty = 0;

      //extract useful html
      $part1 = $dom->find('div[class=voting_stats_summary_panel]');
      $part2 = $dom->find('div[id=_sectionLayoutContainer_ctl00_ctl00__resultsTablePanel]');
      $part3 = $dom->find('table[id=_sectionLayoutContainer_ctl00__resultsTable]');
      $text = $part1[0]->outertext . "\n" . $part2[0]->outertext . "\n" . $part3[0]->outertext;

      //find date
      $divs = $part1[0]->find('div[class=grid_4]');
      $dates = $divs[1]->find('span');
      $date = str_replace('&nbsp;','',str_replace('. ','.',$dates[0]->plaintext));
      $last_date = new DateTime($date);
      //save it
      $out = array(
        'id' => $i,
        'html' => $text,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    //}
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 150))  {
    $continue = false;
  }
}
?>
<?php
//original url: http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=1000
//there are empty ids!


require 'scraperwiki/simple_html_dom.php'; 

//corrections "by hand":
//scraperwiki::save_var('last_i',54535);
//scraperwiki::save_var('last_i',19106);
//scraperwiki::sqliteexecute("delete from swdata where id>56000");
//scraperwiki::sqlitecommit();
//print_r($tmp);
//die();

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
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
    $consecutive_empty ++;
  } else {
    /*if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or ($titles[0]->plaintext == 'Error response')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_i',$last_ok_i);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {*/
      $consecutive_empty = 0;

      //extract useful html
      $part1 = $dom->find('div[class=voting_stats_summary_panel]');
      $part2 = $dom->find('div[id=_sectionLayoutContainer_ctl00_ctl00__resultsTablePanel]');
      $part3 = $dom->find('table[id=_sectionLayoutContainer_ctl00__resultsTable]');
      $text = $part1[0]->outertext . "\n" . $part2[0]->outertext . "\n" . $part3[0]->outertext;

      //find date
      $divs = $part1[0]->find('div[class=grid_4]');
      $dates = $divs[1]->find('span');
      $date = str_replace('&nbsp;','',str_replace('. ','.',$dates[0]->plaintext));
      $last_date = new DateTime($date);
      //save it
      $out = array(
        'id' => $i,
        'html' => $text,
      );
      scraperwiki::save_sqlite(array('id'),$out);
      $last_ok_i = $i;
      scraperwiki::save_var('last_i',$i);
    //}
  }  
  $i++;
  //continue?
  $interval = $last_date->diff($now); 
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 150))  {
    $continue = false;
  }
}
?>
