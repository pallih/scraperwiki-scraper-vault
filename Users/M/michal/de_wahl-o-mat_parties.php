<?php

//extract parties from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
'sl'=>array('file'=>'sl_0.html','year'=>'2012'),
'sh'=>array('file'=>'sh_0.html','year'=>'2012'),
'nw'=>array('file'=>'nw_0.html','year'=>'2012'),
'hh'=>array('file'=>'hh_0.html','year'=>'2011'),
'rp'=>array('file'=>'rp_0.html','year'=>'2011'),
'bw'=>array('file'=>'bw_0.html','year'=>'2011'),
'hb'=>array('file'=>'hb_0.html','year'=>'2011'),
'be'=>array('file'=>'be_0.html','year'=>'2011'),
);

require 'scraperwiki/simple_html_dom.php';

foreach ($files as $key => $row) {
  $url = $domain . $row['file'];
  $html = iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
//echo $dom->innertext;die();

  $divs = $dom->find("div[class=checkbox_wrap]");

  foreach ($divs as $div) {
    $span_ar=explode('</b>',$div->find("span[class=middle]",0)->innertext);
    $item = array( 
      'abbreviation' => html_entity_decode(strip_tags($span_ar[0]),ENT_COMPAT,'UTF-8'),
      'name' => strip_tags(html_entity_decode($span_ar[1],ENT_COMPAT,'UTF-8')),
      'land' => $key,
      'year' => $row['year'],
    );
//echo html_entity_decode($span_ar[0],ENT_COMPAT,'UTF-8');
//echo $span_ar[0];
    $data[] = $item;
  }
/*print_r($data);
die();*/
}
scraperwiki::save_sqlite(array('land','year','name'),$data);

?>
<?php

//extract parties from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
'sl'=>array('file'=>'sl_0.html','year'=>'2012'),
'sh'=>array('file'=>'sh_0.html','year'=>'2012'),
'nw'=>array('file'=>'nw_0.html','year'=>'2012'),
'hh'=>array('file'=>'hh_0.html','year'=>'2011'),
'rp'=>array('file'=>'rp_0.html','year'=>'2011'),
'bw'=>array('file'=>'bw_0.html','year'=>'2011'),
'hb'=>array('file'=>'hb_0.html','year'=>'2011'),
'be'=>array('file'=>'be_0.html','year'=>'2011'),
);

require 'scraperwiki/simple_html_dom.php';

foreach ($files as $key => $row) {
  $url = $domain . $row['file'];
  $html = iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
//echo $dom->innertext;die();

  $divs = $dom->find("div[class=checkbox_wrap]");

  foreach ($divs as $div) {
    $span_ar=explode('</b>',$div->find("span[class=middle]",0)->innertext);
    $item = array( 
      'abbreviation' => html_entity_decode(strip_tags($span_ar[0]),ENT_COMPAT,'UTF-8'),
      'name' => strip_tags(html_entity_decode($span_ar[1],ENT_COMPAT,'UTF-8')),
      'land' => $key,
      'year' => $row['year'],
    );
//echo html_entity_decode($span_ar[0],ENT_COMPAT,'UTF-8');
//echo $span_ar[0];
    $data[] = $item;
  }
/*print_r($data);
die();*/
}
scraperwiki::save_sqlite(array('land','year','name'),$data);

?>
<?php

//extract parties from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
'sl'=>array('file'=>'sl_0.html','year'=>'2012'),
'sh'=>array('file'=>'sh_0.html','year'=>'2012'),
'nw'=>array('file'=>'nw_0.html','year'=>'2012'),
'hh'=>array('file'=>'hh_0.html','year'=>'2011'),
'rp'=>array('file'=>'rp_0.html','year'=>'2011'),
'bw'=>array('file'=>'bw_0.html','year'=>'2011'),
'hb'=>array('file'=>'hb_0.html','year'=>'2011'),
'be'=>array('file'=>'be_0.html','year'=>'2011'),
);

require 'scraperwiki/simple_html_dom.php';

foreach ($files as $key => $row) {
  $url = $domain . $row['file'];
  $html = iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
//echo $dom->innertext;die();

  $divs = $dom->find("div[class=checkbox_wrap]");

  foreach ($divs as $div) {
    $span_ar=explode('</b>',$div->find("span[class=middle]",0)->innertext);
    $item = array( 
      'abbreviation' => html_entity_decode(strip_tags($span_ar[0]),ENT_COMPAT,'UTF-8'),
      'name' => strip_tags(html_entity_decode($span_ar[1],ENT_COMPAT,'UTF-8')),
      'land' => $key,
      'year' => $row['year'],
    );
//echo html_entity_decode($span_ar[0],ENT_COMPAT,'UTF-8');
//echo $span_ar[0];
    $data[] = $item;
  }
/*print_r($data);
die();*/
}
scraperwiki::save_sqlite(array('land','year','name'),$data);

?>
<?php

//extract parties from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
'sl'=>array('file'=>'sl_0.html','year'=>'2012'),
'sh'=>array('file'=>'sh_0.html','year'=>'2012'),
'nw'=>array('file'=>'nw_0.html','year'=>'2012'),
'hh'=>array('file'=>'hh_0.html','year'=>'2011'),
'rp'=>array('file'=>'rp_0.html','year'=>'2011'),
'bw'=>array('file'=>'bw_0.html','year'=>'2011'),
'hb'=>array('file'=>'hb_0.html','year'=>'2011'),
'be'=>array('file'=>'be_0.html','year'=>'2011'),
);

require 'scraperwiki/simple_html_dom.php';

foreach ($files as $key => $row) {
  $url = $domain . $row['file'];
  $html = iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
//echo $dom->innertext;die();

  $divs = $dom->find("div[class=checkbox_wrap]");

  foreach ($divs as $div) {
    $span_ar=explode('</b>',$div->find("span[class=middle]",0)->innertext);
    $item = array( 
      'abbreviation' => html_entity_decode(strip_tags($span_ar[0]),ENT_COMPAT,'UTF-8'),
      'name' => strip_tags(html_entity_decode($span_ar[1],ENT_COMPAT,'UTF-8')),
      'land' => $key,
      'year' => $row['year'],
    );
//echo html_entity_decode($span_ar[0],ENT_COMPAT,'UTF-8');
//echo $span_ar[0];
    $data[] = $item;
  }
/*print_r($data);
die();*/
}
scraperwiki::save_sqlite(array('land','year','name'),$data);

?>
