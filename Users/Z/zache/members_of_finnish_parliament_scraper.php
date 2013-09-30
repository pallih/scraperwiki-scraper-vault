<?php

// Get all members of finnish parliament.
// From: http://www.eduskunta.fi/thwfakta/hetekau/hex/hxent.htm 

$maxcount=10;
$parliament_members=array();
 
$url='http://www.eduskunta.fi/triphome/bin/thw/trip/?${base}=hetekaue&${maxpage}=101&${snhtml}=
hex/hxnosynk&${html}=hex/hx4600&${oohtml}=hex/hx4600&${sort}=lajitnimi&nykyinen=$+and+lajitnimi=$#alkuun';
$file=file_get_contents($url);

$continue=true;
while($continue) {
   $continue=false;
  $match="|<table.*?>(.*?)</table>|ism";
  if (preg_match_all($match, $file, $tables)) {
    $match="|<tr.*?>(.*?)</tr>|ism";
    if (preg_match_all($match, $tables[1][1], $rows)) {
      foreach ($rows[1] as $r) {
         $match="|<a.*?href=\"(.*?)\".*?target=\"edus_main\".*?>(.*?)</a>|ism";
         
         if (preg_match($match, $r, $n)) {
             $url="http://www.eduskunta.fi/" . $n[1];
             $name=trim(strip_tags(str_replace("&nbsp", " ", $n[2])));
             $parliament_members[$name]=$url;
         } 
       }
    }
  } else {
    die("ERROR: Failed to get parliament members.!\n");
  }

  $match="|href=\"(.*?)#.*?\"Seuraava sivu\"|"; 
  if (preg_match($match, $file, $m)) { 
     $continue=true;
     $url="http://www.eduskunta.fi/" . $m[1];
     $file=file_get_contents($url);
     sleep(0.1);
  }
}

function parse_parliament_member($url, $name) {
  $file=file_get_contents($url);

  $match="|frame name=oikea2 src=(.*?htm) |";
  if (preg_match($match, $file, $tmp)) {
    $file=file_get_contents("http://www.eduskunta.fi" .$tmp[1]);
  } else {
    die("ERROR");
  }; 
  sleep(0.1);

  // Get main table 
  $match="|<table.*?>(.*?)</table>|ism";
  if (preg_match_all($match, $file, $tables)) {
    $match="|<tr.*?>(.*?)</tr>|ism";
    unset($rows);
    if (preg_match_all($match, $tables[1][0], $rows)) {
      unset($n);
      $n=parse_rows($rows[1]);
      $n['Url']=$url;
      $n['Alkuperäinen nimi']=$name;
      
      return $n;      
    }
  } else {
    die("ERROR: Page has no kansanedustaja! $url\n");
  }
}


// Parse single parliament info row

function parse_rows($rows) {
  $parliament_member=array();
  foreach($rows as $k=>$r) {
    if ($k==0) {
       $match="|<b>(.*?)</b>|ism";
       if (preg_match_all($match, $r, $cols)) { 
          $parliament_member['nimi']=$cols[1][0];
          $parliament_member['kansanedustajana']=$cols[1][2];
       }       
    } else {
       $match="|<td.*?>(.*?)</td>|ism";
       if (preg_match_all($match, $r, $cols)) {
          $key=preg_replace("|:\z|", "", trim(strip_tags($cols[1][0])));
         if (!isset($cols[1][1])) continue;
          else if (trim(strip_tags($cols[1][1]))=="") continue;
          $value=trim(str_replace("&nbsp;", " ", strip_tags($cols[1][1])));

          switch($key) {
             case 'Eduskuntatoiminta':
             case 'Yhteiskunnallinen toiminta': continue;
             case 'T&auml;ydellinen nimi': 
                      $tmp=split(",", $value);
                      $parliament_member['Etunimi']=$tmp[1];
                      $parliament_member['Sukunimi']=$tmp[0];
                      break;
             case 'Syntym&auml;aika ja -paikka':
                     $tmp=split(" ", $value);
                      $parliament_member['Syntym&auml;aika']=$tmp[0];
                      $parliament_member['Syntym&auml;paikka']=$tmp[1];
                      break;
             case 'Kuolinaika ja -paikka':
                      $tmp=split(" ", $value);
                      $parliament_member['Kuolinaika']=$tmp[0];
                      $parliament_member['Kuolinpaikka']=$tmp[1];

             default: $parliament_member[$key .""]=trim(strip_tags($cols[1][1]) .""); break;
          }
       } 
    }
  }
  return $parliament_member;
}


// Parse all members of finnish parliament. 
$count=0;
foreach($parliament_members as $k=>$v) {
   $parsed_member=parse_parliament_member($v, $k);
   print_r($parsed_member);
   scraperwiki::save(array('Alkuperäinen nimi'), $parsed_member);
   $count++;
//   if ($count>$maxcount) break;
}

?>
<?php

// Get all members of finnish parliament.
// From: http://www.eduskunta.fi/thwfakta/hetekau/hex/hxent.htm 

$maxcount=10;
$parliament_members=array();
 
$url='http://www.eduskunta.fi/triphome/bin/thw/trip/?${base}=hetekaue&${maxpage}=101&${snhtml}=
hex/hxnosynk&${html}=hex/hx4600&${oohtml}=hex/hx4600&${sort}=lajitnimi&nykyinen=$+and+lajitnimi=$#alkuun';
$file=file_get_contents($url);

$continue=true;
while($continue) {
   $continue=false;
  $match="|<table.*?>(.*?)</table>|ism";
  if (preg_match_all($match, $file, $tables)) {
    $match="|<tr.*?>(.*?)</tr>|ism";
    if (preg_match_all($match, $tables[1][1], $rows)) {
      foreach ($rows[1] as $r) {
         $match="|<a.*?href=\"(.*?)\".*?target=\"edus_main\".*?>(.*?)</a>|ism";
         
         if (preg_match($match, $r, $n)) {
             $url="http://www.eduskunta.fi/" . $n[1];
             $name=trim(strip_tags(str_replace("&nbsp", " ", $n[2])));
             $parliament_members[$name]=$url;
         } 
       }
    }
  } else {
    die("ERROR: Failed to get parliament members.!\n");
  }

  $match="|href=\"(.*?)#.*?\"Seuraava sivu\"|"; 
  if (preg_match($match, $file, $m)) { 
     $continue=true;
     $url="http://www.eduskunta.fi/" . $m[1];
     $file=file_get_contents($url);
     sleep(0.1);
  }
}

function parse_parliament_member($url, $name) {
  $file=file_get_contents($url);

  $match="|frame name=oikea2 src=(.*?htm) |";
  if (preg_match($match, $file, $tmp)) {
    $file=file_get_contents("http://www.eduskunta.fi" .$tmp[1]);
  } else {
    die("ERROR");
  }; 
  sleep(0.1);

  // Get main table 
  $match="|<table.*?>(.*?)</table>|ism";
  if (preg_match_all($match, $file, $tables)) {
    $match="|<tr.*?>(.*?)</tr>|ism";
    unset($rows);
    if (preg_match_all($match, $tables[1][0], $rows)) {
      unset($n);
      $n=parse_rows($rows[1]);
      $n['Url']=$url;
      $n['Alkuperäinen nimi']=$name;
      
      return $n;      
    }
  } else {
    die("ERROR: Page has no kansanedustaja! $url\n");
  }
}


// Parse single parliament info row

function parse_rows($rows) {
  $parliament_member=array();
  foreach($rows as $k=>$r) {
    if ($k==0) {
       $match="|<b>(.*?)</b>|ism";
       if (preg_match_all($match, $r, $cols)) { 
          $parliament_member['nimi']=$cols[1][0];
          $parliament_member['kansanedustajana']=$cols[1][2];
       }       
    } else {
       $match="|<td.*?>(.*?)</td>|ism";
       if (preg_match_all($match, $r, $cols)) {
          $key=preg_replace("|:\z|", "", trim(strip_tags($cols[1][0])));
         if (!isset($cols[1][1])) continue;
          else if (trim(strip_tags($cols[1][1]))=="") continue;
          $value=trim(str_replace("&nbsp;", " ", strip_tags($cols[1][1])));

          switch($key) {
             case 'Eduskuntatoiminta':
             case 'Yhteiskunnallinen toiminta': continue;
             case 'T&auml;ydellinen nimi': 
                      $tmp=split(",", $value);
                      $parliament_member['Etunimi']=$tmp[1];
                      $parliament_member['Sukunimi']=$tmp[0];
                      break;
             case 'Syntym&auml;aika ja -paikka':
                     $tmp=split(" ", $value);
                      $parliament_member['Syntym&auml;aika']=$tmp[0];
                      $parliament_member['Syntym&auml;paikka']=$tmp[1];
                      break;
             case 'Kuolinaika ja -paikka':
                      $tmp=split(" ", $value);
                      $parliament_member['Kuolinaika']=$tmp[0];
                      $parliament_member['Kuolinpaikka']=$tmp[1];

             default: $parliament_member[$key .""]=trim(strip_tags($cols[1][1]) .""); break;
          }
       } 
    }
  }
  return $parliament_member;
}


// Parse all members of finnish parliament. 
$count=0;
foreach($parliament_members as $k=>$v) {
   $parsed_member=parse_parliament_member($v, $k);
   print_r($parsed_member);
   scraperwiki::save(array('Alkuperäinen nimi'), $parsed_member);
   $count++;
//   if ($count>$maxcount) break;
}

?>
