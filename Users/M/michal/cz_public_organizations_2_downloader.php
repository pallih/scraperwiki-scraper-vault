<?php
/**
* url structure:
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola=335&Viewnao=1&useZko=1&typ=1&pocet=20
* kapitola=335 number of state budget category
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&Viewnao=1&useZko=1&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_chapter = scraperwiki::get_var('last_chapter',0);
$last_i = scraperwiki::get_var('last_i',0);

//get chapters
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //chapters
$chaps = $dom->find("option");
foreach((array)$chaps as $chap) {
  $chapters[] = $chap->value;
}
//foreach chapter
foreach ((array) $chapters as $key => $chapter) {
 if($key >= $last_chapter) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezeny', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezen', 'záznam'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('chapter' => $chapter, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('chapter','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_chapter',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_chapter',0);



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
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola=335&Viewnao=1&useZko=1&typ=1&pocet=20
* kapitola=335 number of state budget category
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&Viewnao=1&useZko=1&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_chapter = scraperwiki::get_var('last_chapter',0);
$last_i = scraperwiki::get_var('last_i',0);

//get chapters
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //chapters
$chaps = $dom->find("option");
foreach((array)$chaps as $chap) {
  $chapters[] = $chap->value;
}
//foreach chapter
foreach ((array) $chapters as $key => $chapter) {
 if($key >= $last_chapter) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezeny', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezen', 'záznam'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('chapter' => $chapter, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('chapter','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_chapter',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_chapter',0);



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
* http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola=335&Viewnao=1&useZko=1&typ=1&pocet=20
* kapitola=335 number of state budget category
* pocet=20 starting number(-1) for list ('pocet' - bad name)
* Viewico=1&Viewnao=1&useZko=1&typ=1 dont know, leave as it is
*/

// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

//get vars for next run
$last_chapter = scraperwiki::get_var('last_chapter',0);
$last_i = scraperwiki::get_var('last_i',0);

//get chapters
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2uvod.pl";
$html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
$dom = new simple_html_dom();
$dom->load($html);
  //chapters
$chaps = $dom->find("option");
foreach((array)$chaps as $chap) {
  $chapters[] = $chap->value;
}
//foreach chapter
foreach ((array) $chapters as $key => $chapter) {
 if($key >= $last_chapter) {
  //get number of records
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet=0";
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $total = trim(get_first_string ($html,'Celkem nalezeno', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezeny', 'záznam'));
  if ($total == '') $total = trim(get_first_string ($html,'Celkem nalezen', 'záznam'));
  //up to number of records
  for ($i = $last_i; $i < $total; $i=$i+20) {
    //get the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/vyber2.pl?Viewico=1&kapitola={$chapter}&Viewnao=1&useZko=1&typ=1&pocet={$i}";
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //get dom
    $dom = new simple_html_dom(); 
    $dom->load($html);
    //extract the table with data
    $tables = $dom->find("table");
    $out = array('chapter' => $chapter, 'i' => $i, 'html' => $tables[2]->innertext);
    //save it
    scraperwiki::save_sqlite(array('chapter','i'),$out);
    scraperwiki::save_var('last_i',$i);
    scraperwiki::save_var('last_chapter',$key);
  }
  scraperwiki::save_var('last_i',0);
  $last_i = 0;
 }
}
scraperwiki::save_var('last_chapter',0);



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
