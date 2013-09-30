<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.webentwickler-jobs.de");
$dom = new simple_html_dom();
$dom->load($html);
$html_el = $dom->find( "div[@id='content'] table",0);           

//alle tr innerhalb der table rausfiltern
foreach ($html_el->find("tr") as $child1) {

    $url = "http://www.webentwickler-jobs.de". $child1->children(0)->children(0)->href;

    $subpage = scraperWiki::scrape($url);
    $subdom = new simple_html_dom();
    $subdom->load($subpage);
    
      foreach($subdom->find("div[@id='content']") as $newdata)
      {
        $dds = $newdata->find("dd");
        $h2 = $newdata->find("h2");
        $datesrc = $newdata->find("div[@id='content_footer']");
        $curDate = substr($datesrc[0], -18, -8);

        //get mail
        $match = preg_match('^[a-zA-Z0-9\.\-\_]{2,}@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z]{2,5}^' , $dds[3], $matches);      
        if($match ==  1)
            $email = $matches[0];
        else
            $email = "";
    
        // Nur weitermachen, wenn es ein Datum gibt:
        if(!empty($curDate)){

            // Daten aufbereiten:
            $job = strip_tags($h2[0]->plaintext);
            $company = strip_tags($dds[0]->plaintext);
            $contact = strip_tags($dds[4]->plaintext);
            $city = strip_tags($dds[1]->plaintext);
            $text = strip_tags($dds[3]);

            //get informations:
            $record = array(
              'url' => $url, 
              'date' => $curDate,
              'job' => $job,
              'company' => $company,
              'contact' => $contact,
              'email' => $email,
              'city' => $city,
              'text' => $text
            );

            $message = scraperwiki::save_sqlite(array("url", "date", "job", "company", "contact", "email", "city", "text"), $record);      
        }
      }
      $subdom->__destruct();

}   <?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.webentwickler-jobs.de");
$dom = new simple_html_dom();
$dom->load($html);
$html_el = $dom->find( "div[@id='content'] table",0);           

//alle tr innerhalb der table rausfiltern
foreach ($html_el->find("tr") as $child1) {

    $url = "http://www.webentwickler-jobs.de". $child1->children(0)->children(0)->href;

    $subpage = scraperWiki::scrape($url);
    $subdom = new simple_html_dom();
    $subdom->load($subpage);
    
      foreach($subdom->find("div[@id='content']") as $newdata)
      {
        $dds = $newdata->find("dd");
        $h2 = $newdata->find("h2");
        $datesrc = $newdata->find("div[@id='content_footer']");
        $curDate = substr($datesrc[0], -18, -8);

        //get mail
        $match = preg_match('^[a-zA-Z0-9\.\-\_]{2,}@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z]{2,5}^' , $dds[3], $matches);      
        if($match ==  1)
            $email = $matches[0];
        else
            $email = "";
    
        // Nur weitermachen, wenn es ein Datum gibt:
        if(!empty($curDate)){

            // Daten aufbereiten:
            $job = strip_tags($h2[0]->plaintext);
            $company = strip_tags($dds[0]->plaintext);
            $contact = strip_tags($dds[4]->plaintext);
            $city = strip_tags($dds[1]->plaintext);
            $text = strip_tags($dds[3]);

            //get informations:
            $record = array(
              'url' => $url, 
              'date' => $curDate,
              'job' => $job,
              'company' => $company,
              'contact' => $contact,
              'email' => $email,
              'city' => $city,
              'text' => $text
            );

            $message = scraperwiki::save_sqlite(array("url", "date", "job", "company", "contact", "email", "city", "text"), $record);      
        }
      }
      $subdom->__destruct();

}   