<?php

# Blank PHP
$urls = array('textile'=>'http://www.business-in-asia.com/vietnam/exporttextile.html');

foreach ($urls as $table=>$url) {
  # first time through, create tables and indices
  scraperwiki::sqliteexecute("drop table if exists $table");
 
  scraperwiki::sqliteexecute("create table $table (id INTEGER PRIMARY KEY, `name` string, address string, city string)");
  print '<pre>';
  $data = scraperWiki::scrape($url);
  if (preg_match_all('{<p>.*?</p>}ism', $data, $mm)) {
      foreach ($mm[0] as $m) {
         print_r($m); 
         $p = $m[0];
         $name = $addr = $city = '';
         if (preg_match('{name:(.*?)<br>}ism', $p, $mname)) {
            $name = strip_html($mname[1]);
            if (preg_match('{address:(.*?)<br>}ism', $p, $maddr)) {
               $addr = strip_html($maddr[1]);
            }
            printf("Inserting $name\n");
            scraperwiki::sqliteexecute("insert into $table values (?, ?,?,?)", 
               array(null, clean($name), clean($addr), ''));
         } else {
           printf("Can't find name: in $p\n");
         }
      }
  } else {
    die ("Can't parse addresses");
  }
  scraperwiki::sqlitecommit();
}

########################################
function strip_html($s) {
    $s = preg_replace('{,\s*}', ', ', $s);
    $s = preg_replace('{<.*?>}', '', $s);
    $s = preg_replace('{<.*$}', '', $s); // in case the string starts wtih an open tag, e.g. "click <a hre"
    return $s;
}

function clean($name) {
  return ucfirst(strtolower($name));
}


?>
<?php

# Blank PHP
$urls = array('textile'=>'http://www.business-in-asia.com/vietnam/exporttextile.html');

foreach ($urls as $table=>$url) {
  # first time through, create tables and indices
  scraperwiki::sqliteexecute("drop table if exists $table");
 
  scraperwiki::sqliteexecute("create table $table (id INTEGER PRIMARY KEY, `name` string, address string, city string)");
  print '<pre>';
  $data = scraperWiki::scrape($url);
  if (preg_match_all('{<p>.*?</p>}ism', $data, $mm)) {
      foreach ($mm[0] as $m) {
         print_r($m); 
         $p = $m[0];
         $name = $addr = $city = '';
         if (preg_match('{name:(.*?)<br>}ism', $p, $mname)) {
            $name = strip_html($mname[1]);
            if (preg_match('{address:(.*?)<br>}ism', $p, $maddr)) {
               $addr = strip_html($maddr[1]);
            }
            printf("Inserting $name\n");
            scraperwiki::sqliteexecute("insert into $table values (?, ?,?,?)", 
               array(null, clean($name), clean($addr), ''));
         } else {
           printf("Can't find name: in $p\n");
         }
      }
  } else {
    die ("Can't parse addresses");
  }
  scraperwiki::sqlitecommit();
}

########################################
function strip_html($s) {
    $s = preg_replace('{,\s*}', ', ', $s);
    $s = preg_replace('{<.*?>}', '', $s);
    $s = preg_replace('{<.*$}', '', $s); // in case the string starts wtih an open tag, e.g. "click <a hre"
    return $s;
}

function clean($name) {
  return ucfirst(strtolower($name));
}


?>
