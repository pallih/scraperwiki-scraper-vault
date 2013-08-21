<?php

//use CZ volby.cz 1 to get all pages like 'http://volby.cz/pls/ps2010/ps3?xjazyk=CZ'

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_1", "src");
$rows = scraperwiki::select("* from src.swdata");

$data = array();

foreach ($rows as $row) {
  if (substr($row['link'],0,1) != '/') $row['link'] = '/' . $row['link'];
echo substr($row['link'],0,1);
  $url = 'http://volby.cz' . str_replace('&amp;','&',$row['link']);  //correction of &amp; from scraper 1
  $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
  $dom = new simple_html_dom();
  $dom->load($html);
echo $url . "\n";
  switch ($row['type']) { //Senat and Zastupitelstva obci have different format
    case 'Zastupitelstva obcí':
      if (strpos($row['link'],'xid=') > 0) {
        get_link($data,'Výsledky hlasování',$dom,$row['link'],$row['type'],$row['year'],1);
      } else { //we need go thru another page
        get_link_2($data,$dom,$row);
      }
      break;
    case 'Senát Parlamentu ČR':
      if (is_numeric($row['year'])) {
        $ok = get_link($data,'Výsledky hlasování',$dom,$row['link'],$row['type'],$row['year'],1);    
        if (!$ok) { //different page as in http://volby.cz/pls/senat/serok?xjazyk=CZ&xrok=2003, we need to go thru different page
            get_link_3($data,$dom,$row);
        }
      }    
      break;
    default: //all others are the same
      get_link($data,'Výsledky hlasování za územní celky',$dom,$row['link'],$row['type'],$row['year'],1);

  }
}
scraperwiki::save_sqlite(array('type_code','type_subcode','year','subyear'),$data);

function get_link_3(&$data,$dom,$row) {
  $i = 1; // for dinstinction of two different elections during a year in the senate
  $as = $dom->find('a');
  foreach ($as as $a) {
    if (strpos($a->href,'xdatum') > 0) {
      $tmp = explode('/',$row['link']);
      array_pop($tmp);
      $url2 = 'http://volby.cz' . str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      $html2 = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url2)));
      $dom2 = new simple_html_dom();
      $dom2->load($html2);
      get_link($data,'Výsledky hlasování',$dom2,$row['link'],$row['type'],$row['year'],$i);  
      get_link($data,'Výsledky voleb &ndash; výběr obce dle území',$dom2,$row['link'],$row['type'],$row['year'],$i);  
      $i++;  
    }
  }
}

function get_link_2(&$data,$dom,$row) {
  $as = $dom->find('a');
  foreach ($as as $a) {
    if (strpos($a->href,'xid=0') > 0) {
      $tmp = explode('/',$row['link']);
      array_pop($tmp);
      $url2 = 'http://volby.cz' . str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      $html2 = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url2)));
      $dom2 = new simple_html_dom();
      $dom2->load($html2);
      get_link($data,'Výsledky hlasování',$dom2,$row['link'],$row['type'],$row['year'],1);
      get_link($data,'Výsledky voleb &ndash; výběr obce dle území',$dom2,$row['link'],$row['type'],$row['year'],1);
    }
  }  
}
//link, year, subyear, type
function get_link(&$data, $text, $dom, $link, $type, $year, $subyear) {
  $as = $dom->find('a');
  foreach ($as as $a) {
    if ($a->plaintext == $text) {
      if ($link[0] != '/') $link = '/' . $link;
      $tmp = explode('/',$link);
      array_pop($tmp);
      $new_link = str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      if ($new_link[0] != '/') $new_link = '/' . $new_link;
      $type_code = $tmp[2];
      if ($type_code == 'senat') {
        preg_match('/xdatum=([0-9]{1,})/',$link,$matches);
        if (isset($matches[1]))
          $type_subcode = $matches[1];
        else
          $type_subcode = '-';
      } else
        $type_subcode = '-';
      $data[] = array(
        'type' => $type,
        'year' => $year,
        'subyear' => $subyear,
        'type_code' => $type_code,
        'type_subcode' => $type_subcode,
        'link' => $new_link,
      );
      return true;
    }
  }
}

?><?php

//use CZ volby.cz 1 to get all pages like 'http://volby.cz/pls/ps2010/ps3?xjazyk=CZ'

require 'scraperwiki/simple_html_dom.php';

scraperwiki::attach("cz_volbycz_1", "src");
$rows = scraperwiki::select("* from src.swdata");

$data = array();

foreach ($rows as $row) {
  if (substr($row['link'],0,1) != '/') $row['link'] = '/' . $row['link'];
echo substr($row['link'],0,1);
  $url = 'http://volby.cz' . str_replace('&amp;','&',$row['link']);  //correction of &amp; from scraper 1
  $html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
  $dom = new simple_html_dom();
  $dom->load($html);
echo $url . "\n";
  switch ($row['type']) { //Senat and Zastupitelstva obci have different format
    case 'Zastupitelstva obcí':
      if (strpos($row['link'],'xid=') > 0) {
        get_link($data,'Výsledky hlasování',$dom,$row['link'],$row['type'],$row['year'],1);
      } else { //we need go thru another page
        get_link_2($data,$dom,$row);
      }
      break;
    case 'Senát Parlamentu ČR':
      if (is_numeric($row['year'])) {
        $ok = get_link($data,'Výsledky hlasování',$dom,$row['link'],$row['type'],$row['year'],1);    
        if (!$ok) { //different page as in http://volby.cz/pls/senat/serok?xjazyk=CZ&xrok=2003, we need to go thru different page
            get_link_3($data,$dom,$row);
        }
      }    
      break;
    default: //all others are the same
      get_link($data,'Výsledky hlasování za územní celky',$dom,$row['link'],$row['type'],$row['year'],1);

  }
}
scraperwiki::save_sqlite(array('type_code','type_subcode','year','subyear'),$data);

function get_link_3(&$data,$dom,$row) {
  $i = 1; // for dinstinction of two different elections during a year in the senate
  $as = $dom->find('a');
  foreach ($as as $a) {
    if (strpos($a->href,'xdatum') > 0) {
      $tmp = explode('/',$row['link']);
      array_pop($tmp);
      $url2 = 'http://volby.cz' . str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      $html2 = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url2)));
      $dom2 = new simple_html_dom();
      $dom2->load($html2);
      get_link($data,'Výsledky hlasování',$dom2,$row['link'],$row['type'],$row['year'],$i);  
      get_link($data,'Výsledky voleb &ndash; výběr obce dle území',$dom2,$row['link'],$row['type'],$row['year'],$i);  
      $i++;  
    }
  }
}

function get_link_2(&$data,$dom,$row) {
  $as = $dom->find('a');
  foreach ($as as $a) {
    if (strpos($a->href,'xid=0') > 0) {
      $tmp = explode('/',$row['link']);
      array_pop($tmp);
      $url2 = 'http://volby.cz' . str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      $html2 = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url2)));
      $dom2 = new simple_html_dom();
      $dom2->load($html2);
      get_link($data,'Výsledky hlasování',$dom2,$row['link'],$row['type'],$row['year'],1);
      get_link($data,'Výsledky voleb &ndash; výběr obce dle území',$dom2,$row['link'],$row['type'],$row['year'],1);
    }
  }  
}
//link, year, subyear, type
function get_link(&$data, $text, $dom, $link, $type, $year, $subyear) {
  $as = $dom->find('a');
  foreach ($as as $a) {
    if ($a->plaintext == $text) {
      if ($link[0] != '/') $link = '/' . $link;
      $tmp = explode('/',$link);
      array_pop($tmp);
      $new_link = str_replace('&amp;','&',implode('/',$tmp) . '/' . $a->href);
      if ($new_link[0] != '/') $new_link = '/' . $new_link;
      $type_code = $tmp[2];
      if ($type_code == 'senat') {
        preg_match('/xdatum=([0-9]{1,})/',$link,$matches);
        if (isset($matches[1]))
          $type_subcode = $matches[1];
        else
          $type_subcode = '-';
      } else
        $type_subcode = '-';
      $data[] = array(
        'type' => $type,
        'year' => $year,
        'subyear' => $subyear,
        'type_code' => $type_code,
        'type_subcode' => $type_subcode,
        'link' => $new_link,
      );
      return true;
    }
  }
}

?>