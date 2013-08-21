<?php

//Chilean parliament voting records downloader
//original url: http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=1282
//there are many empty ids!

require 'scraperwiki/simple_html_dom.php'; 

//get last i
//scraperwiki::save_var('last_i',1282); //temp
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//test
//$i = 1920;


//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it valid division (or empty)
  $valid = false;
  $divs = $dom->find('div[class=stress]');
  foreach($divs as $div) {
    $tables = $div->find('table');
    if (count($tables) > 0) $valid = true;
  }
  if (!$valid)
    $consecutive_empty ++;
  else {
    $consecutive_empty = 0;

    //extract useful html
    $part0 = $dom->find('div[id=ctl00_mainPlaceHolder_pnlBoletin]');
    $part0b = $dom->find('div[id=ctl00_mainPlaceHolder_pnlOtro]');
    $part0c = $dom->find('div[id=ctl00_mainPlaceHolder_pnlPacuerdo]');
    $part1 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlAFavor]');
    $part2 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlEncontra]');
    $part3 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlAbstencion]');
    $part4 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlArt5]'); //e.g. i=11969
    $part5 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlPareos]'); //e.g. i=11969
 
    //save it
    $data = array(
       'id' => $i,
     ); 
    if (isset($part0[0])) $data['info'] = $part0[0]->outertext;
    else if (isset($part0b[0])) $data['info'] = $part0b[0]->outertext;
    else if (isset($part0c[0])) $data['info'] = $part0c[0]->outertext;
    if (isset($part1[0])) $data['for'] = $part1[0]->outertext;
    if (isset($part2[0])) $data['against'] = $part2[0]->outertext;
    if (isset($part3[0])) $data['abstain'] = $part3[0]->outertext;
    if (isset($part4[0])) $data['art5'] = $part4[0]->outertext;
    if (isset($part5[0])) $data['paired'] = $part5[0]->outertext;
    scraperwiki::save_sqlite(array('id'),$data);
    $last_ok_i = $i;
    scraperwiki::save_var('last_i',$i);

    //find date
    if (isset($part0[0])) $ps = $part0[0]->find('p');
    else if (isset($part0b[0]))$ps = $part0b[0]->find('p');
    else $ps = $part0c[0]->find('p');
    $tmp = date_es2iso($ps[0]->plaintext);
    $last_date= new DateTime($tmp);
  }
  $i++;

  //continue?
  $interval = $last_date->diff($now);
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 200))  {
    $continue = false;
  }
}

function date_es2iso ($date) {
  $replacement = array(
    'Ene' => '01',
    'Feb' => '02',
    'Mar' => '03',
    'Abr' => '04',
    'May' => '05',
    'Jun' => '06',
    'Jul' => '07',
    'Ago' => '08',
    'Sep' => '09',
    'Set' => '09',
    'Oct' => '10',
    'Nov' => '11',
    'Dic' => '12',
  );
    foreach ($replacement as $key => $r) {
      $date = str_replace(' de '.$key.'. de ','-'.$r.'-',$date);
    }
    preg_match('/([0-9]{2})-([0-9]{2})-([0-9]{4})/',$date,$matches);
    return $matches[3].'-'.$matches[2].'-'.$matches[1];
}

?>
<?php

//Chilean parliament voting records downloader
//original url: http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=1282
//there are many empty ids!

require 'scraperwiki/simple_html_dom.php'; 

//get last i
//scraperwiki::save_var('last_i',1282); //temp
$i = scraperwiki::get_var('last_i',0);
$last_ok_i = $i;

//test
//$i = 1920;


//set conditions to continue
$continue = true;
$consecutive_empty = 0;
date_default_timezone_set('UTC');
$last_date = new DateTime('1993-01-01');
$now = new DateTime('now');

while ($continue) {
  $url = "http://www.camara.cl/trabajamos/sala_votacion_detalle.aspx?prmID=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  //is it valid division (or empty)
  $valid = false;
  $divs = $dom->find('div[class=stress]');
  foreach($divs as $div) {
    $tables = $div->find('table');
    if (count($tables) > 0) $valid = true;
  }
  if (!$valid)
    $consecutive_empty ++;
  else {
    $consecutive_empty = 0;

    //extract useful html
    $part0 = $dom->find('div[id=ctl00_mainPlaceHolder_pnlBoletin]');
    $part0b = $dom->find('div[id=ctl00_mainPlaceHolder_pnlOtro]');
    $part0c = $dom->find('div[id=ctl00_mainPlaceHolder_pnlPacuerdo]');
    $part1 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlAFavor]');
    $part2 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlEncontra]');
    $part3 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlAbstencion]');
    $part4 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlArt5]'); //e.g. i=11969
    $part5 = $dom->find('table[id=ctl00_mainPlaceHolder_dtlPareos]'); //e.g. i=11969
 
    //save it
    $data = array(
       'id' => $i,
     ); 
    if (isset($part0[0])) $data['info'] = $part0[0]->outertext;
    else if (isset($part0b[0])) $data['info'] = $part0b[0]->outertext;
    else if (isset($part0c[0])) $data['info'] = $part0c[0]->outertext;
    if (isset($part1[0])) $data['for'] = $part1[0]->outertext;
    if (isset($part2[0])) $data['against'] = $part2[0]->outertext;
    if (isset($part3[0])) $data['abstain'] = $part3[0]->outertext;
    if (isset($part4[0])) $data['art5'] = $part4[0]->outertext;
    if (isset($part5[0])) $data['paired'] = $part5[0]->outertext;
    scraperwiki::save_sqlite(array('id'),$data);
    $last_ok_i = $i;
    scraperwiki::save_var('last_i',$i);

    //find date
    if (isset($part0[0])) $ps = $part0[0]->find('p');
    else if (isset($part0b[0]))$ps = $part0b[0]->find('p');
    else $ps = $part0c[0]->find('p');
    $tmp = date_es2iso($ps[0]->plaintext);
    $last_date= new DateTime($tmp);
  }
  $i++;

  //continue?
  $interval = $last_date->diff($now);
  if ($interval->format('%r%a') < 180) $date_condition = true; else $date_condition = false; //always continue when the division is more than 6 months old
  if ($date_condition and ($consecutive_empty > 200))  {
    $continue = false;
  }
}

function date_es2iso ($date) {
  $replacement = array(
    'Ene' => '01',
    'Feb' => '02',
    'Mar' => '03',
    'Abr' => '04',
    'May' => '05',
    'Jun' => '06',
    'Jul' => '07',
    'Ago' => '08',
    'Sep' => '09',
    'Set' => '09',
    'Oct' => '10',
    'Nov' => '11',
    'Dic' => '12',
  );
    foreach ($replacement as $key => $r) {
      $date = str_replace(' de '.$key.'. de ','-'.$r.'-',$date);
    }
    preg_match('/([0-9]{2})-([0-9]{2})-([0-9]{4})/',$date,$matches);
    return $matches[3].'-'.$matches[2].'-'.$matches[1];
}

?>
