<?php
require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.webentwickler-jobs.de");
$dom = new simple_html_dom();
$dom->load($html);
$html_el = $dom->find( "div[@id='content'] table",0);           




//alle tr innerhalb der table rausfiltern
foreach ($html_el->find("tr") as $child1) {
   // if( ($child1->children(0)->children(0)->href)  != ""){
    $url = "http://www.indeed.com/". $child1->children(0)->children(0)->href;
    
    //print $url ."\n";

    $subpage = scraperWiki::scrape($url);
    $subdom = new simple_html_dom();
    $subdom->load($subpage);
    
      foreach($subdom->find("div[@id='content']") as $newdata)
      {
        $dds = $newdata->find("dd");
        $h2 = $newdata->find("h2");
        $date = $newdata->find("div[@id='content_footer']");
      
        //get current Date
        $curDate = substr($date[0], -18, -8);
         //get mail
        $match = preg_match('^[a-zA-Z0-9\.\-\_]{2,}@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z]{2,5}^' , $dds[3], $matches);
        
        if($match ==  1)
            $mail = $matches[0];
        else
            $mail = "Not found";

         /* Skills finden und ausgeben (erstmal seeeehr rudimentär!)
         *
         * @param string
         * @return string
         */
            function find_skills($text=""){
        
            $possible_titles = "/(Ihr Profil|Dein Profil|Vorraussetzungen|Was erwarten wir|Wir erwarten|Ihre Kenntnisse|Dein Profil|Anforderungen|Was Sie mitbringen sollten|Ihr Anforderungsprofil|Sie bringen mit|Von Vorteil wären|Was wir uns wünschen|Wir erwarten von Ihnen|Ihre Qualifikation|Gewünschte Qualifikation)(:|\?)?/i";
            $possible_followingtitles = "/(Wir bieten|Was wir bieten|Wir bieten|Es erwartet Sie|Unser Angebot|Das bietet Ihnen)(:|\?)?/i";
        
            $skills = preg_split($possible_titles, $text, NULL); // tauchen die Signalwörter für den Anfang auf?
            $output = preg_split($possible_followingtitles, $skills[1], NULL); // tauchen die Signalwörter für den Ende auf?
            
            return $output[0]; // den Teil zurückgeben, der uns interessiert
            
        }

        //get Skills for current object
        $skills = find_skills($dds[3]);

        //get informations about date, job, firm, contact, phone, mail, place, adress, skills  
        $record = array(
          'date' =>$curDate,
          'job'=> $h2[0]->plaintext,
          'firm'=> $dds[0]->plaintext,
          'contact' => $dds[4]->plaintext,
          'phone' => "Not supported",
          'mail' => $mail,
          'place'=> $dds[1]->plaintext,
          'address' => "Not supported",
          'skills' => $skills
        );
        //print_r($record);
        $message = scraperwiki::save_sqlite(array("date", "job", "firm", "contact", "phone", "mail", "place", "address", "skills"), $record);           
       
        //print json_encode(array("a"),$record);     
      }
      $subdom->__destruct();   
    //}
}   