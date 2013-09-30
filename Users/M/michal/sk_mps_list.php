<?php

// source: http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=1 (.. 5)
// problem: current term does not have all the MPs, only current ones

scraperwiki::sqliteexecute("create table if not exists swdata (`id` int, `term` int, `name` string)"); 
scraperwiki::sqlitecommit();

//delete last term mps
$max_ar = scraperwiki::select("max(term) as max from swdata");
$max_term = $max_ar[0]['max'];
scraperwiki::sqliteexecute("delete from swdata where term='{$max_term}'");
scraperwiki::sqlitecommit();

require 'scraperwiki/simple_html_dom.php'; 

$continue = true;
$i = 1;
while ($continue) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //mps list
  $block = $dom->find('div[class=mps_list]');
  
  if (trim($block[0]->plaintext) == '') $continue = false;
  else {
      //mps
      $mps = $block[0]->find('a[href]');
      $data = array();
      foreach ($mps as $mp) {
        $name = $mp->plaintext;
        if ($name != '&uarr;') {
            $link = $mp->href;
            preg_match('/PoslanecID=([0-9]{1,})/',$link,$matches);
            $id = $matches[1];
            $data[] = array(
              'term' => $i,
              'id' => $id,
              'name' =>$mp->plaintext,
            );
        }
      }
      scraperwiki::save_sqlite(array('term','id'),$data);
      $i++;
  }
}
?>
<?php

// source: http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=1 (.. 5)
// problem: current term does not have all the MPs, only current ones

scraperwiki::sqliteexecute("create table if not exists swdata (`id` int, `term` int, `name` string)"); 
scraperwiki::sqlitecommit();

//delete last term mps
$max_ar = scraperwiki::select("max(term) as max from swdata");
$max_term = $max_ar[0]['max'];
scraperwiki::sqliteexecute("delete from swdata where term='{$max_term}'");
scraperwiki::sqlitecommit();

require 'scraperwiki/simple_html_dom.php'; 

$continue = true;
$i = 1;
while ($continue) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //mps list
  $block = $dom->find('div[class=mps_list]');
  
  if (trim($block[0]->plaintext) == '') $continue = false;
  else {
      //mps
      $mps = $block[0]->find('a[href]');
      $data = array();
      foreach ($mps as $mp) {
        $name = $mp->plaintext;
        if ($name != '&uarr;') {
            $link = $mp->href;
            preg_match('/PoslanecID=([0-9]{1,})/',$link,$matches);
            $id = $matches[1];
            $data[] = array(
              'term' => $i,
              'id' => $id,
              'name' =>$mp->plaintext,
            );
        }
      }
      scraperwiki::save_sqlite(array('term','id'),$data);
      $i++;
  }
}
?>
<?php

// source: http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=1 (.. 5)
// problem: current term does not have all the MPs, only current ones

scraperwiki::sqliteexecute("create table if not exists swdata (`id` int, `term` int, `name` string)"); 
scraperwiki::sqlitecommit();

//delete last term mps
$max_ar = scraperwiki::select("max(term) as max from swdata");
$max_term = $max_ar[0]['max'];
scraperwiki::sqliteexecute("delete from swdata where term='{$max_term}'");
scraperwiki::sqlitecommit();

require 'scraperwiki/simple_html_dom.php'; 

$continue = true;
$i = 1;
while ($continue) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //mps list
  $block = $dom->find('div[class=mps_list]');
  
  if (trim($block[0]->plaintext) == '') $continue = false;
  else {
      //mps
      $mps = $block[0]->find('a[href]');
      $data = array();
      foreach ($mps as $mp) {
        $name = $mp->plaintext;
        if ($name != '&uarr;') {
            $link = $mp->href;
            preg_match('/PoslanecID=([0-9]{1,})/',$link,$matches);
            $id = $matches[1];
            $data[] = array(
              'term' => $i,
              'id' => $id,
              'name' =>$mp->plaintext,
            );
        }
      }
      scraperwiki::save_sqlite(array('term','id'),$data);
      $i++;
  }
}
?>
<?php

// source: http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=1 (.. 5)
// problem: current term does not have all the MPs, only current ones

scraperwiki::sqliteexecute("create table if not exists swdata (`id` int, `term` int, `name` string)"); 
scraperwiki::sqlitecommit();

//delete last term mps
$max_ar = scraperwiki::select("max(term) as max from swdata");
$max_term = $max_ar[0]['max'];
scraperwiki::sqliteexecute("delete from swdata where term='{$max_term}'");
scraperwiki::sqlitecommit();

require 'scraperwiki/simple_html_dom.php'; 

$continue = true;
$i = 1;
while ($continue) {
  $url = "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/zoznam_abc&ListType=0&CisObdobia=" . $i;
  $html = scraperwiki::scrape($url);
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //mps list
  $block = $dom->find('div[class=mps_list]');
  
  if (trim($block[0]->plaintext) == '') $continue = false;
  else {
      //mps
      $mps = $block[0]->find('a[href]');
      $data = array();
      foreach ($mps as $mp) {
        $name = $mp->plaintext;
        if ($name != '&uarr;') {
            $link = $mp->href;
            preg_match('/PoslanecID=([0-9]{1,})/',$link,$matches);
            $id = $matches[1];
            $data[] = array(
              'term' => $i,
              'id' => $id,
              'name' =>$mp->plaintext,
            );
        }
      }
      scraperwiki::save_sqlite(array('term','id'),$data);
      $i++;
  }
}
?>
