<?php

// the original is in windows-1250 !!
// there are some chapters that are only in one of the sources, most of them are in both

//sources:
// http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisorg/uvodni.pl
// http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl

require 'scraperwiki/simple_html_dom.php';

$urls = array(
'http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisorg/uvodni.pl',
'http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl',
);
$data = array();
foreach ($urls as $url) {
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $options = $dom->find('select[name=kapitolanam]',0)->find('option');
  foreach ($options as $option) {
    $data[$option->value] = array(
      'id' => $option->value,
      'name' => $option->plaintext,
    );
  }
}
//scraperwiki probably accepts as data only an array with keys 0, 1, ... 
foreach($data as $d) {
  $out[] = $d;
}
scraperwiki::save_sqlite(array('id'),$out);
?>
<?php

// the original is in windows-1250 !!
// there are some chapters that are only in one of the sources, most of them are in both

//sources:
// http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisorg/uvodni.pl
// http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl

require 'scraperwiki/simple_html_dom.php';

$urls = array(
'http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisorg/uvodni.pl',
'http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl',
);
$data = array();
foreach ($urls as $url) {
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  $dom = new simple_html_dom();
  $dom->load($html);
  
  $options = $dom->find('select[name=kapitolanam]',0)->find('option');
  foreach ($options as $option) {
    $data[$option->value] = array(
      'id' => $option->value,
      'name' => $option->plaintext,
    );
  }
}
//scraperwiki probably accepts as data only an array with keys 0, 1, ... 
foreach($data as $d) {
  $out[] = $d;
}
scraperwiki::save_sqlite(array('id'),$out);
?>
