<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=598518
//source of codes: https://scraperwiki.com/scrapers/cz_localities_list/

require 'scraperwiki/simple_html_dom.php'; 

scraperwiki::save_var('last_code',570966);  //temp
$last_code = scraperwiki::get_var('last_code',0);


scraperwiki::attach("cz_localities_list", "src");
$rows = scraperwiki::select("code from src.swdata where code> '{$last_code}' order by code");
echo count($rows);

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $url = "http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=" . $row['code'];
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    //extract info
    $forms = $dom->find('form[name=Obec]');
    scraperwiki::save_sqlite(array('code'),array('code'=>$row['code'],'html'=>$forms[0]->outertext));
    scraperwiki::save_var('last_code',$row['code']);
    //echo $forms[0]->outertext;die();
  }
}
scraperwiki::save_var('last_code',0);


?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=598518
//source of codes: https://scraperwiki.com/scrapers/cz_localities_list/

require 'scraperwiki/simple_html_dom.php'; 

scraperwiki::save_var('last_code',570966);  //temp
$last_code = scraperwiki::get_var('last_code',0);


scraperwiki::attach("cz_localities_list", "src");
$rows = scraperwiki::select("code from src.swdata where code> '{$last_code}' order by code");
echo count($rows);

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $url = "http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=" . $row['code'];
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    //extract info
    $forms = $dom->find('form[name=Obec]');
    scraperwiki::save_sqlite(array('code'),array('code'=>$row['code'],'html'=>$forms[0]->outertext));
    scraperwiki::save_var('last_code',$row['code']);
    //echo $forms[0]->outertext;die();
  }
}
scraperwiki::save_var('last_code',0);


?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=598518
//source of codes: https://scraperwiki.com/scrapers/cz_localities_list/

require 'scraperwiki/simple_html_dom.php'; 

scraperwiki::save_var('last_code',570966);  //temp
$last_code = scraperwiki::get_var('last_code',0);


scraperwiki::attach("cz_localities_list", "src");
$rows = scraperwiki::select("code from src.swdata where code> '{$last_code}' order by code");
echo count($rows);

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $url = "http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=" . $row['code'];
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    //extract info
    $forms = $dom->find('form[name=Obec]');
    scraperwiki::save_sqlite(array('code'),array('code'=>$row['code'],'html'=>$forms[0]->outertext));
    scraperwiki::save_var('last_code',$row['code']);
    //echo $forms[0]->outertext;die();
  }
}
scraperwiki::save_var('last_code',0);


?>
<?php

//source: http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=598518
//source of codes: https://scraperwiki.com/scrapers/cz_localities_list/

require 'scraperwiki/simple_html_dom.php'; 

scraperwiki::save_var('last_code',570966);  //temp
$last_code = scraperwiki::get_var('last_code',0);


scraperwiki::attach("cz_localities_list", "src");
$rows = scraperwiki::select("code from src.swdata where code> '{$last_code}' order by code");
echo count($rows);

if (count($rows) > 0) {
  foreach ($rows as $row) {
    $url = "http://portal.gov.cz/wps/portal/_s.155/696?kam=obec&kod=" . $row['code'];
    $html = scraperwiki::scrape($url);
    //get dom
    $dom = new simple_html_dom();
    $dom->load($html);
    //extract info
    $forms = $dom->find('form[name=Obec]');
    scraperwiki::save_sqlite(array('code'),array('code'=>$row['code'],'html'=>$forms[0]->outertext));
    scraperwiki::save_var('last_code',$row['code']);
    //echo $forms[0]->outertext;die();
  }
}
scraperwiki::save_var('last_code',0);


?>
