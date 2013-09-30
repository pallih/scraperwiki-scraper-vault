<?php

//extract data from html files about towns

//temp
/*scraperwiki::save_var('last_town_code',0);
die();*/
scraperwiki::sqliteexecute("delete from `vote` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_president_2013_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");
//echo count($rows);die();
foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
//echo $table->outertext;die();
  $trs = $table->find('tr');
  $trsc = count($trs);
  $tr = $table->find('tr',$trsc-1);
  $shift = (($trsc == 2) ? 3 : 0);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => (($trsc == 2) ? 1 : str_replace(' ','',$tds[0]->plaintext)),
    'voters_registred' => str_replace(' ','',$tds[3-$shift]->plaintext),
    'voters_attended' => str_replace(' ','',$tds[4-$shift]->plaintext),
    'turnout_percentage' => str_replace(',','.',$tds[5-$shift]->plaintext),
    'voters_voted' => str_replace(' ','',$tds[6-$shift]->plaintext),
    'voters_valid' => str_replace(' ','',$tds[7-$shift]->plaintext),
    'valid_percentage' => str_replace(' ','',str_replace(',','.',$tds[8-$shift]->plaintext)),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);
///print_r($info);die();
  $data = array();
  $tables = $dom->find('table');
  array_shift($tables);
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach party
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if (($tds[0]->plaintext != '')and($tds[0]->plaintext != '-')) {
          $item['candidate_number'] = str_replace('*','',str_replace('+','',str_replace(' ','',$tds[0]->plaintext)));
          $item['candidate'] = $tds[1]->plaintext;
          $item['votes'] = str_replace(' ','',$tds[4]->plaintext);
          $item['votes_percentage'] = str_replace(' ','',str_replace(',','.',$tds[5]->plaintext));
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','candidate_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
/*scraperwiki::save_var('last_town_code',0);
die();*/
scraperwiki::sqliteexecute("delete from `vote` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_president_2013_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");
//echo count($rows);die();
foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
//echo $table->outertext;die();
  $trs = $table->find('tr');
  $trsc = count($trs);
  $tr = $table->find('tr',$trsc-1);
  $shift = (($trsc == 2) ? 3 : 0);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => (($trsc == 2) ? 1 : str_replace(' ','',$tds[0]->plaintext)),
    'voters_registred' => str_replace(' ','',$tds[3-$shift]->plaintext),
    'voters_attended' => str_replace(' ','',$tds[4-$shift]->plaintext),
    'turnout_percentage' => str_replace(',','.',$tds[5-$shift]->plaintext),
    'voters_voted' => str_replace(' ','',$tds[6-$shift]->plaintext),
    'voters_valid' => str_replace(' ','',$tds[7-$shift]->plaintext),
    'valid_percentage' => str_replace(' ','',str_replace(',','.',$tds[8-$shift]->plaintext)),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);
///print_r($info);die();
  $data = array();
  $tables = $dom->find('table');
  array_shift($tables);
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach party
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if (($tds[0]->plaintext != '')and($tds[0]->plaintext != '-')) {
          $item['candidate_number'] = str_replace('*','',str_replace('+','',str_replace(' ','',$tds[0]->plaintext)));
          $item['candidate'] = $tds[1]->plaintext;
          $item['votes'] = str_replace(' ','',$tds[4]->plaintext);
          $item['votes_percentage'] = str_replace(' ','',str_replace(',','.',$tds[5]->plaintext));
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','candidate_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
/*scraperwiki::save_var('last_town_code',0);
die();*/
scraperwiki::sqliteexecute("delete from `vote` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_president_2013_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");
//echo count($rows);die();
foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
//echo $table->outertext;die();
  $trs = $table->find('tr');
  $trsc = count($trs);
  $tr = $table->find('tr',$trsc-1);
  $shift = (($trsc == 2) ? 3 : 0);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => (($trsc == 2) ? 1 : str_replace(' ','',$tds[0]->plaintext)),
    'voters_registred' => str_replace(' ','',$tds[3-$shift]->plaintext),
    'voters_attended' => str_replace(' ','',$tds[4-$shift]->plaintext),
    'turnout_percentage' => str_replace(',','.',$tds[5-$shift]->plaintext),
    'voters_voted' => str_replace(' ','',$tds[6-$shift]->plaintext),
    'voters_valid' => str_replace(' ','',$tds[7-$shift]->plaintext),
    'valid_percentage' => str_replace(' ','',str_replace(',','.',$tds[8-$shift]->plaintext)),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);
///print_r($info);die();
  $data = array();
  $tables = $dom->find('table');
  array_shift($tables);
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach party
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if (($tds[0]->plaintext != '')and($tds[0]->plaintext != '-')) {
          $item['candidate_number'] = str_replace('*','',str_replace('+','',str_replace(' ','',$tds[0]->plaintext)));
          $item['candidate'] = $tds[1]->plaintext;
          $item['votes'] = str_replace(' ','',$tds[4]->plaintext);
          $item['votes_percentage'] = str_replace(' ','',str_replace(',','.',$tds[5]->plaintext));
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','candidate_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
/*scraperwiki::save_var('last_town_code',0);
die();*/
scraperwiki::sqliteexecute("delete from `vote` where town_code>'599999'");
scraperwiki::sqlitecommit();
die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_president_2013_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");
//echo count($rows);die();
foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
//echo $table->outertext;die();
  $trs = $table->find('tr');
  $trsc = count($trs);
  $tr = $table->find('tr',$trsc-1);
  $shift = (($trsc == 2) ? 3 : 0);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => (($trsc == 2) ? 1 : str_replace(' ','',$tds[0]->plaintext)),
    'voters_registred' => str_replace(' ','',$tds[3-$shift]->plaintext),
    'voters_attended' => str_replace(' ','',$tds[4-$shift]->plaintext),
    'turnout_percentage' => str_replace(',','.',$tds[5-$shift]->plaintext),
    'voters_voted' => str_replace(' ','',$tds[6-$shift]->plaintext),
    'voters_valid' => str_replace(' ','',$tds[7-$shift]->plaintext),
    'valid_percentage' => str_replace(' ','',str_replace(',','.',$tds[8-$shift]->plaintext)),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);
///print_r($info);die();
  $data = array();
  $tables = $dom->find('table');
  array_shift($tables);
  foreach ($tables as $table) {
    $trs = $table->find('tr');
    array_shift($trs);
    array_shift($trs);

    //foreach party
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      
      if (($tds[0]->plaintext != '')and($tds[0]->plaintext != '-')) {
          $item['candidate_number'] = str_replace('*','',str_replace('+','',str_replace(' ','',$tds[0]->plaintext)));
          $item['candidate'] = $tds[1]->plaintext;
          $item['votes'] = str_replace(' ','',$tds[4]->plaintext);
          $item['votes_percentage'] = str_replace(' ','',str_replace(',','.',$tds[5]->plaintext));
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','candidate_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
