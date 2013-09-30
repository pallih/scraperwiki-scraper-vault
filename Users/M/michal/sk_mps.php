<?php

//SK MPs' details
//memberships are only current!

require 'scraperwiki/simple_html_dom.php';

//saved vars
$last_term = scraperwiki::get_var('last_term',0);
$last_id = scraperwiki::get_var('last_id',1);

//temp
//$last_term = 4;
//$last_id = 10000;

//get ids
//** may be changed for ids from voting records, because the current term does not have all MPs (just the current, too)
scraperwiki::attach("sk_mps_list", "src");
$rows = scraperwiki::select("* from src.swdata where term>{$last_term} order by term,id");

foreach ($rows as $row) {
  //
  if (($row['term'] == $last_term) and ($row['id'] < $last_id)) continue;

  //get page
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/poslanec&PoslanecID={$row['id']}&CisObdobia={$row['term']}";
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load(str_replace('&nbsp;',' ',$html));

  //personal data
  $data = array(
        'id' => $row['id'],
        'term' => $row['term'],
  );
  $divs = $dom->find('div[class=mp_personal_data]');
  $parts = $divs[0]->find('div');
  foreach ($parts as $part) {
    $labels = $part->find('strong');
    $spans = $part->find('span');
    $data[trim($labels[0]->plaintext)] = trim($spans[0]->plaintext);
  } 
  scraperwiki::save_sqlite(array('id','term'),$data,'mp');

  //memberships
  $mdata = array();
  $divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
  $uls = $divs[0]->find('ul');
  $lis = $uls[0]->find('li');
  if (count($lis) > 0) {
    foreach($lis as $li) {
      $mdata[] = array(
        'id' => $row['id'],
        'term' => $row['term'],
        'group' => trim($li->plaintext),
      );
    }
    scraperwiki::save_sqlite(array('id','term','group'),$mdata,'membership');
  }
  
 
  //save vars
  scraperwiki::save_var('last_term',$row['term']);
  scraperwiki::save_var('last_id',$row['id']);  

}
//save vars
scraperwiki::save_var('last_term',0);
scraperwiki::save_var('last_id',1);



?><?php

//SK MPs' details
//memberships are only current!

require 'scraperwiki/simple_html_dom.php';

//saved vars
$last_term = scraperwiki::get_var('last_term',0);
$last_id = scraperwiki::get_var('last_id',1);

//temp
//$last_term = 4;
//$last_id = 10000;

//get ids
//** may be changed for ids from voting records, because the current term does not have all MPs (just the current, too)
scraperwiki::attach("sk_mps_list", "src");
$rows = scraperwiki::select("* from src.swdata where term>{$last_term} order by term,id");

foreach ($rows as $row) {
  //
  if (($row['term'] == $last_term) and ($row['id'] < $last_id)) continue;

  //get page
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/poslanec&PoslanecID={$row['id']}&CisObdobia={$row['term']}";
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load(str_replace('&nbsp;',' ',$html));

  //personal data
  $data = array(
        'id' => $row['id'],
        'term' => $row['term'],
  );
  $divs = $dom->find('div[class=mp_personal_data]');
  $parts = $divs[0]->find('div');
  foreach ($parts as $part) {
    $labels = $part->find('strong');
    $spans = $part->find('span');
    $data[trim($labels[0]->plaintext)] = trim($spans[0]->plaintext);
  } 
  scraperwiki::save_sqlite(array('id','term'),$data,'mp');

  //memberships
  $mdata = array();
  $divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
  $uls = $divs[0]->find('ul');
  $lis = $uls[0]->find('li');
  if (count($lis) > 0) {
    foreach($lis as $li) {
      $mdata[] = array(
        'id' => $row['id'],
        'term' => $row['term'],
        'group' => trim($li->plaintext),
      );
    }
    scraperwiki::save_sqlite(array('id','term','group'),$mdata,'membership');
  }
  
 
  //save vars
  scraperwiki::save_var('last_term',$row['term']);
  scraperwiki::save_var('last_id',$row['id']);  

}
//save vars
scraperwiki::save_var('last_term',0);
scraperwiki::save_var('last_id',1);



?><?php

//SK MPs' details
//memberships are only current!

require 'scraperwiki/simple_html_dom.php';

//saved vars
$last_term = scraperwiki::get_var('last_term',0);
$last_id = scraperwiki::get_var('last_id',1);

//temp
//$last_term = 4;
//$last_id = 10000;

//get ids
//** may be changed for ids from voting records, because the current term does not have all MPs (just the current, too)
scraperwiki::attach("sk_mps_list", "src");
$rows = scraperwiki::select("* from src.swdata where term>{$last_term} order by term,id");

foreach ($rows as $row) {
  //
  if (($row['term'] == $last_term) and ($row['id'] < $last_id)) continue;

  //get page
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/poslanec&PoslanecID={$row['id']}&CisObdobia={$row['term']}";
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load(str_replace('&nbsp;',' ',$html));

  //personal data
  $data = array(
        'id' => $row['id'],
        'term' => $row['term'],
  );
  $divs = $dom->find('div[class=mp_personal_data]');
  $parts = $divs[0]->find('div');
  foreach ($parts as $part) {
    $labels = $part->find('strong');
    $spans = $part->find('span');
    $data[trim($labels[0]->plaintext)] = trim($spans[0]->plaintext);
  } 
  scraperwiki::save_sqlite(array('id','term'),$data,'mp');

  //memberships
  $mdata = array();
  $divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
  $uls = $divs[0]->find('ul');
  $lis = $uls[0]->find('li');
  if (count($lis) > 0) {
    foreach($lis as $li) {
      $mdata[] = array(
        'id' => $row['id'],
        'term' => $row['term'],
        'group' => trim($li->plaintext),
      );
    }
    scraperwiki::save_sqlite(array('id','term','group'),$mdata,'membership');
  }
  
 
  //save vars
  scraperwiki::save_var('last_term',$row['term']);
  scraperwiki::save_var('last_id',$row['id']);  

}
//save vars
scraperwiki::save_var('last_term',0);
scraperwiki::save_var('last_id',1);



?><?php

//SK MPs' details
//memberships are only current!

require 'scraperwiki/simple_html_dom.php';

//saved vars
$last_term = scraperwiki::get_var('last_term',0);
$last_id = scraperwiki::get_var('last_id',1);

//temp
//$last_term = 4;
//$last_id = 10000;

//get ids
//** may be changed for ids from voting records, because the current term does not have all MPs (just the current, too)
scraperwiki::attach("sk_mps_list", "src");
$rows = scraperwiki::select("* from src.swdata where term>{$last_term} order by term,id");

foreach ($rows as $row) {
  //
  if (($row['term'] == $last_term) and ($row['id'] < $last_id)) continue;

  //get page
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/poslanec&PoslanecID={$row['id']}&CisObdobia={$row['term']}";
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load(str_replace('&nbsp;',' ',$html));

  //personal data
  $data = array(
        'id' => $row['id'],
        'term' => $row['term'],
  );
  $divs = $dom->find('div[class=mp_personal_data]');
  $parts = $divs[0]->find('div');
  foreach ($parts as $part) {
    $labels = $part->find('strong');
    $spans = $part->find('span');
    $data[trim($labels[0]->plaintext)] = trim($spans[0]->plaintext);
  } 
  scraperwiki::save_sqlite(array('id','term'),$data,'mp');

  //memberships
  $mdata = array();
  $divs = $dom->find('div[id=_sectionLayoutContainer__panelContent]');
  $uls = $divs[0]->find('ul');
  $lis = $uls[0]->find('li');
  if (count($lis) > 0) {
    foreach($lis as $li) {
      $mdata[] = array(
        'id' => $row['id'],
        'term' => $row['term'],
        'group' => trim($li->plaintext),
      );
    }
    scraperwiki::save_sqlite(array('id','term','group'),$mdata,'membership');
  }
  
 
  //save vars
  scraperwiki::save_var('last_term',$row['term']);
  scraperwiki::save_var('last_id',$row['id']);  

}
//save vars
scraperwiki::save_var('last_term',0);
scraperwiki::save_var('last_id',1);



?>