<?php
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico=&obdobi=&vykaz=
//http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazyxml.pl

require 'scraperwiki/simple_html_dom.php';
//read the saved tables
//scraperwiki::save_var('last_i',0);die();//5577
scraperwiki::attach("cz_public_organizations_ufis_ids", "src");
//$forms = scraperwiki::select("* from src.form order by dri DESC,period DESC,org_id ASC,form DESC");
$forms = scraperwiki::select("* from src.form where dri=1 and period='12/2012' order by dri DESC,period DESC,org_id ASC,form DESC");
//scraperwiki::save_var('last_i',0);die();//temp
$i = scraperwiki::get_var('last_i',0);

foreach ((array) $forms as $key => $form) {
  if ($key < $i) continue; 
 
  scraperwiki::save_var('last_i',$key);

  $date_ar = explode('/',$form['period']);
  $date = $date_ar[1] . $date_ar[0] . '00';
  $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufis/iufisxml/vykazxml.pl?ico={$form['org_id']}&obdobi={$date}&vykaz={$form['form']}";
  $xml = scraperwiki::scrape($url);
  $data = $form;
  $data['xml'] = $xml;
  scraperwiki::save_sqlite(array('org_id','period','form'), $data);
}
?>
