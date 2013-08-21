<?php

require 'scraperwiki/simple_html_dom.php';

  $html = scraperWiki::scrape("http://drupal.org/project/modules/index?project-status=0&drupal_core=103");
  $dom = new simple_html_dom();
  $dom->load($html);
  $i = 0;
  foreach($dom->find("div[@class='view-content'] ol li a") as $data) {
    if (stristr($data->plaintext,"commerce ") || stristr(strtolower($data->plaintext)," commerce") || stristr($data->href,"commerce_") || stristr($data->href,"_commerce") || stristr($data->href,"_dc") || stristr($data->href,"dc_")) {
      if ($data->plaintext != "Drupal Commerce") {
      //print($data->plaintext." - ".$data->href."\n");
      $i++;
}
    }
  }
  print($i." Commerce Modules found");
  
  $html = scraperWiki::scrape("http://drupal.org/project/modules/index?project-status=1&drupal_core=All");
  $dom = new simple_html_dom();
  $dom->load($html);
  $i = 0;
  foreach($dom->find("div[@class='view-content'] ol li a") as $data) {
    if (stripos($data->plaintext,"commerce")) {
      print($data->plaintext." - ".$data->href."\n");
      $i++;
    }
  }
  print($i." Commerce Sandboxes found");
?>
