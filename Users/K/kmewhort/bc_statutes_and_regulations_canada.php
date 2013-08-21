<?php
error_reporting(E_ERROR);
require 'scraperwiki/simple_html_dom.php';

/* globals */
$db_index = array('cite');
$base_url = 'http://www.bclaws.ca';
$index_url = $base_url . '/EPLibraries/bclaws_new/content?xsl=/templates/toc.xsl/group=%s/lastsearch=/l'; // %s = index (A-Z);
$start_index = 'A';


/* execution */

// for each index from A-Z (plus '#')
foreach(range($start_index,'Z') as $a){
    // load the list of legislation
    $html_content = scraperwiki::scrape(sprintf($index_url, $a));
    if(empty($html_content))
      continue;
    $dom = str_get_html($html_content);
    if(!$dom)
       continue;
   
    // for each statute/reg
    foreach($dom->find("#legis tr") as $row){
      $r = array('jurisdiction' => 'bc');
 
      // if the row is a statute
      if($row->find("td.act",0)){
         $item = $row->find("td.act a",1);
         $title_and_cite = $item->plaintext;
         $cite_start = strrpos($title_and_cite, '[');
         if($cite_start === false)
           continue;
         $r['title'] = substr($title_and_cite, 0, $cite_start);
         $r['cite'] = preg_replace('/]/', ',', substr($title_and_cite, $cite_start+1));
         $r['type'] = 'statute';
         $r['url_html'] = $base_url . $item->href;

         // extract year from the citation
         if(preg_match('/(\d{4})\,/', $r['cite'], $match))
           $r['year'] = $match[1];
      }
      // if the row is a regulation
      else if($row->find("td.stat_reg",0)){
         $item = $row->find("td.stat_reg a",1);
         $title_and_cite = $item->plaintext;
         $title_start = strrpos($title_and_cite, ':');
         if($title_start === false)
           continue;
         $r['cite'] = 'BC Reg ' . substr($title_and_cite, 0, $title_start);
         $r['title'] = substr($title_and_cite, $title_start+1);
         $r['type'] = 'regulation';
         $r['url_html'] = $base_url . $item->href;

        // extract year from the citation
        if(preg_match('/\/(\d{4})/', $r['cite'], $match))
          $r['year'] = $match[1];
        else if(preg_match('/\/(\d{2})/', $r['cite'], $match))
          $r['year'] = '19' . $match[1];
      }
      else
        continue;
      
      scraperwiki::save($db_index, $r);
    }// end for each statute/reg
}// end for each A-Z index
?>



