<?php

//extract data from html files about towns

//temp
//scraperwiki::save_var('last_town_code',0);
//die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_parliament_2010_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
  $tr = $table->find('tr',2);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => $tds[0]->plaintext,
    'voters_registred' => $tds[3]->plaintext,
    'voters_attended' => $tds[4]->plaintext,
    'turnout_percentage' => str_replace(',','.',$tds[5]->plaintext),
    'voters_voted' => $tds[6]->plaintext,
    'voters_valid' => $tds[7]->plaintext,
    'valid_percentage' => str_replace(',','.',$tds[8]->plaintext),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);

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
          $item['party_number'] = $tds[0]->plaintext;
          $item['party'] = $tds[1]->plaintext;
          $item['votes'] = $tds[2]->plaintext;
          $item['votes_percentage'] = str_replace(',','.',$tds[3]->plaintext);
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','party_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
//scraperwiki::save_var('last_town_code',0);
//die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_parliament_2010_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
  $tr = $table->find('tr',2);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => $tds[0]->plaintext,
    'voters_registred' => $tds[3]->plaintext,
    'voters_attended' => $tds[4]->plaintext,
    'turnout_percentage' => str_replace(',','.',$tds[5]->plaintext),
    'voters_voted' => $tds[6]->plaintext,
    'voters_valid' => $tds[7]->plaintext,
    'valid_percentage' => str_replace(',','.',$tds[8]->plaintext),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);

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
          $item['party_number'] = $tds[0]->plaintext;
          $item['party'] = $tds[1]->plaintext;
          $item['votes'] = $tds[2]->plaintext;
          $item['votes_percentage'] = str_replace(',','.',$tds[3]->plaintext);
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','party_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
//scraperwiki::save_var('last_town_code',0);
//die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_parliament_2010_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
  $tr = $table->find('tr',2);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => $tds[0]->plaintext,
    'voters_registred' => $tds[3]->plaintext,
    'voters_attended' => $tds[4]->plaintext,
    'turnout_percentage' => str_replace(',','.',$tds[5]->plaintext),
    'voters_voted' => $tds[6]->plaintext,
    'voters_valid' => $tds[7]->plaintext,
    'valid_percentage' => str_replace(',','.',$tds[8]->plaintext),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);

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
          $item['party_number'] = $tds[0]->plaintext;
          $item['party'] = $tds[1]->plaintext;
          $item['votes'] = $tds[2]->plaintext;
          $item['votes_percentage'] = str_replace(',','.',$tds[3]->plaintext);
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','party_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
<?php

//extract data from html files about towns

//temp
//scraperwiki::save_var('last_town_code',0);
//die();

require 'scraperwiki/simple_html_dom.php';

$last_town_code = scraperwiki::get_var('last_town_code',0);

scraperwiki::attach("cz_volbycz_parliament_2010_2_downloader", "src");
$rows = scraperwiki::select("* from src.swdata where town_code>'{$last_town_code}' order by town_code");

foreach ($rows as $row) {
  $html = $row['html'];
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $table = $dom->find('table',0);
  $tr = $table->find('tr',2);
  $tds = $tr->find('td');
  $info = array(
    'okrsky' => $tds[0]->plaintext,
    'voters_registred' => $tds[3]->plaintext,
    'voters_attended' => $tds[4]->plaintext,
    'turnout_percentage' => str_replace(',','.',$tds[5]->plaintext),
    'voters_voted' => $tds[6]->plaintext,
    'voters_valid' => $tds[7]->plaintext,
    'valid_percentage' => str_replace(',','.',$tds[8]->plaintext),
  );
  $item = $row;
  unset($item['html']);
  $info = array_merge($item,$info);

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
          $item['party_number'] = $tds[0]->plaintext;
          $item['party'] = $tds[1]->plaintext;
          $item['votes'] = $tds[2]->plaintext;
          $item['votes_percentage'] = str_replace(',','.',$tds[3]->plaintext);
          $data[] = $item;
      }
    }
  }

  scraperwiki::save_sqlite(array('town_code'),$info,'info');
  scraperwiki::save_sqlite(array('town_code','party_number'),$data,'vote');
  scraperwiki::save_var('last_town_code',$info['town_code']);
  

}

?>
