<?php
/**
* url structure:
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj=CZ031&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=20
* zkokraj=CZ031 region (kraj) according to CZSO (czso.cz)
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&uzemcelek=2&Viewnao=0&useZko=0&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_region = scraperwiki::get_var('last_region',0);
$last_i = scraperwiki::get_var('last_i',0);

//get regions
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //selects
$selects = $dom->find("select");
  //options from 2nd select
$regs = $selects[1]->find("option");
foreach((array)$regs as $reg) {
  $regions[] = $reg->value;
}

//foreach region
foreach ((array) $regions as $key => $region) {
 if($key >= $last_region) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznamů'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('region' => $region, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('region','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_region',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_region',0);



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
/**
* url structure:
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj=CZ031&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=20
* zkokraj=CZ031 region (kraj) according to CZSO (czso.cz)
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&uzemcelek=2&Viewnao=0&useZko=0&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_region = scraperwiki::get_var('last_region',0);
$last_i = scraperwiki::get_var('last_i',0);

//get regions
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //selects
$selects = $dom->find("select");
  //options from 2nd select
$regs = $selects[1]->find("option");
foreach((array)$regs as $reg) {
  $regions[] = $reg->value;
}

//foreach region
foreach ((array) $regions as $key => $region) {
 if($key >= $last_region) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznamů'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('region' => $region, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('region','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_region',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_region',0);



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
/**
* url structure:
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj=CZ031&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=20
* zkokraj=CZ031 region (kraj) according to CZSO (czso.cz)
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&uzemcelek=2&Viewnao=0&useZko=0&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_region = scraperwiki::get_var('last_region',0);
$last_i = scraperwiki::get_var('last_i',0);

//get regions
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //selects
$selects = $dom->find("select");
  //options from 2nd select
$regs = $selects[1]->find("option");
foreach((array)$regs as $reg) {
  $regions[] = $reg->value;
}

//foreach region
foreach ((array) $regions as $key => $region) {
 if($key >= $last_region) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznamů'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('region' => $region, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('region','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_region',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_region',0);



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
/**
* url structure:
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj=CZ031&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=20
* zkokraj=CZ031 region (kraj) according to CZSO (czso.cz)
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&uzemcelek=2&Viewnao=0&useZko=0&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_region = scraperwiki::get_var('last_region',0);
$last_i = scraperwiki::get_var('last_i',0);

//get regions
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //selects
$selects = $dom->find("select");
  //options from 2nd select
$regs = $selects[1]->find("option");
foreach((array)$regs as $reg) {
  $regions[] = $reg->value;
}

//foreach region
foreach ((array) $regions as $key => $region) {
 if($key >= $last_region) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznamů'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber1.pl?Viewico=1&zkokraj={$region}&uzemcelek=2&Viewnao=0&useZko=0&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('region' => $region, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('region','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_region',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_region',0);



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
