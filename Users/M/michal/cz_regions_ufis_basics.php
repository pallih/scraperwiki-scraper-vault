<?php

//get all regions and their ID (ICO)

require 'scraperwiki/simple_html_dom.php';

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/index.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$options = $dom->find('select[id=nutsnam]',0)->find('option');
foreach ($options as $option) {
  $url_reg = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/charakteristika.pl?nuts={$option->value}&nutsnam={$option->value}";
  $html_reg = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url_reg)));
  $reg = array(
    'code' => $option->value,
    'name' => $option->name
  );
  $dom_reg = new simple_html_dom();
  $dom_reg->load($html_reg);
  $lis = $dom_reg->find('li');
  foreach ($lis as $li) {
    $divl = $li->find('div[class=LeftColumn]',0);
    $divr = $li->find('div[class=RightColumn]',0);
    $reg[$divl->plaintext] = trim(str_replace('&nbsp;','',$divr->plaintext));
  }
  $region[] = $reg;
}
 
scraperwiki::save_sqlite(array('code'), $region);



?>
<?php

//get all regions and their ID (ICO)

require 'scraperwiki/simple_html_dom.php';

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/index.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$options = $dom->find('select[id=nutsnam]',0)->find('option');
foreach ($options as $option) {
  $url_reg = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/charakteristika.pl?nuts={$option->value}&nutsnam={$option->value}";
  $html_reg = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url_reg)));
  $reg = array(
    'code' => $option->value,
    'name' => $option->name
  );
  $dom_reg = new simple_html_dom();
  $dom_reg->load($html_reg);
  $lis = $dom_reg->find('li');
  foreach ($lis as $li) {
    $divl = $li->find('div[class=LeftColumn]',0);
    $divr = $li->find('div[class=RightColumn]',0);
    $reg[$divl->plaintext] = trim(str_replace('&nbsp;','',$divr->plaintext));
  }
  $region[] = $reg;
}
 
scraperwiki::save_sqlite(array('code'), $region);



?>
<?php

//get all regions and their ID (ICO)

require 'scraperwiki/simple_html_dom.php';

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/index.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$options = $dom->find('select[id=nutsnam]',0)->find('option');
foreach ($options as $option) {
  $url_reg = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/charakteristika.pl?nuts={$option->value}&nutsnam={$option->value}";
  $html_reg = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url_reg)));
  $reg = array(
    'code' => $option->value,
    'name' => $option->name
  );
  $dom_reg = new simple_html_dom();
  $dom_reg->load($html_reg);
  $lis = $dom_reg->find('li');
  foreach ($lis as $li) {
    $divl = $li->find('div[class=LeftColumn]',0);
    $divr = $li->find('div[class=RightColumn]',0);
    $reg[$divl->plaintext] = trim(str_replace('&nbsp;','',$divr->plaintext));
  }
  $region[] = $reg;
}
 
scraperwiki::save_sqlite(array('code'), $region);



?>
<?php

//get all regions and their ID (ICO)

require 'scraperwiki/simple_html_dom.php';

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/index.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

$options = $dom->find('select[id=nutsnam]',0)->find('option');
foreach ($options as $option) {
  $url_reg = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisusc/charakteristika.pl?nuts={$option->value}&nutsnam={$option->value}";
  $html_reg = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url_reg)));
  $reg = array(
    'code' => $option->value,
    'name' => $option->name
  );
  $dom_reg = new simple_html_dom();
  $dom_reg->load($html_reg);
  $lis = $dom_reg->find('li');
  foreach ($lis as $li) {
    $divl = $li->find('div[class=LeftColumn]',0);
    $divr = $li->find('div[class=RightColumn]',0);
    $reg[$divl->plaintext] = trim(str_replace('&nbsp;','',$divr->plaintext));
  }
  $region[] = $reg;
}
 
scraperwiki::save_sqlite(array('code'), $region);



?>
