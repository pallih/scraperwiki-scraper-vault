<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('court','year','docket');
$minYear = 2012;
$base_url = 'http://decisions.fca-caf.gc.ca';
$index_url = $base_url . '/en/dn/%d/%02d.html'; // %d = year; %2d = month;

/* execution */

// for each year
for($y = $minYear; $y <= date('Y'); $y++){
  // for each month
  for($m = 1; $m <= 12; $m++){ 
    // load the page listing the cases for the year
    $html_content = scraperwiki::scrape(sprintf($index_url, $y, $m));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each case
    foreach($dom->find(".intitule li") as $row){
      $r = array('year' => $y, 'court' => 'FCA');
      $r['title'] = $row->find(".texte2 a",0)->innertext;

      // if there is a second span, it's the citation
      $cite = $row->find("span", 1);
      if($cite && $cite->plaintext{0} == '(')
        $r['cite'] = html_entity_decode(trim($cite->plaintext, '() '), ENT_COMPAT, 'UTF-8');
    
      $docket_and_date = $row->innertext;
      if(preg_match('/\<br\>\s*([A-Z0-9\-]+)\,/', $docket_and_date, $match))
        $r['docket'] = $match[1];
      if(preg_match('/Date\:\s+(.*)/', $docket_and_date, $match))
        $r['date'] = trim($match[1]);

      // load the inner case page to get the direct file links
      $link = $base_url . $row->find(".texte2 a",0)->href;
      $case_html_content = scraperwiki::scrape($link);
      if(empty($case_html_content)){
        scraperwiki::save(array('court','year','docket'), $r);
        continue;
      }

      // some pages are too big to load the dom (zend_nm_heap error): delete the main "section" divs
      $case_html_content = preg_replace('/\<DIV class=\"Section\d+\"\>.*?\<\/DIV\>/is', '', $case_html_content);

      // get the dom
      $case_dom = str_get_html($case_html_content);
      if(!$case_dom){
        scraperwiki::save($db_index, $r);
        continue;
      }

      // printer-friendly html
      $r['url_html'] = $base_url . $case_dom->find("a.printerFriendlyLink",0)->href;

      // pdf
      foreach($case_dom->find(".item a") as $item){
        if($item->plaintext == 'PDF'){
          $r['url_pdf'] = $base_url . $item->href;
          break;
        }
      }
      scraperwiki::save($db_index, $r);
    }// end for each case
  }// end for each month
}// end for each year
?>
