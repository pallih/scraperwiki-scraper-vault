<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.webentwickler-jobs.de");
$dom = new simple_html_dom();
$dom->load($html);
$html_el = $dom->find( "div[@id='content'] table",0);           

print_r(scraperwiki::show_tables()); 


//alle tr innerhalb der table rausfiltern
foreach ($html_el->find("tr") as $child1) {
   // if( ($child1->children(0)->children(0)->href)  != ""){
    $url = "http://www.webentwickler-jobs.de". $child1->children(0)->children(0)->href;
    
    //print $url ."\n";

    $subpage = scraperWiki::scrape($url);
    $subdom = new simple_html_dom();
    $subdom->load($subpage);
    
      foreach($subdom->find("div[@id='content']") as $newdata)
      {
        $dds = $newdata->find("dd");
        $h2 = $newdata->find("h2");
        $date = $newdata->find("div[@id='content_footer']");
      


         //get mail
        $match = preg_match('^[a-zA-Z0-9\.\-\_]{2,}@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z]{2,5}^' , $dds[3], $matches);
        
        if($match ==  1)
            $mail = $matches[0];
        else
            $mail = "";


        //get informations about date, job, firm, contact, phone, mail, place, adress, skills  
        $record = array(
          'date' => $date[0],
          'job'=> $h2[0]->plaintext,
          'firm'=> $dds[0]->plaintext,
          'contact' => $dds[4]->plaintext,
          'phone' => "-",
          'mail' => $mail,
          'place'=> $dds[1]->plaintext,
          'address' => "-",
          'skills' => $dds[3]
        );
        //print_r($record);
        $message = scraperwiki::save_sqlite(array("date", "job", "firm", "contact", "phone", "mail", "place", "address", "skills"), $record);           
       
        //print json_encode(array("a"),$record);     
      }
      $subdom->__destruct();   
    //}
}   
