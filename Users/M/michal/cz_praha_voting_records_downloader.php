<?php

# for 2010-2014

require 'scraperwiki/simple_html_dom.php';

//temp:
//scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
//scraperwiki::sqlitecommit();
scraperwiki::save_sqlite(array('id'),array('id' => 0,'date' => '1977-01-01'),'session');

//download the overall tables and extract data

$url0 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=10&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting=&start=0";
$html0 = scraperwiki::scrape($url0);

$dom0 = new simple_html_dom();
$dom0->load($html0);

//meetings
$selects = $dom0->find("select[name=meeting]",0)->find("option");
array_shift($selects);

foreach ($selects as $select) {
  $s = array();
  $s['id'] = $select->value;
  $s['date'] = convert_date(get_first_string($select->plaintext,'(',')'));
//print_r($s);
  //is already in db?
  $c_ar = scraperwiki::select("count(*) as count from `session` where id='{$s['id']}'");
//print_r($c_ar);die();
  if ($c_ar[0]['count'] == 0) {
    $url1 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=500&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting={$s['id']}&start=0";  //500 is max
    $html1 = scraperwiki::scrape($url1);
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

    //check number of divisions
    $number = $dom1->find("div[class=pg-count]",0)->find('strong',0)->plaintext;
    if ($number > 500) {
      echo $url1 . "** has more than 500 divisions -> problem -> needs to solve pagination";
      die();
    }
    $trs = $dom1->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      $datum = array(
        'decision_number' => $tds[0]->plaintext,
        'date' => convert_date($tds[1]->plaintext),
        'document_number' => $tds[2]->plaintext,
        'name' => $tds[3]->plaintext,
        'passed' => $tds[4]->plaintext,
        'link' => htmlspecialchars_decode($tds[4]->find('a',0)->href),
      );
      $datum['id'] = get_first_string($datum['link'] . "&","votingId=","&");
      $url = "http://www.praha.eu" . $datum['link'];
      $html = scraperwiki::scrape($url);
      $dom = new simple_html_dom();
      $dom->load($html);

      $datum['html'] = '<h1>'.get_first_string($dom->innertext,'<h1>','</table>').'</table>';   

      $data[] = $datum;
    }
    //one session done:
    scraperwiki::save_sqlite(array('id'),$data,'division');
    scraperwiki::save_sqlite(array('id'),$s,'session');
  }
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

?>
<?php

# for 2010-2014

require 'scraperwiki/simple_html_dom.php';

//temp:
//scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
//scraperwiki::sqlitecommit();
scraperwiki::save_sqlite(array('id'),array('id' => 0,'date' => '1977-01-01'),'session');

//download the overall tables and extract data

$url0 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=10&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting=&start=0";
$html0 = scraperwiki::scrape($url0);

$dom0 = new simple_html_dom();
$dom0->load($html0);

//meetings
$selects = $dom0->find("select[name=meeting]",0)->find("option");
array_shift($selects);

foreach ($selects as $select) {
  $s = array();
  $s['id'] = $select->value;
  $s['date'] = convert_date(get_first_string($select->plaintext,'(',')'));
//print_r($s);
  //is already in db?
  $c_ar = scraperwiki::select("count(*) as count from `session` where id='{$s['id']}'");
//print_r($c_ar);die();
  if ($c_ar[0]['count'] == 0) {
    $url1 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=500&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting={$s['id']}&start=0";  //500 is max
    $html1 = scraperwiki::scrape($url1);
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

    //check number of divisions
    $number = $dom1->find("div[class=pg-count]",0)->find('strong',0)->plaintext;
    if ($number > 500) {
      echo $url1 . "** has more than 500 divisions -> problem -> needs to solve pagination";
      die();
    }
    $trs = $dom1->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      $datum = array(
        'decision_number' => $tds[0]->plaintext,
        'date' => convert_date($tds[1]->plaintext),
        'document_number' => $tds[2]->plaintext,
        'name' => $tds[3]->plaintext,
        'passed' => $tds[4]->plaintext,
        'link' => htmlspecialchars_decode($tds[4]->find('a',0)->href),
      );
      $datum['id'] = get_first_string($datum['link'] . "&","votingId=","&");
      $url = "http://www.praha.eu" . $datum['link'];
      $html = scraperwiki::scrape($url);
      $dom = new simple_html_dom();
      $dom->load($html);

      $datum['html'] = '<h1>'.get_first_string($dom->innertext,'<h1>','</table>').'</table>';   

      $data[] = $datum;
    }
    //one session done:
    scraperwiki::save_sqlite(array('id'),$data,'division');
    scraperwiki::save_sqlite(array('id'),$s,'session');
  }
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

?>
<?php

# for 2010-2014

require 'scraperwiki/simple_html_dom.php';

//temp:
//scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
//scraperwiki::sqlitecommit();
scraperwiki::save_sqlite(array('id'),array('id' => 0,'date' => '1977-01-01'),'session');

//download the overall tables and extract data

$url0 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=10&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting=&start=0";
$html0 = scraperwiki::scrape($url0);

$dom0 = new simple_html_dom();
$dom0->load($html0);

//meetings
$selects = $dom0->find("select[name=meeting]",0)->find("option");
array_shift($selects);

foreach ($selects as $select) {
  $s = array();
  $s['id'] = $select->value;
  $s['date'] = convert_date(get_first_string($select->plaintext,'(',')'));
//print_r($s);
  //is already in db?
  $c_ar = scraperwiki::select("count(*) as count from `session` where id='{$s['id']}'");
//print_r($c_ar);die();
  if ($c_ar[0]['count'] == 0) {
    $url1 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=500&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting={$s['id']}&start=0";  //500 is max
    $html1 = scraperwiki::scrape($url1);
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

    //check number of divisions
    $number = $dom1->find("div[class=pg-count]",0)->find('strong',0)->plaintext;
    if ($number > 500) {
      echo $url1 . "** has more than 500 divisions -> problem -> needs to solve pagination";
      die();
    }
    $trs = $dom1->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      $datum = array(
        'decision_number' => $tds[0]->plaintext,
        'date' => convert_date($tds[1]->plaintext),
        'document_number' => $tds[2]->plaintext,
        'name' => $tds[3]->plaintext,
        'passed' => $tds[4]->plaintext,
        'link' => htmlspecialchars_decode($tds[4]->find('a',0)->href),
      );
      $datum['id'] = get_first_string($datum['link'] . "&","votingId=","&");
      $url = "http://www.praha.eu" . $datum['link'];
      $html = scraperwiki::scrape($url);
      $dom = new simple_html_dom();
      $dom->load($html);

      $datum['html'] = '<h1>'.get_first_string($dom->innertext,'<h1>','</table>').'</table>';   

      $data[] = $datum;
    }
    //one session done:
    scraperwiki::save_sqlite(array('id'),$data,'division');
    scraperwiki::save_sqlite(array('id'),$s,'session');
  }
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

?>
<?php

# for 2010-2014

require 'scraperwiki/simple_html_dom.php';

//temp:
//scraperwiki::sqliteexecute("delete from `swdata` where town_code>'599999'");
//scraperwiki::sqlitecommit();
scraperwiki::save_sqlite(array('id'),array('id' => 0,'date' => '1977-01-01'),'session');

//download the overall tables and extract data

$url0 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=10&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting=&start=0";
$html0 = scraperwiki::scrape($url0);

$dom0 = new simple_html_dom();
$dom0->load($html0);

//meetings
$selects = $dom0->find("select[name=meeting]",0)->find("option");
array_shift($selects);

foreach ($selects as $select) {
  $s = array();
  $s['id'] = $select->value;
  $s['date'] = convert_date(get_first_string($select->plaintext,'(',')'));
//print_r($s);
  //is already in db?
  $c_ar = scraperwiki::select("count(*) as count from `session` where id='{$s['id']}'");
//print_r($c_ar);die();
  if ($c_ar[0]['count'] == 0) {
    $url1 = "http://www.praha.eu/jnp/cz/home/volene_organy/zastupitelstvo_hmp/hlasovani/index.html?size=500&periodId=18284&resolutionNumber=&printNumber=&s=1&meeting={$s['id']}&start=0";  //500 is max
    $html1 = scraperwiki::scrape($url1);
    $dom1 = new simple_html_dom();
    $dom1->load($html1);

    //check number of divisions
    $number = $dom1->find("div[class=pg-count]",0)->find('strong',0)->plaintext;
    if ($number > 500) {
      echo $url1 . "** has more than 500 divisions -> problem -> needs to solve pagination";
      die();
    }
    $trs = $dom1->find("table[class=data-grid]",0)->find("tr");
    array_shift($trs);
    $data = array();
    foreach ($trs as $tr) {
      $tds = $tr->find('td');
      $datum = array(
        'decision_number' => $tds[0]->plaintext,
        'date' => convert_date($tds[1]->plaintext),
        'document_number' => $tds[2]->plaintext,
        'name' => $tds[3]->plaintext,
        'passed' => $tds[4]->plaintext,
        'link' => htmlspecialchars_decode($tds[4]->find('a',0)->href),
      );
      $datum['id'] = get_first_string($datum['link'] . "&","votingId=","&");
      $url = "http://www.praha.eu" . $datum['link'];
      $html = scraperwiki::scrape($url);
      $dom = new simple_html_dom();
      $dom->load($html);

      $datum['html'] = '<h1>'.get_first_string($dom->innertext,'<h1>','</table>').'</table>';   

      $data[] = $datum;
    }
    //one session done:
    scraperwiki::save_sqlite(array('id'),$data,'division');
    scraperwiki::save_sqlite(array('id'),$s,'session');
  }
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

?>
