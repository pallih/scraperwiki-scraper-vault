<?php

//downloader of all result tables from volby.cz (using cz_volbycz_3)

require 'scraperwiki/simple_html_dom.php';

$last_type_code = '!';
$last_type_subcode = '!';
$last_year = '!';
$last_subyear = '!';
$last_region_code = '!';

scraperwiki::attach("cz_volbycz_2", "src2");
$rows_2 = scraperwiki::select("* from src2.swdata order by type_code,type_subcode,year,subyear");

foreach($rows_2 as $row_2) {

if ($last_type_code == '!') $ltc = 'cnr1990';
else $ltc = $last_type_code;

scraperwiki::attach("cz_volbycz_3", "src3");
$rows = scraperwiki::select("* from src3.swdata where type_code='{$ltc}' order by type_code,type_subcode,year,subyear,region_code");

//last vars - bug in scraperwiki
/*
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_code'");
$last_type_code =  $tmp[0]['value_blob'];
//$last_type_code = scraperwiki::get_var('last_type_code','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_subcode'");
$last_type_subcode =  $tmp[0]['value_blob'];
//$last_type_subcode = scraperwiki::get_var('last_type_subcode','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_year'");
$last_year =  $tmp[0]['value_blob'];
//$last_year = scraperwiki::get_var('last_year','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_subyear'");
$last_subyear =  $tmp[0]['value_blob'];
//$last_subyear = scraperwiki::get_var('last_subyear','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_region_code'");
$last_region_code =  $tmp[0]['value_blob'];
//$region_code = scraperwiki::get_var('last_region_code','!');
*/


echo '++';

foreach ($rows as $row) {
  //skip rows that are already done
  if (strcmp($row['type_code'],$last_type_code) < 0) continue;
    if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) < 0)) continue;
      if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) < 0)) continue;
        if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) < 0)) continue;
            if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) == 0) and (strcmp($row['region_code'],$last_region_code) <= 0) ) continue;


    //download page
    $url = 'http://volby.cz' . $row['link'];

echo '**' . $url . "**\n";
    $html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));

    //desirable page cannot not contain: 'xokres=1' and 'xokrsek=2', etc. or 'xobvod=1' and 'xobvod=2', etc.
    //otherwise it has to download the detailed pages
    $okres = array();
    preg_match_all('/xokrsek=([0-9]{1,})/',$html,$matches1);
    preg_match_all('/xobvod=([0-9]{1,})/',$html,$matches2);
//print_r($matches1);die();
    if (  (count($matches1) > 0) and (count($matches1[0]) > 0) ) {
      foreach ($matches1[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (  (count($matches2) > 0) and (count($matches2[0]) > 0) ) {
      foreach ($matches2[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (count($m) < 1) { //it is a desirable page
      savepage($row,$html,$url);
    } else { //it is not a desirable page, we have to go deeper
        $dom = new simple_html_dom();
        $dom->load($html);
        $tds = $dom->find('td');
        if (count($tds) > 0) {
            foreach ($tds as $td) {
                //is it a cell with link to desirable page?
                if ((strpos($td->innertext,'xokrsek=') > 0) or ((strpos($td->innertext,'xobvod=') > 0))) {
                    $tmp = explode('/',$row['link']);
                    array_pop($tmp);
                    $new_link = implode('/',$tmp) . '/' . html_entity_decode($td->find('a',0)->href);
                    $okrsek = $td->plaintext;
                    $new_url = 'http://volby.cz' . $new_link;
                    $new_html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($new_url)));
                    savepage($row,$new_html,$new_url,$okrsek);
                }
            }
        }
    }

  

  //save info about last row
  scraperwiki::save_var('last_type_code',$row['type_code']);
  scraperwiki::save_var('last_type_subcode',$row['type_subcode']);
  scraperwiki::save_var('last_year',$row['year']);
  scraperwiki::save_var('last_subyear',$row['subyear']);
  scraperwiki::save_var('last_region_code',$row['region_code']);
}

scraperwiki::save_var('last_type_code','!');
scraperwiki::save_var('last_type_subcode','!');
scraperwiki::save_var('last_year','!');
scraperwiki::save_var('last_subyear','!');
scraperwiki::save_var('last_region_code','!');

}

function savepage($row,$html,$url,$okrsek = 0) {
  $data = $row;
  $data['html'] = $html;
  $data['url'] = $url;
  $data['okrsek'] = $okrsek;

  scraperwiki::save_sqlite(array('type_code', 'type_subcode', 'year', 'subyear', 'region_code', 'okrsek'), $data);
}



?>
<?php

//downloader of all result tables from volby.cz (using cz_volbycz_3)

require 'scraperwiki/simple_html_dom.php';

$last_type_code = '!';
$last_type_subcode = '!';
$last_year = '!';
$last_subyear = '!';
$last_region_code = '!';

scraperwiki::attach("cz_volbycz_2", "src2");
$rows_2 = scraperwiki::select("* from src2.swdata order by type_code,type_subcode,year,subyear");

foreach($rows_2 as $row_2) {

if ($last_type_code == '!') $ltc = 'cnr1990';
else $ltc = $last_type_code;

scraperwiki::attach("cz_volbycz_3", "src3");
$rows = scraperwiki::select("* from src3.swdata where type_code='{$ltc}' order by type_code,type_subcode,year,subyear,region_code");

//last vars - bug in scraperwiki
/*
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_code'");
$last_type_code =  $tmp[0]['value_blob'];
//$last_type_code = scraperwiki::get_var('last_type_code','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_subcode'");
$last_type_subcode =  $tmp[0]['value_blob'];
//$last_type_subcode = scraperwiki::get_var('last_type_subcode','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_year'");
$last_year =  $tmp[0]['value_blob'];
//$last_year = scraperwiki::get_var('last_year','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_subyear'");
$last_subyear =  $tmp[0]['value_blob'];
//$last_subyear = scraperwiki::get_var('last_subyear','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_region_code'");
$last_region_code =  $tmp[0]['value_blob'];
//$region_code = scraperwiki::get_var('last_region_code','!');
*/


echo '++';

foreach ($rows as $row) {
  //skip rows that are already done
  if (strcmp($row['type_code'],$last_type_code) < 0) continue;
    if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) < 0)) continue;
      if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) < 0)) continue;
        if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) < 0)) continue;
            if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) == 0) and (strcmp($row['region_code'],$last_region_code) <= 0) ) continue;


    //download page
    $url = 'http://volby.cz' . $row['link'];

echo '**' . $url . "**\n";
    $html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));

    //desirable page cannot not contain: 'xokres=1' and 'xokrsek=2', etc. or 'xobvod=1' and 'xobvod=2', etc.
    //otherwise it has to download the detailed pages
    $okres = array();
    preg_match_all('/xokrsek=([0-9]{1,})/',$html,$matches1);
    preg_match_all('/xobvod=([0-9]{1,})/',$html,$matches2);
//print_r($matches1);die();
    if (  (count($matches1) > 0) and (count($matches1[0]) > 0) ) {
      foreach ($matches1[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (  (count($matches2) > 0) and (count($matches2[0]) > 0) ) {
      foreach ($matches2[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (count($m) < 1) { //it is a desirable page
      savepage($row,$html,$url);
    } else { //it is not a desirable page, we have to go deeper
        $dom = new simple_html_dom();
        $dom->load($html);
        $tds = $dom->find('td');
        if (count($tds) > 0) {
            foreach ($tds as $td) {
                //is it a cell with link to desirable page?
                if ((strpos($td->innertext,'xokrsek=') > 0) or ((strpos($td->innertext,'xobvod=') > 0))) {
                    $tmp = explode('/',$row['link']);
                    array_pop($tmp);
                    $new_link = implode('/',$tmp) . '/' . html_entity_decode($td->find('a',0)->href);
                    $okrsek = $td->plaintext;
                    $new_url = 'http://volby.cz' . $new_link;
                    $new_html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($new_url)));
                    savepage($row,$new_html,$new_url,$okrsek);
                }
            }
        }
    }

  

  //save info about last row
  scraperwiki::save_var('last_type_code',$row['type_code']);
  scraperwiki::save_var('last_type_subcode',$row['type_subcode']);
  scraperwiki::save_var('last_year',$row['year']);
  scraperwiki::save_var('last_subyear',$row['subyear']);
  scraperwiki::save_var('last_region_code',$row['region_code']);
}

scraperwiki::save_var('last_type_code','!');
scraperwiki::save_var('last_type_subcode','!');
scraperwiki::save_var('last_year','!');
scraperwiki::save_var('last_subyear','!');
scraperwiki::save_var('last_region_code','!');

}

function savepage($row,$html,$url,$okrsek = 0) {
  $data = $row;
  $data['html'] = $html;
  $data['url'] = $url;
  $data['okrsek'] = $okrsek;

  scraperwiki::save_sqlite(array('type_code', 'type_subcode', 'year', 'subyear', 'region_code', 'okrsek'), $data);
}



?>
<?php

//downloader of all result tables from volby.cz (using cz_volbycz_3)

require 'scraperwiki/simple_html_dom.php';

$last_type_code = '!';
$last_type_subcode = '!';
$last_year = '!';
$last_subyear = '!';
$last_region_code = '!';

scraperwiki::attach("cz_volbycz_2", "src2");
$rows_2 = scraperwiki::select("* from src2.swdata order by type_code,type_subcode,year,subyear");

foreach($rows_2 as $row_2) {

if ($last_type_code == '!') $ltc = 'cnr1990';
else $ltc = $last_type_code;

scraperwiki::attach("cz_volbycz_3", "src3");
$rows = scraperwiki::select("* from src3.swdata where type_code='{$ltc}' order by type_code,type_subcode,year,subyear,region_code");

//last vars - bug in scraperwiki
/*
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_code'");
$last_type_code =  $tmp[0]['value_blob'];
//$last_type_code = scraperwiki::get_var('last_type_code','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_type_subcode'");
$last_type_subcode =  $tmp[0]['value_blob'];
//$last_type_subcode = scraperwiki::get_var('last_type_subcode','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_year'");
$last_year =  $tmp[0]['value_blob'];
//$last_year = scraperwiki::get_var('last_year','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_subyear'");
$last_subyear =  $tmp[0]['value_blob'];
//$last_subyear = scraperwiki::get_var('last_subyear','!');
$tmp = scraperwiki::select("value_blob from swvariables where name='last_region_code'");
$last_region_code =  $tmp[0]['value_blob'];
//$region_code = scraperwiki::get_var('last_region_code','!');
*/


echo '++';

foreach ($rows as $row) {
  //skip rows that are already done
  if (strcmp($row['type_code'],$last_type_code) < 0) continue;
    if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) < 0)) continue;
      if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) < 0)) continue;
        if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) < 0)) continue;
            if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) == 0) and (strcmp($row['region_code'],$last_region_code) <= 0) ) continue;


    //download page
    $url = 'http://volby.cz' . $row['link'];

echo '**' . $url . "**\n";
    $html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));

    //desirable page cannot not contain: 'xokres=1' and 'xokrsek=2', etc. or 'xobvod=1' and 'xobvod=2', etc.
    //otherwise it has to download the detailed pages
    $okres = array();
    preg_match_all('/xokrsek=([0-9]{1,})/',$html,$matches1);
    preg_match_all('/xobvod=([0-9]{1,})/',$html,$matches2);
//print_r($matches1);die();
    if (  (count($matches1) > 0) and (count($matches1[0]) > 0) ) {
      foreach ($matches1[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (  (count($matches2) > 0) and (count($matches2[0]) > 0) ) {
      foreach ($matches2[0] as $m) {
        $okrsek[$m[1]] = true;
      }
    }
    if (count($m) < 1) { //it is a desirable page
      savepage($row,$html,$url);
    } else { //it is not a desirable page, we have to go deeper
        $dom = new simple_html_dom();
        $dom->load($html);
        $tds = $dom->find('td');
        if (count($tds) > 0) {
            foreach ($tds as $td) {
                //is it a cell with link to desirable page?
                if ((strpos($td->innertext,'xokrsek=') > 0) or ((strpos($td->innertext,'xobvod=') > 0))) {
                    $tmp = explode('/',$row['link']);
                    array_pop($tmp);
                    $new_link = implode('/',$tmp) . '/' . html_entity_decode($td->find('a',0)->href);
                    $okrsek = $td->plaintext;
                    $new_url = 'http://volby.cz' . $new_link;
                    $new_html = str_replace('&nbsp;',' ',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($new_url)));
                    savepage($row,$new_html,$new_url,$okrsek);
                }
            }
        }
    }

  

  //save info about last row
  scraperwiki::save_var('last_type_code',$row['type_code']);
  scraperwiki::save_var('last_type_subcode',$row['type_subcode']);
  scraperwiki::save_var('last_year',$row['year']);
  scraperwiki::save_var('last_subyear',$row['subyear']);
  scraperwiki::save_var('last_region_code',$row['region_code']);
}

scraperwiki::save_var('last_type_code','!');
scraperwiki::save_var('last_type_subcode','!');
scraperwiki::save_var('last_year','!');
scraperwiki::save_var('last_subyear','!');
scraperwiki::save_var('last_region_code','!');

}

function savepage($row,$html,$url,$okrsek = 0) {
  $data = $row;
  $data['html'] = $html;
  $data['url'] = $url;
  $data['okrsek'] = $okrsek;

  scraperwiki::save_sqlite(array('type_code', 'type_subcode', 'year', 'subyear', 'region_code', 'okrsek'), $data);
}



?>
