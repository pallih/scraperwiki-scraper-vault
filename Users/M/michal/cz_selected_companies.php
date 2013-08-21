<?php

//get changes in Czech firms
require 'scraperwiki/simple_html_dom.php'; 

//get list of organizations' ids (IČO)
$url = 'https://docs.google.com/spreadsheet/pub?key=0ApmBqWaAzMn_dGItc2VMV2liQTJCTG43UncyQVNoakE&output=txt';
$rows = str_getcsv(scraperwiki::scrape($url),"\n");
foreach ($rows as $row)
  $ar[] = str_getcsv($row,"\t");
//remove first line
array_shift($ar);

$today = date("Y-m-d");

foreach ($ar as $row) {
  $url = 'https://or.justice.cz/ias/ui/rejstrik-dotaz?dotaz=' . $row[0];
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

//echo $html;die();

  $ul = $dom->find('ul[class=result-links]',0);
  $lis = $ul->find('li');

  
  $url = 'https://or.justice.cz' . str_replace('&amp;','&', $lis[1]->find('a',0)->href);
  /*$options = array(
       array(CURLOPT_USERAGENT,'Googlebot/2.1 (+http://www.google.com/bot.html)'),
  );*/
  $html = scraperwiki::scrape($url);//grabber($url,$options);
//echo $url;
//echo $html;die();
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  $name = iconv("UTF-8", "ASCII//IGNORE", trim($dom->find('h2',0)->plaintext));

  $spans1 = $dom->find('span[class=platne]');
  $spans2 = $dom->find('span[class=neplatne]');

  foreach ($spans1 as $s) {
    $in_ar = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$s->plaintext)));
    if ($in_ar[0] == 'Zapsáno') {
      $in_ar2 = explode('.',$in_ar[1]);
      $date = trim($in_ar2[2]) . '-' . n2(months($in_ar2[1])) . '-' .  n2($in_ar2[0]);
      $data = array(
        'org_id' => $row[0],
        'org_name' => $name,
        'since' => $date,
        'text' => iconv("UTF-8", "ASCII//IGNORE",$last_text),
        'active' => 'active',
        'last_updated' => $today,
        'last_change' => $date,
      );
      scraperwiki::save_sqlite(array('org_id','since','text'),$data);
    } else {
      $last_text = $s->innertext;
    }
  }

  foreach ($spans2 as $s) {
    $in_ar0 = explode('&nbsp;&nbsp;&nbsp;',$s->plaintext);
    $in_ar = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$in_ar0[0])));
    if ($in_ar[0] == 'Zapsáno') {
      $in_ar2 = explode('.',$in_ar[1]);
      $date = trim($in_ar2[2]) . '-' . n2(months($in_ar2[1])) . '-' .  n2($in_ar2[0]);
      $in_ar_until = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$in_ar0[1])));
      $in_ar2_until = explode('.',$in_ar_until[1]);
      $date_until = trim($in_ar2_until[2]) . '-' . n2(months($in_ar2_until[1])) . '-' .  n2($in_ar2_until[0]);
      $data = array(
        'org_id' => $row[0],
        'org_name' => $name,
        'since' => $date,
        'text' => iconv("UTF-8", "ASCII//IGNORE",$last_text),
        'active' => 'historical',
        'until' => $date_until,
        'last_updated' => $today,
        'last_change' => $date_until,
      );
      scraperwiki::save_sqlite(array('org_id','since','text'),$data);
    } else {
      $last_text = $s->innertext;
    }
  }

}

function months($m) {
  switch($m) {
    case 'ledna': return '1';
    case 'února': return '2';
    case 'března': return '3';
    case 'dubna': return '4';
    case 'května': return '5';
    case 'června': return '6';
    case 'července': return '7';
    case 'srpna': return '8';
    case 'září': return '9';
    case 'října': return '10';
    case 'listopadu': return '11';
    case 'prosince': return '12';
  }
}

function n2($n){
  if ($n<10) return '0'.$n;
  else return $n;
}

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

//get changes in Czech firms
require 'scraperwiki/simple_html_dom.php'; 

//get list of organizations' ids (IČO)
$url = 'https://docs.google.com/spreadsheet/pub?key=0ApmBqWaAzMn_dGItc2VMV2liQTJCTG43UncyQVNoakE&output=txt';
$rows = str_getcsv(scraperwiki::scrape($url),"\n");
foreach ($rows as $row)
  $ar[] = str_getcsv($row,"\t");
//remove first line
array_shift($ar);

$today = date("Y-m-d");

foreach ($ar as $row) {
  $url = 'https://or.justice.cz/ias/ui/rejstrik-dotaz?dotaz=' . $row[0];
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

//echo $html;die();

  $ul = $dom->find('ul[class=result-links]',0);
  $lis = $ul->find('li');

  
  $url = 'https://or.justice.cz' . str_replace('&amp;','&', $lis[1]->find('a',0)->href);
  /*$options = array(
       array(CURLOPT_USERAGENT,'Googlebot/2.1 (+http://www.google.com/bot.html)'),
  );*/
  $html = scraperwiki::scrape($url);//grabber($url,$options);
//echo $url;
//echo $html;die();
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);

  $name = iconv("UTF-8", "ASCII//IGNORE", trim($dom->find('h2',0)->plaintext));

  $spans1 = $dom->find('span[class=platne]');
  $spans2 = $dom->find('span[class=neplatne]');

  foreach ($spans1 as $s) {
    $in_ar = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$s->plaintext)));
    if ($in_ar[0] == 'Zapsáno') {
      $in_ar2 = explode('.',$in_ar[1]);
      $date = trim($in_ar2[2]) . '-' . n2(months($in_ar2[1])) . '-' .  n2($in_ar2[0]);
      $data = array(
        'org_id' => $row[0],
        'org_name' => $name,
        'since' => $date,
        'text' => iconv("UTF-8", "ASCII//IGNORE",$last_text),
        'active' => 'active',
        'last_updated' => $today,
        'last_change' => $date,
      );
      scraperwiki::save_sqlite(array('org_id','since','text'),$data);
    } else {
      $last_text = $s->innertext;
    }
  }

  foreach ($spans2 as $s) {
    $in_ar0 = explode('&nbsp;&nbsp;&nbsp;',$s->plaintext);
    $in_ar = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$in_ar0[0])));
    if ($in_ar[0] == 'Zapsáno') {
      $in_ar2 = explode('.',$in_ar[1]);
      $date = trim($in_ar2[2]) . '-' . n2(months($in_ar2[1])) . '-' .  n2($in_ar2[0]);
      $in_ar_until = explode(':',str_replace(' ','.',str_replace('&nbsp;','',$in_ar0[1])));
      $in_ar2_until = explode('.',$in_ar_until[1]);
      $date_until = trim($in_ar2_until[2]) . '-' . n2(months($in_ar2_until[1])) . '-' .  n2($in_ar2_until[0]);
      $data = array(
        'org_id' => $row[0],
        'org_name' => $name,
        'since' => $date,
        'text' => iconv("UTF-8", "ASCII//IGNORE",$last_text),
        'active' => 'historical',
        'until' => $date_until,
        'last_updated' => $today,
        'last_change' => $date_until,
      );
      scraperwiki::save_sqlite(array('org_id','since','text'),$data);
    } else {
      $last_text = $s->innertext;
    }
  }

}

function months($m) {
  switch($m) {
    case 'ledna': return '1';
    case 'února': return '2';
    case 'března': return '3';
    case 'dubna': return '4';
    case 'května': return '5';
    case 'června': return '6';
    case 'července': return '7';
    case 'srpna': return '8';
    case 'září': return '9';
    case 'října': return '10';
    case 'listopadu': return '11';
    case 'prosince': return '12';
  }
}

function n2($n){
  if ($n<10) return '0'.$n;
  else return $n;
}

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
