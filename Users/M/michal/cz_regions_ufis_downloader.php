<?php
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico=&obdobi=&vykaz=
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazyxml.pl

require 'scraperwiki/simple_html_dom.php';
//read the saved tables
scraperwiki::attach("cz_regions_ufis_basics", "src");
$regions = scraperwiki::select("* from src.swdata order by code ASC");
//scraperwiki::save_var('last_i',0);die();//temp
//$i = scraperwiki::get_var('last_i',0);

$years = array('2010','2011');
$forms = array(50,1,2,3,4);

foreach ($regions as $region) {
  foreach ($forms as $form) {
    foreach ($years as $year) {  
      $date = $year. '1200';
      $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico={$region['IČ']}&obdobi={$date}&vykaz={$form}";
      $xml = scraperwiki::scrape($url);
      $data = array('region_code' => $region['code'], 'org_id' => $region['IČ'], 'region_name' => $region['Název /dle ČSÚ/'],'period' => $year, 'form' => $form);
      $data['xml'] = $xml;
      scraperwiki::save_sqlite(array('org_id','period','form'), $data);
    }
  }
}
?>
<?php
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico=&obdobi=&vykaz=
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazyxml.pl

require 'scraperwiki/simple_html_dom.php';
//read the saved tables
scraperwiki::attach("cz_regions_ufis_basics", "src");
$regions = scraperwiki::select("* from src.swdata order by code ASC");
//scraperwiki::save_var('last_i',0);die();//temp
//$i = scraperwiki::get_var('last_i',0);

$years = array('2010','2011');
$forms = array(50,1,2,3,4);

foreach ($regions as $region) {
  foreach ($forms as $form) {
    foreach ($years as $year) {  
      $date = $year. '1200';
      $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico={$region['IČ']}&obdobi={$date}&vykaz={$form}";
      $xml = scraperwiki::scrape($url);
      $data = array('region_code' => $region['code'], 'org_id' => $region['IČ'], 'region_name' => $region['Název /dle ČSÚ/'],'period' => $year, 'form' => $form);
      $data['xml'] = $xml;
      scraperwiki::save_sqlite(array('org_id','period','form'), $data);
    }
  }
}
?>
<?php
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico=&obdobi=&vykaz=
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazyxml.pl

require 'scraperwiki/simple_html_dom.php';
//read the saved tables
scraperwiki::attach("cz_regions_ufis_basics", "src");
$regions = scraperwiki::select("* from src.swdata order by code ASC");
//scraperwiki::save_var('last_i',0);die();//temp
//$i = scraperwiki::get_var('last_i',0);

$years = array('2010','2011');
$forms = array(50,1,2,3,4);

foreach ($regions as $region) {
  foreach ($forms as $form) {
    foreach ($years as $year) {  
      $date = $year. '1200';
      $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico={$region['IČ']}&obdobi={$date}&vykaz={$form}";
      $xml = scraperwiki::scrape($url);
      $data = array('region_code' => $region['code'], 'org_id' => $region['IČ'], 'region_name' => $region['Název /dle ČSÚ/'],'period' => $year, 'form' => $form);
      $data['xml'] = $xml;
      scraperwiki::save_sqlite(array('org_id','period','form'), $data);
    }
  }
}
?>
<?php
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico=&obdobi=&vykaz=
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazyxml.pl

require 'scraperwiki/simple_html_dom.php';
//read the saved tables
scraperwiki::attach("cz_regions_ufis_basics", "src");
$regions = scraperwiki::select("* from src.swdata order by code ASC");
//scraperwiki::save_var('last_i',0);die();//temp
//$i = scraperwiki::get_var('last_i',0);

$years = array('2010','2011');
$forms = array(50,1,2,3,4);

foreach ($regions as $region) {
  foreach ($forms as $form) {
    foreach ($years as $year) {  
      $date = $year. '1200';
      $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico={$region['IČ']}&obdobi={$date}&vykaz={$form}";
      $xml = scraperwiki::scrape($url);
      $data = array('region_code' => $region['code'], 'org_id' => $region['IČ'], 'region_name' => $region['Název /dle ČSÚ/'],'period' => $year, 'form' => $form);
      $data['xml'] = $xml;
      scraperwiki::save_sqlite(array('org_id','period','form'), $data);
    }
  }
}
?>
