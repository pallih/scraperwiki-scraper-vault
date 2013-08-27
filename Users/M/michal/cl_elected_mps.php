<?php

//get lists of elected MPs in Chile (and not elected, too, actually)
//source: possible also from http://elecciones.gob.cl/ !!

require 'scraperwiki/simple_html_dom.php';

$curl_options = array(
  array(CURLOPT_USERAGENT,'ScraperWiki.com; https://scraperwiki.com/scrapers/cl_elected_mps/'),
);



$last_number = 400;//scraperwiki::get_var('last_number',400);
$last_year = 2009;//scraperwiki::get_var('last_year',2009);
$last_sex = 0;//scraperwiki::get_var('last_sex',0);
$last_house = 0;//scraperwiki::get_var('last_house',0);

$sexs = array('0'=>'total','1'=>'varones','2'=>'mujeres');
$houses = array('0'=>'diputados','1'=>'senadores');

foreach ($houses as $hkey => $house) {
  if ($last_house > $hkey) continue;
  scraperwiki::save_var('last_house',$hkey);
  foreach ($sexs as $skey => $sex) {
    if (($last_house == $hkey) and ($last_sex > $skey)) continue;
    scraperwiki::save_var('last_sex',$skey);
    for ($year = 2009; $year >= 1989; $year = $year - 4) {
      if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year < $year)) continue;
      scraperwiki::save_var('last_year',$year);
      for ($number = 401; $number <= 460; $number++) {
        if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year = $skey) and ($last_number > $number)) continue;
        scraperwiki::save_var('last_number',$number);
        $url = "http://elecciones.gob.cl/SitioHistorico/paginas/{$year}/{$house}/distritos/candidatos/{$sex}/{$number}.htm";
        $html = html_entity_decode (iconv("ISO-8859-1", "UTF-8", grabber($url,$curl_options)),ENT_COMPAT,'UTF-8');
        $dom = new simple_html_dom();
        $dom->load($html);
        //check for empty file
        if (strpos($html,'Para esta zona no hay elección') > 0) continue;
        
        $data = get_data($dom,$house,$sex,$year,$number-400);
        scraperwiki::save_sqlite(array('year','house','district','i','sex'),$data);
      }
      scraperwiki::save_var('last_number',400);
      $last_number = 400;
    }
    scraperwiki::save_var('last_year',2009);
    $last_year = 2009;
  }
  scraperwiki::save_var('last_sex',0);
  $last_sex = 0;
}
scraperwiki::save_var('last_house',0);
$last_house = 0;
function get_data($dom,$house,$sex,$year,$district) {
  $data = array();
  $i = 1;
  $table = $dom->find('table[CellPadding=4]',0);
  $trs = $table->find('tr');
  array_shift($trs);
  array_pop($trs);
  foreach($trs as $tr) {
    $row = array(
        'year' => $year,
        'house' => $house,
        'sex' => $sex,
        'district' => $district
    );
    $tds = $tr->find('td');
    $row['name'] = $tds[0]->plaintext;
    $row['party'] = $tds[1]->plaintext;
    $row['votes'] = str_replace('.','',trim($tds[2]->plaintext));
    $row['percentage'] = str_replace(',','.',trim($tds[3]->plaintext));
    $row['elected'] = str_replace('&nbsp;','',trim($tds[4]->plaintext));
    $row['i'] = $i;
    $data[] = $row;
    $i++;
  }
  return $data;
}


//2001:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2001";
$html = grabber($url,$curl_options);//scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=sortable]',0);
$trs = $table->find('tr');
array_shift($trs);

$data = array();
$i = 1;
foreach ($trs as $tr) {
  $row = array();
  $tds = $tr->find('td');
  if ($tds[0]->plaintext != '')
    $last_district = $tds[0]->plaintext;
  $row['district'] = $last_district;
  $row['i'] = $i;
  $row['communities'] = $tds[1]->plaintext;
  $row['name'] = $tds[2]->find('a')->plaintext;
  $row['party_short_name'] = $tds[3]->plaintext;
  $row['party_long_name'] = $tds[3]->find('a',0)->title;
  $row['votes'] = str_replace('.','',$tds[4]->plaintext);
  $row['votes_percentage'] = str_replace(',','.',$tds[4]->plaintext);
  $row['year'] = '2002';
  $row['house'] = 'camara';
  $data[] = $row;
  $i++;
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);
*/

//2005:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2005";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',0);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
echo count($tds);
 for($j=0; $j<count($tds)/2; $j++) {
echo '*';
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2006';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;   
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);

//2010:
$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2009";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
//$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',1);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
 for($j=0; $j<count($tds)/2; $j++) {
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2010';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;  
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);



/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
<?php

//get lists of elected MPs in Chile (and not elected, too, actually)
//source: possible also from http://elecciones.gob.cl/ !!

require 'scraperwiki/simple_html_dom.php';

$curl_options = array(
  array(CURLOPT_USERAGENT,'ScraperWiki.com; https://scraperwiki.com/scrapers/cl_elected_mps/'),
);



$last_number = 400;//scraperwiki::get_var('last_number',400);
$last_year = 2009;//scraperwiki::get_var('last_year',2009);
$last_sex = 0;//scraperwiki::get_var('last_sex',0);
$last_house = 0;//scraperwiki::get_var('last_house',0);

$sexs = array('0'=>'total','1'=>'varones','2'=>'mujeres');
$houses = array('0'=>'diputados','1'=>'senadores');

foreach ($houses as $hkey => $house) {
  if ($last_house > $hkey) continue;
  scraperwiki::save_var('last_house',$hkey);
  foreach ($sexs as $skey => $sex) {
    if (($last_house == $hkey) and ($last_sex > $skey)) continue;
    scraperwiki::save_var('last_sex',$skey);
    for ($year = 2009; $year >= 1989; $year = $year - 4) {
      if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year < $year)) continue;
      scraperwiki::save_var('last_year',$year);
      for ($number = 401; $number <= 460; $number++) {
        if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year = $skey) and ($last_number > $number)) continue;
        scraperwiki::save_var('last_number',$number);
        $url = "http://elecciones.gob.cl/SitioHistorico/paginas/{$year}/{$house}/distritos/candidatos/{$sex}/{$number}.htm";
        $html = html_entity_decode (iconv("ISO-8859-1", "UTF-8", grabber($url,$curl_options)),ENT_COMPAT,'UTF-8');
        $dom = new simple_html_dom();
        $dom->load($html);
        //check for empty file
        if (strpos($html,'Para esta zona no hay elección') > 0) continue;
        
        $data = get_data($dom,$house,$sex,$year,$number-400);
        scraperwiki::save_sqlite(array('year','house','district','i','sex'),$data);
      }
      scraperwiki::save_var('last_number',400);
      $last_number = 400;
    }
    scraperwiki::save_var('last_year',2009);
    $last_year = 2009;
  }
  scraperwiki::save_var('last_sex',0);
  $last_sex = 0;
}
scraperwiki::save_var('last_house',0);
$last_house = 0;
function get_data($dom,$house,$sex,$year,$district) {
  $data = array();
  $i = 1;
  $table = $dom->find('table[CellPadding=4]',0);
  $trs = $table->find('tr');
  array_shift($trs);
  array_pop($trs);
  foreach($trs as $tr) {
    $row = array(
        'year' => $year,
        'house' => $house,
        'sex' => $sex,
        'district' => $district
    );
    $tds = $tr->find('td');
    $row['name'] = $tds[0]->plaintext;
    $row['party'] = $tds[1]->plaintext;
    $row['votes'] = str_replace('.','',trim($tds[2]->plaintext));
    $row['percentage'] = str_replace(',','.',trim($tds[3]->plaintext));
    $row['elected'] = str_replace('&nbsp;','',trim($tds[4]->plaintext));
    $row['i'] = $i;
    $data[] = $row;
    $i++;
  }
  return $data;
}


//2001:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2001";
$html = grabber($url,$curl_options);//scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=sortable]',0);
$trs = $table->find('tr');
array_shift($trs);

$data = array();
$i = 1;
foreach ($trs as $tr) {
  $row = array();
  $tds = $tr->find('td');
  if ($tds[0]->plaintext != '')
    $last_district = $tds[0]->plaintext;
  $row['district'] = $last_district;
  $row['i'] = $i;
  $row['communities'] = $tds[1]->plaintext;
  $row['name'] = $tds[2]->find('a')->plaintext;
  $row['party_short_name'] = $tds[3]->plaintext;
  $row['party_long_name'] = $tds[3]->find('a',0)->title;
  $row['votes'] = str_replace('.','',$tds[4]->plaintext);
  $row['votes_percentage'] = str_replace(',','.',$tds[4]->plaintext);
  $row['year'] = '2002';
  $row['house'] = 'camara';
  $data[] = $row;
  $i++;
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);
*/

//2005:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2005";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',0);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
echo count($tds);
 for($j=0; $j<count($tds)/2; $j++) {
echo '*';
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2006';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;   
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);

//2010:
$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2009";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
//$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',1);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
 for($j=0; $j<count($tds)/2; $j++) {
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2010';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;  
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);



/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
<?php

//get lists of elected MPs in Chile (and not elected, too, actually)
//source: possible also from http://elecciones.gob.cl/ !!

require 'scraperwiki/simple_html_dom.php';

$curl_options = array(
  array(CURLOPT_USERAGENT,'ScraperWiki.com; https://scraperwiki.com/scrapers/cl_elected_mps/'),
);



$last_number = 400;//scraperwiki::get_var('last_number',400);
$last_year = 2009;//scraperwiki::get_var('last_year',2009);
$last_sex = 0;//scraperwiki::get_var('last_sex',0);
$last_house = 0;//scraperwiki::get_var('last_house',0);

$sexs = array('0'=>'total','1'=>'varones','2'=>'mujeres');
$houses = array('0'=>'diputados','1'=>'senadores');

foreach ($houses as $hkey => $house) {
  if ($last_house > $hkey) continue;
  scraperwiki::save_var('last_house',$hkey);
  foreach ($sexs as $skey => $sex) {
    if (($last_house == $hkey) and ($last_sex > $skey)) continue;
    scraperwiki::save_var('last_sex',$skey);
    for ($year = 2009; $year >= 1989; $year = $year - 4) {
      if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year < $year)) continue;
      scraperwiki::save_var('last_year',$year);
      for ($number = 401; $number <= 460; $number++) {
        if (($last_house == $hkey) and ($last_sex == $skey) and ($last_year = $skey) and ($last_number > $number)) continue;
        scraperwiki::save_var('last_number',$number);
        $url = "http://elecciones.gob.cl/SitioHistorico/paginas/{$year}/{$house}/distritos/candidatos/{$sex}/{$number}.htm";
        $html = html_entity_decode (iconv("ISO-8859-1", "UTF-8", grabber($url,$curl_options)),ENT_COMPAT,'UTF-8');
        $dom = new simple_html_dom();
        $dom->load($html);
        //check for empty file
        if (strpos($html,'Para esta zona no hay elección') > 0) continue;
        
        $data = get_data($dom,$house,$sex,$year,$number-400);
        scraperwiki::save_sqlite(array('year','house','district','i','sex'),$data);
      }
      scraperwiki::save_var('last_number',400);
      $last_number = 400;
    }
    scraperwiki::save_var('last_year',2009);
    $last_year = 2009;
  }
  scraperwiki::save_var('last_sex',0);
  $last_sex = 0;
}
scraperwiki::save_var('last_house',0);
$last_house = 0;
function get_data($dom,$house,$sex,$year,$district) {
  $data = array();
  $i = 1;
  $table = $dom->find('table[CellPadding=4]',0);
  $trs = $table->find('tr');
  array_shift($trs);
  array_pop($trs);
  foreach($trs as $tr) {
    $row = array(
        'year' => $year,
        'house' => $house,
        'sex' => $sex,
        'district' => $district
    );
    $tds = $tr->find('td');
    $row['name'] = $tds[0]->plaintext;
    $row['party'] = $tds[1]->plaintext;
    $row['votes'] = str_replace('.','',trim($tds[2]->plaintext));
    $row['percentage'] = str_replace(',','.',trim($tds[3]->plaintext));
    $row['elected'] = str_replace('&nbsp;','',trim($tds[4]->plaintext));
    $row['i'] = $i;
    $data[] = $row;
    $i++;
  }
  return $data;
}


//2001:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2001";
$html = grabber($url,$curl_options);//scraperwiki::scrape($url);

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=sortable]',0);
$trs = $table->find('tr');
array_shift($trs);

$data = array();
$i = 1;
foreach ($trs as $tr) {
  $row = array();
  $tds = $tr->find('td');
  if ($tds[0]->plaintext != '')
    $last_district = $tds[0]->plaintext;
  $row['district'] = $last_district;
  $row['i'] = $i;
  $row['communities'] = $tds[1]->plaintext;
  $row['name'] = $tds[2]->find('a')->plaintext;
  $row['party_short_name'] = $tds[3]->plaintext;
  $row['party_long_name'] = $tds[3]->find('a',0)->title;
  $row['votes'] = str_replace('.','',$tds[4]->plaintext);
  $row['votes_percentage'] = str_replace(',','.',$tds[4]->plaintext);
  $row['year'] = '2002';
  $row['house'] = 'camara';
  $data[] = $row;
  $i++;
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);
*/

//2005:
/*$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2005";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',0);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
echo count($tds);
 for($j=0; $j<count($tds)/2; $j++) {
echo '*';
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2006';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;   
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);

//2010:
$url = "http://es.wikipedia.org/wiki/Elecciones_parlamentarias_de_Chile_de_2009";
  //for some reason, Wikipedia do not let me download the page, so I have saved it in our server, too
//$url = "http://test.kohovolit.sk/m/Elecciones_parlamentarias_de_Chile_de_2005.html";

//$html = scraperwiki::scrape($url);
$html = grabber($url,$curl_options);
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find('table[class=wikitable]',1);
$trs = $table->find('tr');
array_shift($trs);

$i = 0;
$data = array();
foreach ($trs as $tr) {
 $tds = $tr->find('td[bgcolor=#ECECEC]');
 for($j=0; $j<count($tds)/2; $j++) {
   $row = array();
   $row['district'] = floor($i/2) + 1;
   $row['i'] = $i+1;
   $row['name'] = $tds[$j*2]->plaintext;
   $row['party_short_name'] = $tds[$j*2]->plaintext;
   $tmp = $tds[$j*2]->find('a',0);
   if (count($tmp) > 0)
      $row['party_long_name'] = $tmp->title;
   $row['year'] = '2010';
   $row['house'] = 'camara';
   $data[] = $row;
   $i++;  
 }
}
scraperwiki::save_sqlite(array('year','house','district','i'),$data);



/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
