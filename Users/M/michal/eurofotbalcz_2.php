<?php

//

require 'scraperwiki/simple_html_dom.php';

//save last id - temporary
//scraperwiki::save_var('last_id',0);

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;
//$last_id = 151526;//260766;
//zatim vse: 151526

//read the saved tables
scraperwiki::attach("eurofotbalcz_1", "src");
$rows = scraperwiki::select("* from src.swdata where id>{$last_id} and country='de' order by id");  //germany only
//$rows = scraperwiki::select("* from src.swdata where id>{$last_id} order by id");

foreach ($rows as $row) {
  $url = 'http://www.eurofotbal.cz' . $row['link'];
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $match_id = $row['id'];

  $date_ar = explode(' ',$dom->find('div[class=date]',0)->innertext);
  $date = date2iso($date_ar[0]);
  $time = ($date_ar[1] != '?' ? $date_ar[1] : '');
  $part = (is_object($dom->find('div[class=stage]',0)) ? $dom->find('div[class=stage]',0)->plaintext : '');
 
  //teams
  $table = $dom->find('table',0);
  $h2 = $table->find('h2',0);
  $home_link = $h2->find('a',0)->href;
  $visitor_link = $h2->find('a',1)->href;
  $home = $h2->find('a',0)->plaintext;
  $visitor = $h2->find('a',1)->plaintext;

  $result_ar0 = explode('<',$table->find('tr',1)->find('td',1)->innertext);
  $result = trim(str_replace(' ','',$result_ar0[0]),',');
  $result_ar = explode(':',$result);

  //sub results
  $result1 = $table->find('tr',1)->find('td',1)->find('span');
  if (count($result1) > 1) {
    $add_result = trim($result1[0]->plaintext);
    $half = $result1[1]->plaintext;
  } else {
    $add_result = '';
    $half = $result1[0]->plaintext;
  }
  $half_ar = explode(', ',trim($half,'()'));
  $halftime = $half_ar[0];
  $add_halftime = (isset($half_ar[1]) ? $half_ar[1] : '');

  $stadium_link = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->href : '') : '');
  $stadium = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->plaintext: '') : '');

  $bet365 = $dom->find('a[href=/bet365/]',0);
  if (is_object($bet365))
    $bet = explode(' - ', $bet365->plaintext);
  else
    $bet = array();

  //stats
  $referee = '';
  $visit = '';
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    $trs = $table->find('tr');
    foreach($trs as $tr) {
      if (strpos($tr->innertext,'Rozhodčí') > 0) {
        $ref_ar = explode('&nbsp;',$tr->plaintext);
        $referees_ar = explode('-',$ref_ar[1]);
        $referee = trim($referees_ar[0]);
        if (isset($referees_ar[1])) {
          $ref_ar2 = explode(',',$referees_ar[1]);
          $linesman_1 = trim($ref_ar2[0]);
          $linesman_2 = (isset($ref_ar2[1]) ? trim($ref_ar2[1]) : '');
        } else {
          $linesman_1 = '';
          $linesman_2 = '';
        }
      }
      if (strpos($tr->innertext,'Diváci') > 0) {
        $v_ar = explode('&nbsp;',$tr->plaintext);
        $visit = str_replace('.','',$v_ar[1]);
      }
    }
  }
  //match
  $data = array(
    'match_id' => $match_id,
    'date' => $date,
    'time' => $time,
    'part' => $part,
    'home' => $home,
    'visitor' => $visitor,
    'home_link' => $home_link,
    'visitor_link' => $visitor_link,
    'result' => $result,
    'home_goals' => $result_ar[0],
    'visitor_goals' => $result_ar[1],
    'result_code' => result_code($result_ar),
    'additional_result' => $add_result,
    'halftime' => $halftime,
    'additional_halftime' => $add_halftime,
    'stadium' => $stadium,
    'stadium_link' => $stadium_link,
    'bet365_1' => (isset($bet[0]) ? $bet[0] : ''),
    'bet365_2' => (isset($bet[2]) ? $bet[2] : ''),
    'bet365_0' => (isset($bet[1]) ? $bet[1] : ''),
    'referee' => $referee,
    'linesman_1' => $linesman_1,
    'linesman_2' => $linesman_2,
    'visit' => $visit,
    'league' => $row['league'],
    'country' => $row['country'],
    'season' => $row['season'],
    'link' => $row['link'],
  );
  //print_r($data);die();
  scraperwiki::save_sqlite(array('match_id'),$data,'match');

  
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    //goals
    $tr = $table->find('tr',0);
    $tds = $tr->find('td');
    $goals_home = str2action($tds[0]->innertext,'home',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_home,'goal');
    $goals_visitor = str2action($tds[2]->innertext,'visitor',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_visitor,'goal');  

    //cards
    $tr = $table->find('tr',1);
    $tds = $tr->find('td');
    $yellow_home = str2action($tds[0]->innertext,'home',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_home,'card');
    $yellow_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_visitor,'card');

    $tr = $table->find('tr',2);
    $tds = $tr->find('td');
    $red_home = str2action($tds[0]->innertext,'home',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_home,'card');
    $red_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_visitor,'card');


  }
  scraperwiki::save_var('last_id',$match_id);
}

function str2action($str,$home_visitor,$match_id,$card = null) {
  if ($str != '-') {
    $out = array();
    $rank = 1;
    $goals_ar = explode('<br>',$str);
    foreach ($goals_ar as $goalstr) {
      $fake_dom = new simple_html_dom();
      $fake_dom->load('<html><body>'.$goalstr.'</body></html>');
      if (is_object($fake_dom->find('a',0))) {
        $min_ar = explode('<',$goalstr);
        $minute = trim(trim($min_ar[0]),'.');
        $player = $fake_dom->find('a',0)->plaintext;
        $player_link = $fake_dom->find('a',0)->href;
      } else {
        $min_ar = explode('.',$goalstr);
        $minute = trim($min_ar[0]);
        array_shift($min_ar);
        $player = trim(implode('.',$min_ar));
        $player_link = '';
      }
      $note_ar = explode('</a>',$goalstr);
      $note = (isset($note_ar[1]) ? trim(trim($note_ar[1]),'()') : '');
      $data = array(
        'match_id' => $match_id,
        'minute' => $minute,
        'home_visitor' => $home_visitor,
        'player' => $player,
        'player_link' => $player_link,
        'note' => $note,
        'rank' => $rank,
      );
      if ($card) $data['card'] = $card;
      $out[] = $data;
      $rank++;
    }
    return $out;
  } else return array();
}

function result_code($r){
  if ($r[0] > $r[1]) return '1';
  else if ($r[1] > $r[0]) return '2';
  else return '0';
}

function date2iso($date) {
  $ar = explode('.',$date);
  return implode('-',array($ar[2],$ar[1],$ar[0]));
}
?>
<?php

//

require 'scraperwiki/simple_html_dom.php';

//save last id - temporary
//scraperwiki::save_var('last_id',0);

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;
//$last_id = 151526;//260766;
//zatim vse: 151526

//read the saved tables
scraperwiki::attach("eurofotbalcz_1", "src");
$rows = scraperwiki::select("* from src.swdata where id>{$last_id} and country='de' order by id");  //germany only
//$rows = scraperwiki::select("* from src.swdata where id>{$last_id} order by id");

foreach ($rows as $row) {
  $url = 'http://www.eurofotbal.cz' . $row['link'];
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $match_id = $row['id'];

  $date_ar = explode(' ',$dom->find('div[class=date]',0)->innertext);
  $date = date2iso($date_ar[0]);
  $time = ($date_ar[1] != '?' ? $date_ar[1] : '');
  $part = (is_object($dom->find('div[class=stage]',0)) ? $dom->find('div[class=stage]',0)->plaintext : '');
 
  //teams
  $table = $dom->find('table',0);
  $h2 = $table->find('h2',0);
  $home_link = $h2->find('a',0)->href;
  $visitor_link = $h2->find('a',1)->href;
  $home = $h2->find('a',0)->plaintext;
  $visitor = $h2->find('a',1)->plaintext;

  $result_ar0 = explode('<',$table->find('tr',1)->find('td',1)->innertext);
  $result = trim(str_replace(' ','',$result_ar0[0]),',');
  $result_ar = explode(':',$result);

  //sub results
  $result1 = $table->find('tr',1)->find('td',1)->find('span');
  if (count($result1) > 1) {
    $add_result = trim($result1[0]->plaintext);
    $half = $result1[1]->plaintext;
  } else {
    $add_result = '';
    $half = $result1[0]->plaintext;
  }
  $half_ar = explode(', ',trim($half,'()'));
  $halftime = $half_ar[0];
  $add_halftime = (isset($half_ar[1]) ? $half_ar[1] : '');

  $stadium_link = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->href : '') : '');
  $stadium = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->plaintext: '') : '');

  $bet365 = $dom->find('a[href=/bet365/]',0);
  if (is_object($bet365))
    $bet = explode(' - ', $bet365->plaintext);
  else
    $bet = array();

  //stats
  $referee = '';
  $visit = '';
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    $trs = $table->find('tr');
    foreach($trs as $tr) {
      if (strpos($tr->innertext,'Rozhodčí') > 0) {
        $ref_ar = explode('&nbsp;',$tr->plaintext);
        $referees_ar = explode('-',$ref_ar[1]);
        $referee = trim($referees_ar[0]);
        if (isset($referees_ar[1])) {
          $ref_ar2 = explode(',',$referees_ar[1]);
          $linesman_1 = trim($ref_ar2[0]);
          $linesman_2 = (isset($ref_ar2[1]) ? trim($ref_ar2[1]) : '');
        } else {
          $linesman_1 = '';
          $linesman_2 = '';
        }
      }
      if (strpos($tr->innertext,'Diváci') > 0) {
        $v_ar = explode('&nbsp;',$tr->plaintext);
        $visit = str_replace('.','',$v_ar[1]);
      }
    }
  }
  //match
  $data = array(
    'match_id' => $match_id,
    'date' => $date,
    'time' => $time,
    'part' => $part,
    'home' => $home,
    'visitor' => $visitor,
    'home_link' => $home_link,
    'visitor_link' => $visitor_link,
    'result' => $result,
    'home_goals' => $result_ar[0],
    'visitor_goals' => $result_ar[1],
    'result_code' => result_code($result_ar),
    'additional_result' => $add_result,
    'halftime' => $halftime,
    'additional_halftime' => $add_halftime,
    'stadium' => $stadium,
    'stadium_link' => $stadium_link,
    'bet365_1' => (isset($bet[0]) ? $bet[0] : ''),
    'bet365_2' => (isset($bet[2]) ? $bet[2] : ''),
    'bet365_0' => (isset($bet[1]) ? $bet[1] : ''),
    'referee' => $referee,
    'linesman_1' => $linesman_1,
    'linesman_2' => $linesman_2,
    'visit' => $visit,
    'league' => $row['league'],
    'country' => $row['country'],
    'season' => $row['season'],
    'link' => $row['link'],
  );
  //print_r($data);die();
  scraperwiki::save_sqlite(array('match_id'),$data,'match');

  
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    //goals
    $tr = $table->find('tr',0);
    $tds = $tr->find('td');
    $goals_home = str2action($tds[0]->innertext,'home',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_home,'goal');
    $goals_visitor = str2action($tds[2]->innertext,'visitor',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_visitor,'goal');  

    //cards
    $tr = $table->find('tr',1);
    $tds = $tr->find('td');
    $yellow_home = str2action($tds[0]->innertext,'home',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_home,'card');
    $yellow_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_visitor,'card');

    $tr = $table->find('tr',2);
    $tds = $tr->find('td');
    $red_home = str2action($tds[0]->innertext,'home',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_home,'card');
    $red_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_visitor,'card');


  }
  scraperwiki::save_var('last_id',$match_id);
}

function str2action($str,$home_visitor,$match_id,$card = null) {
  if ($str != '-') {
    $out = array();
    $rank = 1;
    $goals_ar = explode('<br>',$str);
    foreach ($goals_ar as $goalstr) {
      $fake_dom = new simple_html_dom();
      $fake_dom->load('<html><body>'.$goalstr.'</body></html>');
      if (is_object($fake_dom->find('a',0))) {
        $min_ar = explode('<',$goalstr);
        $minute = trim(trim($min_ar[0]),'.');
        $player = $fake_dom->find('a',0)->plaintext;
        $player_link = $fake_dom->find('a',0)->href;
      } else {
        $min_ar = explode('.',$goalstr);
        $minute = trim($min_ar[0]);
        array_shift($min_ar);
        $player = trim(implode('.',$min_ar));
        $player_link = '';
      }
      $note_ar = explode('</a>',$goalstr);
      $note = (isset($note_ar[1]) ? trim(trim($note_ar[1]),'()') : '');
      $data = array(
        'match_id' => $match_id,
        'minute' => $minute,
        'home_visitor' => $home_visitor,
        'player' => $player,
        'player_link' => $player_link,
        'note' => $note,
        'rank' => $rank,
      );
      if ($card) $data['card'] = $card;
      $out[] = $data;
      $rank++;
    }
    return $out;
  } else return array();
}

function result_code($r){
  if ($r[0] > $r[1]) return '1';
  else if ($r[1] > $r[0]) return '2';
  else return '0';
}

function date2iso($date) {
  $ar = explode('.',$date);
  return implode('-',array($ar[2],$ar[1],$ar[0]));
}
?>
<?php

//

require 'scraperwiki/simple_html_dom.php';

//save last id - temporary
//scraperwiki::save_var('last_id',0);

//get last id
$last_id = scraperwiki::get_var('last_id',0);
echo $last_id;
//$last_id = 151526;//260766;
//zatim vse: 151526

//read the saved tables
scraperwiki::attach("eurofotbalcz_1", "src");
$rows = scraperwiki::select("* from src.swdata where id>{$last_id} and country='de' order by id");  //germany only
//$rows = scraperwiki::select("* from src.swdata where id>{$last_id} order by id");

foreach ($rows as $row) {
  $url = 'http://www.eurofotbal.cz' . $row['link'];
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //info
  $match_id = $row['id'];

  $date_ar = explode(' ',$dom->find('div[class=date]',0)->innertext);
  $date = date2iso($date_ar[0]);
  $time = ($date_ar[1] != '?' ? $date_ar[1] : '');
  $part = (is_object($dom->find('div[class=stage]',0)) ? $dom->find('div[class=stage]',0)->plaintext : '');
 
  //teams
  $table = $dom->find('table',0);
  $h2 = $table->find('h2',0);
  $home_link = $h2->find('a',0)->href;
  $visitor_link = $h2->find('a',1)->href;
  $home = $h2->find('a',0)->plaintext;
  $visitor = $h2->find('a',1)->plaintext;

  $result_ar0 = explode('<',$table->find('tr',1)->find('td',1)->innertext);
  $result = trim(str_replace(' ','',$result_ar0[0]),',');
  $result_ar = explode(':',$result);

  //sub results
  $result1 = $table->find('tr',1)->find('td',1)->find('span');
  if (count($result1) > 1) {
    $add_result = trim($result1[0]->plaintext);
    $half = $result1[1]->plaintext;
  } else {
    $add_result = '';
    $half = $result1[0]->plaintext;
  }
  $half_ar = explode(', ',trim($half,'()'));
  $halftime = $half_ar[0];
  $add_halftime = (isset($half_ar[1]) ? $half_ar[1] : '');

  $stadium_link = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->href : '') : '');
  $stadium = (is_object($dom->find('div[class=stadium]',0)) ? (is_object($dom->find('div[class=stadium]',0)->find('a',0)) ? $dom->find('div[class=stadium]',0)->find('a',0)->plaintext: '') : '');

  $bet365 = $dom->find('a[href=/bet365/]',0);
  if (is_object($bet365))
    $bet = explode(' - ', $bet365->plaintext);
  else
    $bet = array();

  //stats
  $referee = '';
  $visit = '';
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    $trs = $table->find('tr');
    foreach($trs as $tr) {
      if (strpos($tr->innertext,'Rozhodčí') > 0) {
        $ref_ar = explode('&nbsp;',$tr->plaintext);
        $referees_ar = explode('-',$ref_ar[1]);
        $referee = trim($referees_ar[0]);
        if (isset($referees_ar[1])) {
          $ref_ar2 = explode(',',$referees_ar[1]);
          $linesman_1 = trim($ref_ar2[0]);
          $linesman_2 = (isset($ref_ar2[1]) ? trim($ref_ar2[1]) : '');
        } else {
          $linesman_1 = '';
          $linesman_2 = '';
        }
      }
      if (strpos($tr->innertext,'Diváci') > 0) {
        $v_ar = explode('&nbsp;',$tr->plaintext);
        $visit = str_replace('.','',$v_ar[1]);
      }
    }
  }
  //match
  $data = array(
    'match_id' => $match_id,
    'date' => $date,
    'time' => $time,
    'part' => $part,
    'home' => $home,
    'visitor' => $visitor,
    'home_link' => $home_link,
    'visitor_link' => $visitor_link,
    'result' => $result,
    'home_goals' => $result_ar[0],
    'visitor_goals' => $result_ar[1],
    'result_code' => result_code($result_ar),
    'additional_result' => $add_result,
    'halftime' => $halftime,
    'additional_halftime' => $add_halftime,
    'stadium' => $stadium,
    'stadium_link' => $stadium_link,
    'bet365_1' => (isset($bet[0]) ? $bet[0] : ''),
    'bet365_2' => (isset($bet[2]) ? $bet[2] : ''),
    'bet365_0' => (isset($bet[1]) ? $bet[1] : ''),
    'referee' => $referee,
    'linesman_1' => $linesman_1,
    'linesman_2' => $linesman_2,
    'visit' => $visit,
    'league' => $row['league'],
    'country' => $row['country'],
    'season' => $row['season'],
    'link' => $row['link'],
  );
  //print_r($data);die();
  scraperwiki::save_sqlite(array('match_id'),$data,'match');

  
  $table = $dom->find('table[class=matchstats]',0);
  if (is_object($table)) {
    //goals
    $tr = $table->find('tr',0);
    $tds = $tr->find('td');
    $goals_home = str2action($tds[0]->innertext,'home',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_home,'goal');
    $goals_visitor = str2action($tds[2]->innertext,'visitor',$match_id);
    scraperwiki::save_sqlite(array('match_id','home_visitor','rank'),$goals_visitor,'goal');  

    //cards
    $tr = $table->find('tr',1);
    $tds = $tr->find('td');
    $yellow_home = str2action($tds[0]->innertext,'home',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_home,'card');
    $yellow_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'yellow');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$yellow_visitor,'card');

    $tr = $table->find('tr',2);
    $tds = $tr->find('td');
    $red_home = str2action($tds[0]->innertext,'home',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_home,'card');
    $red_visitor = str2action($tds[2]->innertext,'visitor',$match_id,'red');
    scraperwiki::save_sqlite(array('match_id','home_visitor','card','rank'),$red_visitor,'card');


  }
  scraperwiki::save_var('last_id',$match_id);
}

function str2action($str,$home_visitor,$match_id,$card = null) {
  if ($str != '-') {
    $out = array();
    $rank = 1;
    $goals_ar = explode('<br>',$str);
    foreach ($goals_ar as $goalstr) {
      $fake_dom = new simple_html_dom();
      $fake_dom->load('<html><body>'.$goalstr.'</body></html>');
      if (is_object($fake_dom->find('a',0))) {
        $min_ar = explode('<',$goalstr);
        $minute = trim(trim($min_ar[0]),'.');
        $player = $fake_dom->find('a',0)->plaintext;
        $player_link = $fake_dom->find('a',0)->href;
      } else {
        $min_ar = explode('.',$goalstr);
        $minute = trim($min_ar[0]);
        array_shift($min_ar);
        $player = trim(implode('.',$min_ar));
        $player_link = '';
      }
      $note_ar = explode('</a>',$goalstr);
      $note = (isset($note_ar[1]) ? trim(trim($note_ar[1]),'()') : '');
      $data = array(
        'match_id' => $match_id,
        'minute' => $minute,
        'home_visitor' => $home_visitor,
        'player' => $player,
        'player_link' => $player_link,
        'note' => $note,
        'rank' => $rank,
      );
      if ($card) $data['card'] = $card;
      $out[] = $data;
      $rank++;
    }
    return $out;
  } else return array();
}

function result_code($r){
  if ($r[0] > $r[1]) return '1';
  else if ($r[1] > $r[0]) return '2';
  else return '0';
}

function date2iso($date) {
  $ar = explode('.',$date);
  return implode('-',array($ar[2],$ar[1],$ar[0]));
}
?>
