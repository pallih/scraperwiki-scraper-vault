<?php

//Slovak parliament voting records retrieval
//using data from sk_parliament_voting_records_downloader

require 'scraperwiki/simple_html_dom.php';

//get last id
$last_id = scraperwiki::get_var('last_id',0);

//read the saved tables
scraperwiki::attach("sk_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
foreach ($rows as $row) {
  //get dom
  $dom = new simple_html_dom();
  $html = scraperwiki::select("* from src.swdata where id={$row['id']}");
  $dom->load(str_replace("&nbsp;"," ","<html><body>".$html[0]['html']."</body></html>"));

  //info
  $data = array('id'=>$row['id']);
  $divs = $dom->find("div[class=voting_stats_summary_full]");
  //session
  preg_match('/CisSchodze=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['session'] = $matches[1];
  //term
  preg_match('/CisObdobia=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['term'] = $matches[1];
  //date and time
  $divs2 = $divs[0]->find("div[class=grid_4]");
  $spans = $divs2[1]->find("span");
  preg_match('/([0-9]{1,2}). ([0-9]{1,2}). ([0-9]{4})/',$spans[0]->innertext,$matches);
  $data['date'] = $matches[3].'-'.n2($matches[2]).'-'.n2($matches[1]);
  preg_match('/([0-9]{1,2}):([0-9]{1,2})/',$spans[0]->innertext,$matches);
  $data['time'] = n2($matches[1]).':'.n2($matches[2]);
  //number of division in session
  $spans = $divs2[2]->find("span");
  $data['division_number'] = trim($spans[0]->innertext);
  //name
  $divs2 = $divs[0]->find("div[class=grid_12]");
  $spans = $divs2[0]->find("span");
  $data['name'] = trim($spans[0]->innertext);
  //results
  if (isset($divs2[1])) {
    $spans = $divs2[1]->find("span");
    if ($spans[0] == 'Návrh prešiel') $data['result'] == 'y';
    else if ($spans[0] == 'Návrh neprešiel') $data['result'] == 'n';
    else $data['result'] = trim($spans[0]->innertext);
  }
  //save info
  scraperwiki::save_sqlite(array('id'),$data,'info');
 
  //votes
  $data = array();
  //tables
  $tables = $dom->find("table");
  if (count($tables) > 0 ) //there are secret votes with no table, as http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=11438
    $trs = $tables[0]->find("tr");
  if (!empty($trs)) {
    foreach ($trs as $tr) {
      $tds = $tr->find("td");
      if (isset($tds[0]->colspan) and ($tds[0]->colspan == 4))
        $club = str_replace('Klub ','',$tds[0]->plaintext);
      else {
        $tds = $tr->find("td");
        foreach($tds as $td) {
          if (trim($td->innertext) != '') {
            preg_match('/\[([0-9a-zA-Z\?]{1})\]/',$td->innertext,$matches);
//echo $td->innertext;
            $vote = $matches[1];
            preg_match('/PoslanecID=([0-9]{1,})/',$td->innertext,$matches);
            $mp_id = $matches[1];
            $as = $td->find('a');
            $name = $as[0]->innertext;
            $data[] = array(
              'division_id' => $row['id'],
              'mp_id' => $mp_id,
              'vote' => $vote,
              'club' => $club,
              'name' => $name              
            );
          }
        }
      }
    }
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
  }
  scraperwiki::save_var('last_id',$row['id']);
}
}

// adds 0s before number
function n2($n) {
  if (($n < 10) and (strlen($n) < 2)) return '0'.$n;
  else return $n;
}

?>
<?php

//Slovak parliament voting records retrieval
//using data from sk_parliament_voting_records_downloader

require 'scraperwiki/simple_html_dom.php';

//get last id
$last_id = scraperwiki::get_var('last_id',0);

//read the saved tables
scraperwiki::attach("sk_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
foreach ($rows as $row) {
  //get dom
  $dom = new simple_html_dom();
  $html = scraperwiki::select("* from src.swdata where id={$row['id']}");
  $dom->load(str_replace("&nbsp;"," ","<html><body>".$html[0]['html']."</body></html>"));

  //info
  $data = array('id'=>$row['id']);
  $divs = $dom->find("div[class=voting_stats_summary_full]");
  //session
  preg_match('/CisSchodze=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['session'] = $matches[1];
  //term
  preg_match('/CisObdobia=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['term'] = $matches[1];
  //date and time
  $divs2 = $divs[0]->find("div[class=grid_4]");
  $spans = $divs2[1]->find("span");
  preg_match('/([0-9]{1,2}). ([0-9]{1,2}). ([0-9]{4})/',$spans[0]->innertext,$matches);
  $data['date'] = $matches[3].'-'.n2($matches[2]).'-'.n2($matches[1]);
  preg_match('/([0-9]{1,2}):([0-9]{1,2})/',$spans[0]->innertext,$matches);
  $data['time'] = n2($matches[1]).':'.n2($matches[2]);
  //number of division in session
  $spans = $divs2[2]->find("span");
  $data['division_number'] = trim($spans[0]->innertext);
  //name
  $divs2 = $divs[0]->find("div[class=grid_12]");
  $spans = $divs2[0]->find("span");
  $data['name'] = trim($spans[0]->innertext);
  //results
  if (isset($divs2[1])) {
    $spans = $divs2[1]->find("span");
    if ($spans[0] == 'Návrh prešiel') $data['result'] == 'y';
    else if ($spans[0] == 'Návrh neprešiel') $data['result'] == 'n';
    else $data['result'] = trim($spans[0]->innertext);
  }
  //save info
  scraperwiki::save_sqlite(array('id'),$data,'info');
 
  //votes
  $data = array();
  //tables
  $tables = $dom->find("table");
  if (count($tables) > 0 ) //there are secret votes with no table, as http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=11438
    $trs = $tables[0]->find("tr");
  if (!empty($trs)) {
    foreach ($trs as $tr) {
      $tds = $tr->find("td");
      if (isset($tds[0]->colspan) and ($tds[0]->colspan == 4))
        $club = str_replace('Klub ','',$tds[0]->plaintext);
      else {
        $tds = $tr->find("td");
        foreach($tds as $td) {
          if (trim($td->innertext) != '') {
            preg_match('/\[([0-9a-zA-Z\?]{1})\]/',$td->innertext,$matches);
//echo $td->innertext;
            $vote = $matches[1];
            preg_match('/PoslanecID=([0-9]{1,})/',$td->innertext,$matches);
            $mp_id = $matches[1];
            $as = $td->find('a');
            $name = $as[0]->innertext;
            $data[] = array(
              'division_id' => $row['id'],
              'mp_id' => $mp_id,
              'vote' => $vote,
              'club' => $club,
              'name' => $name              
            );
          }
        }
      }
    }
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
  }
  scraperwiki::save_var('last_id',$row['id']);
}
}

// adds 0s before number
function n2($n) {
  if (($n < 10) and (strlen($n) < 2)) return '0'.$n;
  else return $n;
}

?>
<?php

//Slovak parliament voting records retrieval
//using data from sk_parliament_voting_records_downloader

require 'scraperwiki/simple_html_dom.php';

//get last id
$last_id = scraperwiki::get_var('last_id',0);

//read the saved tables
scraperwiki::attach("sk_parliament_voting_records_downloader", "src");
$rows = scraperwiki::select("id from src.swdata where id>{$last_id} order by id");

if (!empty($rows)) {
foreach ($rows as $row) {
  //get dom
  $dom = new simple_html_dom();
  $html = scraperwiki::select("* from src.swdata where id={$row['id']}");
  $dom->load(str_replace("&nbsp;"," ","<html><body>".$html[0]['html']."</body></html>"));

  //info
  $data = array('id'=>$row['id']);
  $divs = $dom->find("div[class=voting_stats_summary_full]");
  //session
  preg_match('/CisSchodze=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['session'] = $matches[1];
  //term
  preg_match('/CisObdobia=([0-9]{1,})/',$divs[0]->innertext,$matches);
  $data['term'] = $matches[1];
  //date and time
  $divs2 = $divs[0]->find("div[class=grid_4]");
  $spans = $divs2[1]->find("span");
  preg_match('/([0-9]{1,2}). ([0-9]{1,2}). ([0-9]{4})/',$spans[0]->innertext,$matches);
  $data['date'] = $matches[3].'-'.n2($matches[2]).'-'.n2($matches[1]);
  preg_match('/([0-9]{1,2}):([0-9]{1,2})/',$spans[0]->innertext,$matches);
  $data['time'] = n2($matches[1]).':'.n2($matches[2]);
  //number of division in session
  $spans = $divs2[2]->find("span");
  $data['division_number'] = trim($spans[0]->innertext);
  //name
  $divs2 = $divs[0]->find("div[class=grid_12]");
  $spans = $divs2[0]->find("span");
  $data['name'] = trim($spans[0]->innertext);
  //results
  if (isset($divs2[1])) {
    $spans = $divs2[1]->find("span");
    if ($spans[0] == 'Návrh prešiel') $data['result'] == 'y';
    else if ($spans[0] == 'Návrh neprešiel') $data['result'] == 'n';
    else $data['result'] = trim($spans[0]->innertext);
  }
  //save info
  scraperwiki::save_sqlite(array('id'),$data,'info');
 
  //votes
  $data = array();
  //tables
  $tables = $dom->find("table");
  if (count($tables) > 0 ) //there are secret votes with no table, as http://www.nrsr.sk/web/Default.aspx?sid=schodze/hlasovanie/hlasklub&ID=11438
    $trs = $tables[0]->find("tr");
  if (!empty($trs)) {
    foreach ($trs as $tr) {
      $tds = $tr->find("td");
      if (isset($tds[0]->colspan) and ($tds[0]->colspan == 4))
        $club = str_replace('Klub ','',$tds[0]->plaintext);
      else {
        $tds = $tr->find("td");
        foreach($tds as $td) {
          if (trim($td->innertext) != '') {
            preg_match('/\[([0-9a-zA-Z\?]{1})\]/',$td->innertext,$matches);
//echo $td->innertext;
            $vote = $matches[1];
            preg_match('/PoslanecID=([0-9]{1,})/',$td->innertext,$matches);
            $mp_id = $matches[1];
            $as = $td->find('a');
            $name = $as[0]->innertext;
            $data[] = array(
              'division_id' => $row['id'],
              'mp_id' => $mp_id,
              'vote' => $vote,
              'club' => $club,
              'name' => $name              
            );
          }
        }
      }
    }
    scraperwiki::save_sqlite(array('division_id','mp_id','club'),$data,'vote');
  }
  scraperwiki::save_var('last_id',$row['id']);
}
}

// adds 0s before number
function n2($n) {
  if (($n < 10) and (strlen($n) < 2)) return '0'.$n;
  else return $n;
}

?>
