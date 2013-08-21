<?php

require 'scraperwiki/simple_html_dom.php';           

  
function scrapeTEDRSS($url, $sector){
 print($url." ".$sector."\n");
 // $xml = scraperWiki::scrape($url);  
  $curl = curl_init($url);
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
  curl_setopt($curl, CURLOPT_MAXREDIRS, 10);
  curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
  curl_setopt($curl, CURLOPT_TIMEOUT, 20); // 10 second before aborting
  // try CURLOPT_CONNECTTIMEOUT (in seconds)
  // try CURLOPT_LOW_SPEED_LIMIT (to define what slow is, with):
  // curl_setopt($curl, CURLOPT_LOW_SPEED_TIME, 10); (10 second at low speed before aborting
  $xml = curl_exec($curl);
  print (curl_error($curl)."\n");
 $dom = new simple_html_dom();
 $dom->load($xml);
 
 $items = $dom->find("item");
 foreach ($items as $item){
   $guid = $item->find("guid");
   $noticeURL = str_replace("TEXT", "DATA", $guid[0]->plaintext);
   print($noticeURL." ".$sector." ".(memory_get_usage()/1000000)."MB"); echo "\n";
   // $record = scrapeTEDDataPage ($noticeURL, $sector);
   $record = array ('time' => microtime(true), 'sector' => $sector, 'url' => $noticeURL);
   scraperwiki::save(array('sector', 'url'), $record); 
   sleep(1);
 }
 $dom->__destruct();
 unset($items); unset($dom); unset($xml);
 print(((memory_get_usage()/1024)/1024)."MB\n");
}


scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_agfo_DK.xml', 'Agriculture and Food');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_comp_DK.xml', 'Computer and Related Services');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_core_DK.xml', 'Construction and Real Estate');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_educ_DK.xml', 'Education');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_ener_DK.xml', 'Energy and Related Services');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_ensa_DK.xml', 'Environment and Sanitation');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_fina_DK.xml', 'Finance and Related Services');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_mapr_DK.xml', 'Materials and Products');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_mior_DK.xml', 'Mining and Ores');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_prpu_DK.xml', 'Printing and Publishing');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_reco_DK.xml', 'Research and Development');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_serv_DK.xml', 'Other Services');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_teeq_DK.xml', 'Technology and Equipment');
scrapeTEDRSS('http://ted.europa.eu/TED/rss/en/RSS_tran_DK.xml', 'Transport and Related Services');


?>
