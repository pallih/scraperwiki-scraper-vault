<?php

require 'scraperwiki/simple_html_dom.php'; 

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//get different 'dri' = type of organizations
$inputs = $dom->find('form',0)->find('table[border=1]',0)->find('input');
$labels = $dom->find('form',0)->find('table[border=1]',0)->find('label');
foreach ((array) $inputs as $key => $input) {
  $dri[$key]['value'] = $input->value;
  $dri[$key]['label'] = str_replace('&nbsp;',' ',$labels[$key]->innertext);
  $data = $dri[$key];
  scraperwiki::save_sqlite(array('value'), $data, "dri");
}
//get different periods (obdobi)
$periods_obj = $dom->find('form',0)->find('select[name=obdobi]',0)->find('option');
foreach ((array) $periods_obj as $key => $period) {
  $intervals[$key] = $period->innertext;
  $data = array();
  $data['value'] = $intervals[$key];
  scraperwiki::save_sqlite(array('value'), $data, "period");
}
//get different forms (vykaz)
$forms_obj = $dom->find('form',0)->find('select[name=vykaznam]',0)->find('option');
foreach ((array) $forms_obj as $key => $form) {
  $forms[$key]['value'] = $form->value;
  $forms[$key]['label'] = trim($form->innertext);
  $data = $forms[$key];
  scraperwiki::save_sqlite(array('value'), $data, "form");
}
//get different chapters (kapitola)
$chapters_obj = $dom->find('form',0)->find('select[name=kapitolanam]',0)->find('option');
foreach ((array) $chapters_obj as $key => $chapter) {
  $chapters[$key]['value'] = $chapter->value;
  $chapters[$key]['label'] = trim($chapter->innertext);
  $data = $chapters[$key];
  scraperwiki::save_sqlite(array('value'), $data, "chapter");
}
//get different regions (okres)
$regions_obj = $dom->find('form',0)->find('select[name=zkonam]',0)->find('option');
foreach ((array) $regions_obj as $key => $region) {
  $regions[$key]['value'] = $region->value;
  $regions[$key]['label'] = trim($region->innertext);
  $data = $regions[$key];
  scraperwiki::save_sqlite(array('value'), $data, "region");
}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

//download main page
$url = "http://wwwinfo.mfcr.cz/cgi-bin/aris/iarisorg/uvodni.pl";
$html = str_replace('windows-1250','utf-8',iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url)));
//get dom
$dom = new simple_html_dom();
$dom->load($html);

//get different 'dri' = type of organizations
$inputs = $dom->find('form',0)->find('table[border=1]',0)->find('input');
$labels = $dom->find('form',0)->find('table[border=1]',0)->find('label');
foreach ((array) $inputs as $key => $input) {
  $dri[$key]['value'] = $input->value;
  $dri[$key]['label'] = str_replace('&nbsp;',' ',$labels[$key]->innertext);
  $data = $dri[$key];
  scraperwiki::save_sqlite(array('value'), $data, "dri");
}
//get different periods (obdobi)
$periods_obj = $dom->find('form',0)->find('select[name=obdobi]',0)->find('option');
foreach ((array) $periods_obj as $key => $period) {
  $intervals[$key] = $period->innertext;
  $data = array();
  $data['value'] = $intervals[$key];
  scraperwiki::save_sqlite(array('value'), $data, "period");
}
//get different forms (vykaz)
$forms_obj = $dom->find('form',0)->find('select[name=vykaznam]',0)->find('option');
foreach ((array) $forms_obj as $key => $form) {
  $forms[$key]['value'] = $form->value;
  $forms[$key]['label'] = trim($form->innertext);
  $data = $forms[$key];
  scraperwiki::save_sqlite(array('value'), $data, "form");
}
//get different chapters (kapitola)
$chapters_obj = $dom->find('form',0)->find('select[name=kapitolanam]',0)->find('option');
foreach ((array) $chapters_obj as $key => $chapter) {
  $chapters[$key]['value'] = $chapter->value;
  $chapters[$key]['label'] = trim($chapter->innertext);
  $data = $chapters[$key];
  scraperwiki::save_sqlite(array('value'), $data, "chapter");
}
//get different regions (okres)
$regions_obj = $dom->find('form',0)->find('select[name=zkonam]',0)->find('option');
foreach ((array) $regions_obj as $key => $region) {
  $regions[$key]['value'] = $region->value;
  $regions[$key]['label'] = trim($region->innertext);
  $data = $regions[$key];
  scraperwiki::save_sqlite(array('value'), $data, "region");
}

?>
