<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://www.publications.gov.sk.ca';
$index_url = $base_url . '/deplist.cfm?d=1&c=42';

/* execution */

// load the list of legislation
$html_content = scraperwiki::scrape(sprintf($index_url, $a, $type));
$dom = str_get_html($html_content);
   
// for each statute
foreach($dom->find("table.topDocuments tr a[href*=details]") as $row){
      $r = array('jurisdiction' => 'saskatchewan', 'type' => 'statute');
      $r['title'] = $row->plaintext;
 
      // drill into inner page for the statute
      $link = $base_url . '/' . $row->href;
      $inner_html_content = scraperwiki::scrape($link);
      if(empty($inner_html_content)){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // get the dom
      $inner_dom = str_get_html($inner_html_content);
      if(!$inner_dom){
        // cannot save without at least a cite from the inner page
        continue;
      }

      // description of statute
      $desc = $inner_dom->find("td.description",0)->innertext;

      // try to match a citation against both SS and RSS
      if(preg_match('/Chapter\s+([A-Z\.\-\d]+)\s+of\s+the\s+([^\,\d]+),\s*(\d{4})/is', $desc, $match)){
         $vol = null;
         if($match[2] == 'Revised Statutes of Saskatchewan')
           $vol = 'RSS';
         else if($match[2] == 'Statutes of Saskatchewan')
           $vol = 'SS';
         else
           continue;
         $r['cite'] = $vol . ' ' . $match[3] . ', c ' . $match[1];
         $r['year'] = $match[3];
      }
      else
        continue;

      // find the pdf link
      $img = $inner_dom->find("td.description img[alt*=Open]",0);
      $redirect_url = urldecode($img->parent()->href);
      if(preg_match('/u\=(.*)/', $redirect_url, $match))
        $r['url_pdf'] = $match[1];
      
      scraperwiki::save($db_index, $r);
}//end for statute vs. reg.
?>



