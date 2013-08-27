<?php

//scrapes list of football matches from eurofotbal.cz

require 'scraperwiki/simple_html_dom.php';

$until = 2013;

$leagues = array(
  'de' => array('name' => 'bundesliga', 'since' => 2002),
  'sk' => array('name' => 'corgon-liga', 'since' => 2002),
  'xe' => array('name' => 'premier-league', 'since' => 2000),
  'es' => array('name' => 'primera-division', 'since' => 2000),
  'it' => array('name' => 'serie-a', 'since' => 2000),
  'fr' => array('name' => 'ligue-1', 'since' => 2000),
  'ru' => array('name' => 'premier-liga', 'since' => 2003, 'special-ru' => true),
  'nl' => array('name' => 'eredivisie', 'since' => 2000), 
  'cz' => array('name' => 'gambrinus-liga', 'since' => 2002),
);

//download overview with matches
foreach ($leagues as $key => $league) {
  for ($year = $league['since']; $year < $until; $year++) {
    $next_year = $year + 1;
    $season = $year . '-' . $next_year;

    //corrections
    if (isset($league['special-ru']) and ($year <= 2010)) $season = $year;

    //get page
    $url = 'http://www.eurofotbal.cz/' . $league['name'] . '/' . $season .'/vysledky-rozlosovani/?month=0';
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //extract data
    $h2s = $dom->find('h2[class=pagesubtitle]');
    $tables = $dom->find('table[class=matches]');
    //get rid of "posledni zapasy"
    array_pop($tables);
    //get rid of "Nasledujici zapasy"
    if (count($tables) > 1)
      array_pop($tables);

    $data = array();

    foreach ($tables as $mkey => $table) {
      $trs = $table->find('tr');
      foreach ($trs as $tr) {
        $date = date2iso($tr->find('td',0)->plaintext);
        $time = $tr->find('td[class=time]',0)->plaintext;
        $teams = explode(' - ',$tr->find('td[class=teams]', 0)->find('div[class=fl]',0)->innertext);
//echo '**';
        $result = $tr->find('td',3)->plaintext;
//echo $result;
        $link = $tr->find('td',3)->find('a',0)->href;

        if ($result != 'info') { //it has been played already
    
            $result_ar = explode(':',$result);
            $id = trim(end(explode('-',$link)),'/');
    
            $data[] = array(
              'id' => $id,
              'country' => $key,
              'league' => $league['name'],
              'season' => $season,
              'part' => (isset($h2s[$mkey]) ? $h2s[$mkey]->plaintext : ''),
              'date' => $date,
              'time' => ($time == '?' ? '' : $time),
              'home' => trim($teams[0]),
              'visitor' => trim($teams[1]),
              'result' => $result,
              'home_goals' => $result_ar[0],
              'visitor_goals' => $result_ar[1],
              'result_code' => result_code($result_ar),
              'link' => $link
            );
//echo $teams[0].$tr->find('td[class=date]',0)->plaintext;
        }
      }
    }
    scraperwiki::save_sqlite(array('id'),$data);
  }
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

//scrapes list of football matches from eurofotbal.cz

require 'scraperwiki/simple_html_dom.php';

$until = 2013;

$leagues = array(
  'de' => array('name' => 'bundesliga', 'since' => 2002),
  'sk' => array('name' => 'corgon-liga', 'since' => 2002),
  'xe' => array('name' => 'premier-league', 'since' => 2000),
  'es' => array('name' => 'primera-division', 'since' => 2000),
  'it' => array('name' => 'serie-a', 'since' => 2000),
  'fr' => array('name' => 'ligue-1', 'since' => 2000),
  'ru' => array('name' => 'premier-liga', 'since' => 2003, 'special-ru' => true),
  'nl' => array('name' => 'eredivisie', 'since' => 2000), 
  'cz' => array('name' => 'gambrinus-liga', 'since' => 2002),
);

//download overview with matches
foreach ($leagues as $key => $league) {
  for ($year = $league['since']; $year < $until; $year++) {
    $next_year = $year + 1;
    $season = $year . '-' . $next_year;

    //corrections
    if (isset($league['special-ru']) and ($year <= 2010)) $season = $year;

    //get page
    $url = 'http://www.eurofotbal.cz/' . $league['name'] . '/' . $season .'/vysledky-rozlosovani/?month=0';
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //extract data
    $h2s = $dom->find('h2[class=pagesubtitle]');
    $tables = $dom->find('table[class=matches]');
    //get rid of "posledni zapasy"
    array_pop($tables);
    //get rid of "Nasledujici zapasy"
    if (count($tables) > 1)
      array_pop($tables);

    $data = array();

    foreach ($tables as $mkey => $table) {
      $trs = $table->find('tr');
      foreach ($trs as $tr) {
        $date = date2iso($tr->find('td',0)->plaintext);
        $time = $tr->find('td[class=time]',0)->plaintext;
        $teams = explode(' - ',$tr->find('td[class=teams]', 0)->find('div[class=fl]',0)->innertext);
//echo '**';
        $result = $tr->find('td',3)->plaintext;
//echo $result;
        $link = $tr->find('td',3)->find('a',0)->href;

        if ($result != 'info') { //it has been played already
    
            $result_ar = explode(':',$result);
            $id = trim(end(explode('-',$link)),'/');
    
            $data[] = array(
              'id' => $id,
              'country' => $key,
              'league' => $league['name'],
              'season' => $season,
              'part' => (isset($h2s[$mkey]) ? $h2s[$mkey]->plaintext : ''),
              'date' => $date,
              'time' => ($time == '?' ? '' : $time),
              'home' => trim($teams[0]),
              'visitor' => trim($teams[1]),
              'result' => $result,
              'home_goals' => $result_ar[0],
              'visitor_goals' => $result_ar[1],
              'result_code' => result_code($result_ar),
              'link' => $link
            );
//echo $teams[0].$tr->find('td[class=date]',0)->plaintext;
        }
      }
    }
    scraperwiki::save_sqlite(array('id'),$data);
  }
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

//scrapes list of football matches from eurofotbal.cz

require 'scraperwiki/simple_html_dom.php';

$until = 2013;

$leagues = array(
  'de' => array('name' => 'bundesliga', 'since' => 2002),
  'sk' => array('name' => 'corgon-liga', 'since' => 2002),
  'xe' => array('name' => 'premier-league', 'since' => 2000),
  'es' => array('name' => 'primera-division', 'since' => 2000),
  'it' => array('name' => 'serie-a', 'since' => 2000),
  'fr' => array('name' => 'ligue-1', 'since' => 2000),
  'ru' => array('name' => 'premier-liga', 'since' => 2003, 'special-ru' => true),
  'nl' => array('name' => 'eredivisie', 'since' => 2000), 
  'cz' => array('name' => 'gambrinus-liga', 'since' => 2002),
);

//download overview with matches
foreach ($leagues as $key => $league) {
  for ($year = $league['since']; $year < $until; $year++) {
    $next_year = $year + 1;
    $season = $year . '-' . $next_year;

    //corrections
    if (isset($league['special-ru']) and ($year <= 2010)) $season = $year;

    //get page
    $url = 'http://www.eurofotbal.cz/' . $league['name'] . '/' . $season .'/vysledky-rozlosovani/?month=0';
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //extract data
    $h2s = $dom->find('h2[class=pagesubtitle]');
    $tables = $dom->find('table[class=matches]');
    //get rid of "posledni zapasy"
    array_pop($tables);
    //get rid of "Nasledujici zapasy"
    if (count($tables) > 1)
      array_pop($tables);

    $data = array();

    foreach ($tables as $mkey => $table) {
      $trs = $table->find('tr');
      foreach ($trs as $tr) {
        $date = date2iso($tr->find('td',0)->plaintext);
        $time = $tr->find('td[class=time]',0)->plaintext;
        $teams = explode(' - ',$tr->find('td[class=teams]', 0)->find('div[class=fl]',0)->innertext);
//echo '**';
        $result = $tr->find('td',3)->plaintext;
//echo $result;
        $link = $tr->find('td',3)->find('a',0)->href;

        if ($result != 'info') { //it has been played already
    
            $result_ar = explode(':',$result);
            $id = trim(end(explode('-',$link)),'/');
    
            $data[] = array(
              'id' => $id,
              'country' => $key,
              'league' => $league['name'],
              'season' => $season,
              'part' => (isset($h2s[$mkey]) ? $h2s[$mkey]->plaintext : ''),
              'date' => $date,
              'time' => ($time == '?' ? '' : $time),
              'home' => trim($teams[0]),
              'visitor' => trim($teams[1]),
              'result' => $result,
              'home_goals' => $result_ar[0],
              'visitor_goals' => $result_ar[1],
              'result_code' => result_code($result_ar),
              'link' => $link
            );
//echo $teams[0].$tr->find('td[class=date]',0)->plaintext;
        }
      }
    }
    scraperwiki::save_sqlite(array('id'),$data);
  }
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
