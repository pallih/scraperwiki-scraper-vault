<?php

// sources: http://www.nrsr.sk/web/default.aspx?sid=vybory
// http://www.nrsr.sk/web/Default.aspx?sid=vybory/vybor&ID=96 (ID ...)
// there is a problem: current committes are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about current committees

require 'scraperwiki/simple_html_dom.php';

//get info about current status of the tables

//current committee_ids
$url = "http://www.nrsr.sk/web/default.aspx?sid=vybory";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
$ids = $matches[1];

//current term
$div = $dom->find('select[id=_sectionLayoutContainer_ctl01__currentTerm]',0);
$option = $div->find('option[selected=selected]',0);
$term = $option->value;
//compare saved term
$saved_term = scraperwiki::get_var('current_term');
if ($term != $saved_term) {
  $info = scraperwiki::show_tables();
  if (isset($info['committee'])) {
    scraperwiki::sqliteexecute("delete from committee");
    scraperwiki::sqlitecommit();
  }
  if (isset($info['membership'])) {
    scraperwiki::sqliteexecute("delete from membership");
    scraperwiki::sqlitecommit();
  }
}
scraperwiki::save_var('current_term',$term);

//current committees
foreach ($ids as $i) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=vybory/vybor&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid committee (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {
      //committee
      if (isset($info['committee'])) {
        scraperwiki::sqliteexecute("delete from committee where id = '{$i}'"); //**disable for the first run
        scraperwiki::sqlitecommit(); //**disable for the first run
      }
      $committee = array(
         'id' => $i,
      );
      //committee name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
      $committee['name'] = $com_name;
      //committee info
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs) > 0) {
        foreach($trs as $tr) {
          $tds = $tr->find('td');
          $committee[$tds[0]->plaintext] = $tds[1]->plaintext;
        }
      }
      scraperwiki::save_sqlite(array('id'),$committee,'committee');

    
      //mps
      if (isset($info['membership'])) {
        scraperwiki::sqliteexecute("delete from membership where src_group_id = '{$i}'"); //**disable for the first run
        scraperwiki::sqlitecommit(); //**disable for the first run
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
          $clubs = $divs2[0]->find('em');
          $mp['club'] = trim($clubs[0]->innertext,'()');
          $roles = $divs2[0]->find('span');
          $mp['role'] = $roles[0]->innertext;
          //$pos = strpos($divs2[0]->innertext,'<br />');
          //$mp['role'] = trim(substr($divs2[0]->innertext,$pos+strlen('<br />')));
          //save mp
          scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
        }
      }
  }
}



?><?php

// sources: http://www.nrsr.sk/web/default.aspx?sid=vybory
// http://www.nrsr.sk/web/Default.aspx?sid=vybory/vybor&ID=96 (ID ...)
// there is a problem: current committes are different from historical ones (the current ones have different format and do not have 'since', 'until')
// info only about current committees

require 'scraperwiki/simple_html_dom.php';

//get info about current status of the tables

//current committee_ids
$url = "http://www.nrsr.sk/web/default.aspx?sid=vybory";
$html = scraperwiki::scrape($url);
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$uls = $dom->find('ul[class=longlist]');
preg_match_all('/ID=([0-9]{1,})/' ,$uls[0],$matches);
$ids = $matches[1];

//current term
$div = $dom->find('select[id=_sectionLayoutContainer_ctl01__currentTerm]',0);
$option = $div->find('option[selected=selected]',0);
$term = $option->value;
//compare saved term
$saved_term = scraperwiki::get_var('current_term');
if ($term != $saved_term) {
  $info = scraperwiki::show_tables();
  if (isset($info['committee'])) {
    scraperwiki::sqliteexecute("delete from committee");
    scraperwiki::sqlitecommit();
  }
  if (isset($info['membership'])) {
    scraperwiki::sqliteexecute("delete from membership");
    scraperwiki::sqlitecommit();
  }
}
scraperwiki::save_var('current_term',$term);

//current committees
foreach ($ids as $i) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=vybory/vybor&ID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it a valid committee (or empty)
  $h2s = $dom->find("h2");
  if (trim($h2s[0]->plaintext) == 'Neočakávaná chyba!') {
  } else {
      //committee
      if (isset($info['committee'])) {
        scraperwiki::sqliteexecute("delete from committee where id = '{$i}'"); //**disable for the first run
        scraperwiki::sqlitecommit(); //**disable for the first run
      }
      $committee = array(
         'id' => $i,
      );
      //committee name
      $h1s = $dom->find('h1');
      $com_name = trim($h1s[0]->plaintext);
      $committee['name'] = $com_name;
      //committee info
      $tables = $dom->find('table[class=tab_details]');
      $trs = $tables[0]->find('tr');
      if (count($trs) > 0) {
        foreach($trs as $tr) {
          $tds = $tr->find('td');
          $committee[$tds[0]->plaintext] = $tds[1]->plaintext;
        }
      }
      scraperwiki::save_sqlite(array('id'),$committee,'committee');

    
      //mps
      if (isset($info['membership'])) {
        scraperwiki::sqliteexecute("delete from membership where src_group_id = '{$i}'"); //**disable for the first run
        scraperwiki::sqlitecommit(); //**disable for the first run
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
          $clubs = $divs2[0]->find('em');
          $mp['club'] = trim($clubs[0]->innertext,'()');
          $roles = $divs2[0]->find('span');
          $mp['role'] = $roles[0]->innertext;
          //$pos = strpos($divs2[0]->innertext,'<br />');
          //$mp['role'] = trim(substr($divs2[0]->innertext,$pos+strlen('<br />')));
          //save mp
          scraperwiki::save_sqlite(array('mp_id','src_group_id'),$mp,'membership');
        }
      }
  }
}



?>