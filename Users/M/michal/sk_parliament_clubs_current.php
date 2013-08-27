<?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about current clubs
// id of 'nezavisli' set to term_id/nezavisli (e.g. '5/nezavisli')

require 'scraperwiki/simple_html_dom.php';

//get info about current status of the tables

//current club ids 
$url = "http://www.nrsr.sk/web/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
$ids = $matches[1];

//current term
$divs = $dom->find('select[id=_sectionLayoutContainer_ctl01__currentTerm]');
$options = $divs[0]->find('option[selected=selected]');
$term = $options[0]->value;
//compare saved term
$saved_term = scraperwiki::get_var('current_term');
$info = scraperwiki::show_tables();
if ($term != $saved_term) {
  if (isset($info['club'])) {
    scraperwiki::sqliteexecute("delete from club");
    scraperwiki::sqlitecommit();
  }
  if (isset($info['membership'])) {
    scraperwiki::sqliteexecute("delete from membership");
    scraperwiki::sqlitecommit();
  }
}
scraperwiki::save_var('current_term',$term);

//current clubs
foreach ($ids as $i) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {
      //club
      if (isset($info['club'])) {
        scraperwiki::sqliteexecute("delete from club where id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $club = array(
         'id' => $i,
      );
      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
      $club['name'] = $com_name;
      //committee info
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs) > 0) {
        foreach($trs as $tr) {
          $tds = $tr->find('td');
          $club[$tds[0]->plaintext] = $tds[1]->plaintext;
        }
      }
      scraperwiki::save_sqlite(array('id'),$club,'club');

    
      //mps
      if (isset($info['membership'])) {
        scraperwiki::sqliteexecute("delete from membership where src_group_id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $divs = $dom->find('div[class=member]');
      if (count($divs > 0)) {
        foreach ($divs as $div) {
          $mp = array(
            'src_group_id' => $i,  
          );
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$div->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //name
          $names = $div->find('strong');
          $mp['name'] = $names[0]->innertext;
          //role
          $divs2 = $div->find('div[class=member_name]');
          $roles = trim(str_replace($mp['name'],'',$divs2[0]->plaintext));
          ;$mp['role'] = $roles;
          //$pos = strpos($divs2[0]->innertext,'<br />');
          //$mp['role'] = trim(substr($divs2[0]->innertext,$pos+strlen('<br />')));
          //save mp
          scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
        }
      }
  }
}


//Nezavisli = Poslanci, ktorí nie sú členmi poslaneckých klubov
$url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/nezavisli";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
//delete current data
if (isset($info['club'])) {
  scraperwiki::sqliteexecute("delete from club where id = ''");
  scraperwiki::sqlitecommit();
}
$club = array('id' => $term.'/nezavisli');
$h1s = $dom->find('h1');
$club['name'] = trim($h1s[0]->plaintext);
scraperwiki::save_sqlite(array('id'),$club,'club');
//memberships
if (isset($info['membership'])) {
  scraperwiki::sqliteexecute("delete from membership where src_group_id = ''");
  scraperwiki::sqlitecommit();
}
$divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
$as = $divs[0]->find('a');
//echo $divs[0]->outertext;
if (count($as) > 0) {
  foreach($as as $a) {
    $mp = array('src_group_id' => $term.'/nezavisli');
    preg_match('/PoslanecID=([0-9]{1,})/' ,$a->href,$matches);
    $mp['mp_id'] = $matches[1];
    $mp['name'] = $a->plaintext;
    //delete his other memebrships
    scraperwiki::sqliteexecute("delete from membership where mp_id = '".$mp['mp_id']."'");
    scraperwiki::sqlitecommit();
    scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
  }
}
?><?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about current clubs
// id of 'nezavisli' set to term_id/nezavisli (e.g. '5/nezavisli')

require 'scraperwiki/simple_html_dom.php';

//get info about current status of the tables

//current club ids 
$url = "http://www.nrsr.sk/web/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
$ids = $matches[1];

//current term
$divs = $dom->find('select[id=_sectionLayoutContainer_ctl01__currentTerm]');
$options = $divs[0]->find('option[selected=selected]');
$term = $options[0]->value;
//compare saved term
$saved_term = scraperwiki::get_var('current_term');
$info = scraperwiki::show_tables();
if ($term != $saved_term) {
  if (isset($info['club'])) {
    scraperwiki::sqliteexecute("delete from club");
    scraperwiki::sqlitecommit();
  }
  if (isset($info['membership'])) {
    scraperwiki::sqliteexecute("delete from membership");
    scraperwiki::sqlitecommit();
  }
}
scraperwiki::save_var('current_term',$term);

//current clubs
foreach ($ids as $i) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {
      //club
      if (isset($info['club'])) {
        scraperwiki::sqliteexecute("delete from club where id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $club = array(
         'id' => $i,
      );
      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
      $club['name'] = $com_name;
      //committee info
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs) > 0) {
        foreach($trs as $tr) {
          $tds = $tr->find('td');
          $club[$tds[0]->plaintext] = $tds[1]->plaintext;
        }
      }
      scraperwiki::save_sqlite(array('id'),$club,'club');

    
      //mps
      if (isset($info['membership'])) {
        scraperwiki::sqliteexecute("delete from membership where src_group_id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $divs = $dom->find('div[class=member]');
      if (count($divs > 0)) {
        foreach ($divs as $div) {
          $mp = array(
            'src_group_id' => $i,  
          );
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$div->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //name
          $names = $div->find('strong');
          $mp['name'] = $names[0]->innertext;
          //role
          $divs2 = $div->find('div[class=member_name]');
          $roles = trim(str_replace($mp['name'],'',$divs2[0]->plaintext));
          ;$mp['role'] = $roles;
          //$pos = strpos($divs2[0]->innertext,'<br />');
          //$mp['role'] = trim(substr($divs2[0]->innertext,$pos+strlen('<br />')));
          //save mp
          scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
        }
      }
  }
}


//Nezavisli = Poslanci, ktorí nie sú členmi poslaneckých klubov
$url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/nezavisli";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
//delete current data
if (isset($info['club'])) {
  scraperwiki::sqliteexecute("delete from club where id = ''");
  scraperwiki::sqlitecommit();
}
$club = array('id' => $term.'/nezavisli');
$h1s = $dom->find('h1');
$club['name'] = trim($h1s[0]->plaintext);
scraperwiki::save_sqlite(array('id'),$club,'club');
//memberships
if (isset($info['membership'])) {
  scraperwiki::sqliteexecute("delete from membership where src_group_id = ''");
  scraperwiki::sqlitecommit();
}
$divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
$as = $divs[0]->find('a');
//echo $divs[0]->outertext;
if (count($as) > 0) {
  foreach($as as $a) {
    $mp = array('src_group_id' => $term.'/nezavisli');
    preg_match('/PoslanecID=([0-9]{1,})/' ,$a->href,$matches);
    $mp['mp_id'] = $matches[1];
    $mp['name'] = $a->plaintext;
    //delete his other memebrships
    scraperwiki::sqliteexecute("delete from membership where mp_id = '".$mp['mp_id']."'");
    scraperwiki::sqlitecommit();
    scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
  }
}
?><?php

// sources: http://www.nrsr.sk/default.aspx?sid=poslanci/kluby/zoznam
// http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=32 (ID ...)
// there is a problem: current clubs are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about current clubs
// id of 'nezavisli' set to term_id/nezavisli (e.g. '5/nezavisli')

require 'scraperwiki/simple_html_dom.php';

//get info about current status of the tables

//current club ids 
$url = "http://www.nrsr.sk/web/default.aspx?sid=poslanci/kluby/zoznam";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
$ids = $matches[1];

//current term
$divs = $dom->find('select[id=_sectionLayoutContainer_ctl01__currentTerm]');
$options = $divs[0]->find('option[selected=selected]');
$term = $options[0]->value;
//compare saved term
$saved_term = scraperwiki::get_var('current_term');
$info = scraperwiki::show_tables();
if ($term != $saved_term) {
  if (isset($info['club'])) {
    scraperwiki::sqliteexecute("delete from club");
    scraperwiki::sqlitecommit();
  }
  if (isset($info['membership'])) {
    scraperwiki::sqliteexecute("delete from membership");
    scraperwiki::sqlitecommit();
  }
}
scraperwiki::save_var('current_term',$term);

//current clubs
foreach ($ids as $i) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/klub&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it a valid club (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {
      //club
      if (isset($info['club'])) {
        scraperwiki::sqliteexecute("delete from club where id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $club = array(
         'id' => $i,
      );
      //club name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
      $club['name'] = $com_name;
      //committee info
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs) > 0) {
        foreach($trs as $tr) {
          $tds = $tr->find('td');
          $club[$tds[0]->plaintext] = $tds[1]->plaintext;
        }
      }
      scraperwiki::save_sqlite(array('id'),$club,'club');

    
      //mps
      if (isset($info['membership'])) {
        scraperwiki::sqliteexecute("delete from membership where src_group_id = '{$i}'");
        scraperwiki::sqlitecommit();
      }
      $divs = $dom->find('div[class=member]');
      if (count($divs > 0)) {
        foreach ($divs as $div) {
          $mp = array(
            'src_group_id' => $i,  
          );
          //id
          preg_match('/PoslanecID=([0-9]{1,})/' ,$div->innertext,$matches);
          $mp['mp_id'] = $matches[1];
          //name
          $names = $div->find('strong');
          $mp['name'] = $names[0]->innertext;
          //role
          $divs2 = $div->find('div[class=member_name]');
          $roles = trim(str_replace($mp['name'],'',$divs2[0]->plaintext));
          ;$mp['role'] = $roles;
          //$pos = strpos($divs2[0]->innertext,'<br />');
          //$mp['role'] = trim(substr($divs2[0]->innertext,$pos+strlen('<br />')));
          //save mp
          scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
        }
      }
  }
}


//Nezavisli = Poslanci, ktorí nie sú členmi poslaneckých klubov
$url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/kluby/nezavisli";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);
//delete current data
if (isset($info['club'])) {
  scraperwiki::sqliteexecute("delete from club where id = ''");
  scraperwiki::sqlitecommit();
}
$club = array('id' => $term.'/nezavisli');
$h1s = $dom->find('h1');
$club['name'] = trim($h1s[0]->plaintext);
scraperwiki::save_sqlite(array('id'),$club,'club');
//memberships
if (isset($info['membership'])) {
  scraperwiki::sqliteexecute("delete from membership where src_group_id = ''");
  scraperwiki::sqlitecommit();
}
$divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
$as = $divs[0]->find('a');
//echo $divs[0]->outertext;
if (count($as) > 0) {
  foreach($as as $a) {
    $mp = array('src_group_id' => $term.'/nezavisli');
    preg_match('/PoslanecID=([0-9]{1,})/' ,$a->href,$matches);
    $mp['mp_id'] = $matches[1];
    $mp['name'] = $a->plaintext;
    //delete his other memebrships
    scraperwiki::sqliteexecute("delete from membership where mp_id = '".$mp['mp_id']."'");
    scraperwiki::sqlitecommit();
    scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
  }
}
?>