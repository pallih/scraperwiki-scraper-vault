<?php

//activity of CZ MPs (current term)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

//corrections:
//scraperwiki::save_var('last_id',0); //
//scraperwiki::sqliteexecute("delete from info where id>55899");
//scraperwiki::sqliteexecute("delete from vote where division_id>55899");
//scraperwiki::sqlitecommit();
//die();


//get last id
$last_id = scraperwiki::get_var('last_id');
echo "starting with id:" . $last_id . "\n";

scraperwiki::attach("cz_parliament_mps", "src");
$rows = scraperwiki::select("* from src.swdata where id>'{$last_id}' order by id");

//echo count($rows); die();

$i = 0;
foreach ($rows as $row) {

  $item = $row;

  //main MP page
  $url = "http://www.psp.cz/sqw/detail.sqw?o={$term}&id=". $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $dom = new simple_html_dom();
  $dom->load($html);


  //member since-until
  $li = $dom->find('li',0);
  if (strpos($li->innertext,'do ') > 0) {
    $item['since'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->innertext, ' od ','do '))));
    $item['until'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->outertext, 'do ','</li>'))));
  } else {
    $item['since'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->outertext, ' od ','</li>'))));
    $item['until'] = 'undefined';
  }


  //written changes proposals = amendments /  písemné pozměňovací návrhy
  $position = strpos($html,'Písemné pozměňovací návrhy');
  if ($position) {
    $item['amendment'] = get_first_string(substr($html,$position,100),'(',')');
  } else {
    $item['amendment'] = 0;
  }


  //interpelations oral
  $url = "http://www.psp.cz/sqw/interp.sqw?o={$term}&ic=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $tables = $dom->find('table');
  if (count($tables) > 0) {
    $trs = $tables[0]->find('tr');
    array_shift($trs);
    $sum = 0;
    foreach ($trs as $tr) {
      $session = explode('. ',$tr->find('a',0)->plaintext);
      $url1 = "http://www.psp.cz/sqw/interp.sqw?o={$term}&s={$session[0]}&ic=" . $row['id'];
//echo $url1;
      $html1 = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url1));
      preg_match_all('/#ececec/',$html1,$matches);
      //print_r($matches);die();
      $sum += count($matches[0]) - 2;
    }
    $item['interpelation_oral'] = $sum;
  } else {
    $item['interpelation_oral'] = 0;
  }  


  //interpelations written
  $url = "http://www.psp.cz/sqw/tisky.sqw?o={$term}&pi=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  if (strpos($html,'Celkem nalezen')) {
    $ar = explode(' ',trim(get_first_string($html,'Celkem nalezen','tisk')));
    $item['interpelation_written'] = $ar[count($ar)-1];
  }
  else
    $item['interpelation_written'] = 0;


  //law proposals / návrhy zákonů
  $url = "http://www.psp.cz/sqw/tisky.sqw?o={$term}&nz=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  if (strpos($html,'Celkem nalezen')) {
    $ar = explode(' ',trim(get_first_string($html,'Celkem nalezen','tisk')));
    $item['proposal'] = end($ar);
  }
  else
    $item['proposal'] = 0;

  //speeches (number of sessions)
  $url = "http://www.psp.cz/eknih/2010ps/rejstrik/jmenny/{$row['id']}.html";    //**********
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));  
  preg_match_all('/#sx/',$html,$matches);
  $item['speech_session'] = count($matches[0]);
  
  /*print_r($item);
  if ($i > 3)
    die();*/

  scraperwiki::save_var('last_id',$row['id']);
  scraperwiki::save_sqlite(array('id'),$item);

  $i++;
}

/**
* finds substrings between opening and closing markers
* @return result array of the substrings
*/
function returnSubstrings($text, $openingMarker, $closingMarker) {
$openingMarkerLength = strlen($openingMarker);
$closingMarkerLength = strlen($closingMarker);

$result = array();
$position = 0;
while (($position = strpos($text, $openingMarker, $position)) !== false) {
$position += $openingMarkerLength;
if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {
$result[] = substr($text, $position, $closingMarkerPosition - $position);
$position = $closingMarkerPosition + $closingMarkerLength;
}
}
return $result;
}


/**
* finds 1st substring between opening and closing markers
* @return result 1st substring
*/
function get_first_string ($text,$openingMarker, $closingMarker) {
$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);
$out = $out_ar[0];
return($out);
}

/**
* converts dates formats between Central European and ISO (ISO 8601)
* @return converted date
* examples:
* convert_date('2010-02-15','to euro')
*    returns '15.2.2010;
* convert_date('15.2.2010')
*    returns '2010-02-15'
*/
function convert_date($in,$way = 'to iso') {
$in = str_replace('&nbsp;','',$in);
if ($way == 'to iso') {
$ar = explode('.',$in);
$out = date('Y-m-d',mktime(0,0,0,$ar[1],$ar[0],$ar[2]));
} else {
$ar = explode('-',$in);
$out = date('j.n.Y',mktime(0,0,0,$ar[1],$ar[2],$ar[0]));
}
return $out;
}



?>
<?php

//activity of CZ MPs (current term)

require 'scraperwiki/simple_html_dom.php'; 

$term = 6;

//corrections:
//scraperwiki::save_var('last_id',0); //
//scraperwiki::sqliteexecute("delete from info where id>55899");
//scraperwiki::sqliteexecute("delete from vote where division_id>55899");
//scraperwiki::sqlitecommit();
//die();


//get last id
$last_id = scraperwiki::get_var('last_id');
echo "starting with id:" . $last_id . "\n";

scraperwiki::attach("cz_parliament_mps", "src");
$rows = scraperwiki::select("* from src.swdata where id>'{$last_id}' order by id");

//echo count($rows); die();

$i = 0;
foreach ($rows as $row) {

  $item = $row;

  //main MP page
  $url = "http://www.psp.cz/sqw/detail.sqw?o={$term}&id=". $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $dom = new simple_html_dom();
  $dom->load($html);


  //member since-until
  $li = $dom->find('li',0);
  if (strpos($li->innertext,'do ') > 0) {
    $item['since'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->innertext, ' od ','do '))));
    $item['until'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->outertext, 'do ','</li>'))));
  } else {
    $item['since'] = convert_date(str_replace('&nbsp;','',trim(get_first_string($li->outertext, ' od ','</li>'))));
    $item['until'] = 'undefined';
  }


  //written changes proposals = amendments /  písemné pozměňovací návrhy
  $position = strpos($html,'Písemné pozměňovací návrhy');
  if ($position) {
    $item['amendment'] = get_first_string(substr($html,$position,100),'(',')');
  } else {
    $item['amendment'] = 0;
  }


  //interpelations oral
  $url = "http://www.psp.cz/sqw/interp.sqw?o={$term}&ic=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $tables = $dom->find('table');
  if (count($tables) > 0) {
    $trs = $tables[0]->find('tr');
    array_shift($trs);
    $sum = 0;
    foreach ($trs as $tr) {
      $session = explode('. ',$tr->find('a',0)->plaintext);
      $url1 = "http://www.psp.cz/sqw/interp.sqw?o={$term}&s={$session[0]}&ic=" . $row['id'];
//echo $url1;
      $html1 = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url1));
      preg_match_all('/#ececec/',$html1,$matches);
      //print_r($matches);die();
      $sum += count($matches[0]) - 2;
    }
    $item['interpelation_oral'] = $sum;
  } else {
    $item['interpelation_oral'] = 0;
  }  


  //interpelations written
  $url = "http://www.psp.cz/sqw/tisky.sqw?o={$term}&pi=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  if (strpos($html,'Celkem nalezen')) {
    $ar = explode(' ',trim(get_first_string($html,'Celkem nalezen','tisk')));
    $item['interpelation_written'] = $ar[count($ar)-1];
  }
  else
    $item['interpelation_written'] = 0;


  //law proposals / návrhy zákonů
  $url = "http://www.psp.cz/sqw/tisky.sqw?o={$term}&nz=" . $row['id'];
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  if (strpos($html,'Celkem nalezen')) {
    $ar = explode(' ',trim(get_first_string($html,'Celkem nalezen','tisk')));
    $item['proposal'] = end($ar);
  }
  else
    $item['proposal'] = 0;

  //speeches (number of sessions)
  $url = "http://www.psp.cz/eknih/2010ps/rejstrik/jmenny/{$row['id']}.html";    //**********
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));  
  preg_match_all('/#sx/',$html,$matches);
  $item['speech_session'] = count($matches[0]);
  
  /*print_r($item);
  if ($i > 3)
    die();*/

  scraperwiki::save_var('last_id',$row['id']);
  scraperwiki::save_sqlite(array('id'),$item);

  $i++;
}

/**
* finds substrings between opening and closing markers
* @return result array of the substrings
*/
function returnSubstrings($text, $openingMarker, $closingMarker) {
$openingMarkerLength = strlen($openingMarker);
$closingMarkerLength = strlen($closingMarker);

$result = array();
$position = 0;
while (($position = strpos($text, $openingMarker, $position)) !== false) {
$position += $openingMarkerLength;
if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {
$result[] = substr($text, $position, $closingMarkerPosition - $position);
$position = $closingMarkerPosition + $closingMarkerLength;
}
}
return $result;
}


/**
* finds 1st substring between opening and closing markers
* @return result 1st substring
*/
function get_first_string ($text,$openingMarker, $closingMarker) {
$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);
$out = $out_ar[0];
return($out);
}

/**
* converts dates formats between Central European and ISO (ISO 8601)
* @return converted date
* examples:
* convert_date('2010-02-15','to euro')
*    returns '15.2.2010;
* convert_date('15.2.2010')
*    returns '2010-02-15'
*/
function convert_date($in,$way = 'to iso') {
$in = str_replace('&nbsp;','',$in);
if ($way == 'to iso') {
$ar = explode('.',$in);
$out = date('Y-m-d',mktime(0,0,0,$ar[1],$ar[0],$ar[2]));
} else {
$ar = explode('-',$in);
$out = date('j.n.Y',mktime(0,0,0,$ar[1],$ar[2],$ar[0]));
}
return $out;
}



?>
