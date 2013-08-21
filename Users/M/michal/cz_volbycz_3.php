<?php
$v = scraperwiki::get_var('last_type_code','!');
print $v . "\n";

//from CZ volby.cz 2 to list of okrseks

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_2", "src");
$rows = scraperwiki::select("* from src.swdata order by type_code,type_subcode,year,subyear");



//print_r($rows);

foreach ($rows as $row) {
//last vars
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

/*$last_type_code = 'cnr1990';
$last_type_subcode = '-';
$last_year = '1990';
$last_subyear = '1';*/

  $regions = array();
echo $row['type_code'].'*'.$last_type_code . '*' . strcmp($row['type_code'],$last_type_code) . "*\n";
  if (strcmp($row['type_code'],$last_type_code) < 0) continue;
    if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) < 0)) continue;
      if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) < 0)) continue;
        if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) <= 0)) continue;

//temp correction
/*$row = array(
  'link' => '/pls/senat/se2?xjazyk=CZ&xdatum=19981114',
  'type_code' => 'senat',
  'year' => '1998',
  'subyear' => '1',
  'type_subcode'=> '19981114'
);*/

//print_r($row);    
    $regions = one_page($row['link'],$row['type_code'],$row['type_subcode'],$row['year'],$row['subyear']);
    $obce = array();
    foreach($regions as $region) { //in one (type,year)
print_r($region);
      //$tmp = explode('/',$row['link']);
      //array_pop($tmp);
      $link = $region['link'];
      $obce[] = one_page($link,$row['type_code'],$row['type_subcode'],$row['year'],$row['subyear'],$region['region'],$region['region_code']);
//print_r($obce);die();
    }
    foreach ($obce as $o) {
//print_r($o);die();
      scraperwiki::save_sqlite(array('type_code', 'type_subcode', 'year', 'subyear', 'region_code'),$o);
    }
//die();

  scraperwiki::save_var('last_type_code',$row['type_code']);
  scraperwiki::save_var('last_type_subcode',$row['type_subcode']);
  scraperwiki::save_var('last_year',$row['year']);
  scraperwiki::save_var('last_subyear',$row['subyear']);
}

scraperwiki::save_var('last_type_code','!');
scraperwiki::save_var('last_type_subcode','!');
scraperwiki::save_var('last_year','!');
scraperwiki::save_var('last_subyear','!');



function one_page($link,$type_code,$type_subcode,$year,$subyear,$supregion = '',$supregion_code = '') {
    $data = array();
    $url = 'http://volby.cz' . $link;
//echo '**' . $url . "**\n";
    $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
    //correct errors in html
    $html = str_replace('</td><tr>','</td><tr><td>',str_replace('</TD><TR>','</TD></TR><TR>',str_replace("\n",'',$html)));

    $dom = new simple_html_dom();
    $dom->load($html);

    if (count($dom->find('table table')) > 0)  {
      $doms = $dom->find('table table');
    } else {
      $doms[0] = $dom;
    }
    foreach ($doms as $dom) {
//echo $dom->outertext;    
        $trs = $dom->find('tr');
        foreach ($trs as $tr) {
          $tds = $tr->find('td');
            
          //kv1994 and kv1998 have different structure!
          if ((($type_code == 'kv1994') or ($type_code == 'kv1998')) and ($supregion != '')) {
            //is it a row with link to obce?
            if ((count($tds)>0) and (strpos($tds[0]->innertext,'xobec=') > 0)) {
                $code = $tds[0]->plaintext;
                $region = $tds[1]->plaintext;
                $tmp = explode('/',$link);
                array_pop($tmp);

                //is a row with 'X' link ?
                if (trim($tds[count($tds)-1]->plaintext) == 'X') {
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[count($tds)-1]->find('a',0)->href);
                } else {
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[0]->find('a',0)->href);
                }
                $data[] = array(
                      'region_code' => $code,
                      'region' => $region,
                      'link' => $link,
                      'type_code' => $type_code,
                      'type_subcode' => $type_subcode,
                      'year' => $year,
                      'subyear' => $subyear,
                      'supregion' => $supregion,
                      'supregion_code' => $supregion_code,
                 );

            }
          } else {

              //is it a row with link to obce?
              if ((count($tds)>0) and (trim($tds[count($tds)-1]->plaintext) == 'X')) {
//echo '**' . count($tds) . "**\n";
                
                $tmp = explode('/',$link);
                array_pop($tmp);
                //$type_code=ps2002 has different structure of tables
                
                if (($type_code == 'ps2002') and ($supregion != '')) {
                  for ($exc = 0; $exc <= 4; $exc = $exc + 4) {
                    if (strlen($tds[$exc]) > 2) {
                      $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[2+$exc]->find('a',0)->href);
                      $region = $tds[1+$exc]->plaintext;
                      $code = $tds[0+$exc]->plaintext;
                      $data[] = array(
                        'region_code' => $code,
                        'region' => $region,
                        'link' => $link,
                        'type_code' => $type_code,
                        'type_subcode' => $type_subcode,
                        'year' => $year,
                        'subyear' => $subyear,
                        'supregion' => $supregion,
                        'supregion_code' => $supregion_code,
                      );
                    }
                  }
    
                } else {//it is not ps2002
                    $code = $tds[0]->plaintext;
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[count($tds)-1]->find('a',0)->href);
                    $region = $tds[1]->plaintext;
//echo $region.$link."\n";
                    $data[] = array(
                      'region_code' => $code,
                      'region' => $region,
                      'link' => $link,
                      'type_code' => $type_code,
                      'type_subcode' => $type_subcode,
                      'year' => $year,
                      'subyear' => $subyear,
                      'supregion' => $supregion,
                      'supregion_code' => $supregion_code,
                    );
                }
              }
           } //kv1994,kv1998 vs. rest
        }
    }
return $data;
}

?><?php
$v = scraperwiki::get_var('last_type_code','!');
print $v . "\n";

//from CZ volby.cz 2 to list of okrseks

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_2", "src");
$rows = scraperwiki::select("* from src.swdata order by type_code,type_subcode,year,subyear");



//print_r($rows);

foreach ($rows as $row) {
//last vars
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

/*$last_type_code = 'cnr1990';
$last_type_subcode = '-';
$last_year = '1990';
$last_subyear = '1';*/

  $regions = array();
echo $row['type_code'].'*'.$last_type_code . '*' . strcmp($row['type_code'],$last_type_code) . "*\n";
  if (strcmp($row['type_code'],$last_type_code) < 0) continue;
    if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) < 0)) continue;
      if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) < 0)) continue;
        if ((strcmp($row['type_code'],$last_type_code) == 0) and (strcmp($row['type_subcode'],$last_type_subcode) == 0) and (strcmp($row['year'],$last_year) == 0) and (strcmp($row['subyear'],$last_subyear) <= 0)) continue;

//temp correction
/*$row = array(
  'link' => '/pls/senat/se2?xjazyk=CZ&xdatum=19981114',
  'type_code' => 'senat',
  'year' => '1998',
  'subyear' => '1',
  'type_subcode'=> '19981114'
);*/

//print_r($row);    
    $regions = one_page($row['link'],$row['type_code'],$row['type_subcode'],$row['year'],$row['subyear']);
    $obce = array();
    foreach($regions as $region) { //in one (type,year)
print_r($region);
      //$tmp = explode('/',$row['link']);
      //array_pop($tmp);
      $link = $region['link'];
      $obce[] = one_page($link,$row['type_code'],$row['type_subcode'],$row['year'],$row['subyear'],$region['region'],$region['region_code']);
//print_r($obce);die();
    }
    foreach ($obce as $o) {
//print_r($o);die();
      scraperwiki::save_sqlite(array('type_code', 'type_subcode', 'year', 'subyear', 'region_code'),$o);
    }
//die();

  scraperwiki::save_var('last_type_code',$row['type_code']);
  scraperwiki::save_var('last_type_subcode',$row['type_subcode']);
  scraperwiki::save_var('last_year',$row['year']);
  scraperwiki::save_var('last_subyear',$row['subyear']);
}

scraperwiki::save_var('last_type_code','!');
scraperwiki::save_var('last_type_subcode','!');
scraperwiki::save_var('last_year','!');
scraperwiki::save_var('last_subyear','!');



function one_page($link,$type_code,$type_subcode,$year,$subyear,$supregion = '',$supregion_code = '') {
    $data = array();
    $url = 'http://volby.cz' . $link;
//echo '**' . $url . "**\n";
    $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
    //correct errors in html
    $html = str_replace('</td><tr>','</td><tr><td>',str_replace('</TD><TR>','</TD></TR><TR>',str_replace("\n",'',$html)));

    $dom = new simple_html_dom();
    $dom->load($html);

    if (count($dom->find('table table')) > 0)  {
      $doms = $dom->find('table table');
    } else {
      $doms[0] = $dom;
    }
    foreach ($doms as $dom) {
//echo $dom->outertext;    
        $trs = $dom->find('tr');
        foreach ($trs as $tr) {
          $tds = $tr->find('td');
            
          //kv1994 and kv1998 have different structure!
          if ((($type_code == 'kv1994') or ($type_code == 'kv1998')) and ($supregion != '')) {
            //is it a row with link to obce?
            if ((count($tds)>0) and (strpos($tds[0]->innertext,'xobec=') > 0)) {
                $code = $tds[0]->plaintext;
                $region = $tds[1]->plaintext;
                $tmp = explode('/',$link);
                array_pop($tmp);

                //is a row with 'X' link ?
                if (trim($tds[count($tds)-1]->plaintext) == 'X') {
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[count($tds)-1]->find('a',0)->href);
                } else {
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[0]->find('a',0)->href);
                }
                $data[] = array(
                      'region_code' => $code,
                      'region' => $region,
                      'link' => $link,
                      'type_code' => $type_code,
                      'type_subcode' => $type_subcode,
                      'year' => $year,
                      'subyear' => $subyear,
                      'supregion' => $supregion,
                      'supregion_code' => $supregion_code,
                 );

            }
          } else {

              //is it a row with link to obce?
              if ((count($tds)>0) and (trim($tds[count($tds)-1]->plaintext) == 'X')) {
//echo '**' . count($tds) . "**\n";
                
                $tmp = explode('/',$link);
                array_pop($tmp);
                //$type_code=ps2002 has different structure of tables
                
                if (($type_code == 'ps2002') and ($supregion != '')) {
                  for ($exc = 0; $exc <= 4; $exc = $exc + 4) {
                    if (strlen($tds[$exc]) > 2) {
                      $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[2+$exc]->find('a',0)->href);
                      $region = $tds[1+$exc]->plaintext;
                      $code = $tds[0+$exc]->plaintext;
                      $data[] = array(
                        'region_code' => $code,
                        'region' => $region,
                        'link' => $link,
                        'type_code' => $type_code,
                        'type_subcode' => $type_subcode,
                        'year' => $year,
                        'subyear' => $subyear,
                        'supregion' => $supregion,
                        'supregion_code' => $supregion_code,
                      );
                    }
                  }
    
                } else {//it is not ps2002
                    $code = $tds[0]->plaintext;
                    $link = html_entity_decode(implode('/',$tmp) . '/' . $tds[count($tds)-1]->find('a',0)->href);
                    $region = $tds[1]->plaintext;
//echo $region.$link."\n";
                    $data[] = array(
                      'region_code' => $code,
                      'region' => $region,
                      'link' => $link,
                      'type_code' => $type_code,
                      'type_subcode' => $type_subcode,
                      'year' => $year,
                      'subyear' => $subyear,
                      'supregion' => $supregion,
                      'supregion_code' => $supregion_code,
                    );
                }
              }
           } //kv1994,kv1998 vs. rest
        }
    }
return $data;
}

?>