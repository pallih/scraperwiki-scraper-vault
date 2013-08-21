<?php

require  'scraperwiki/simple_html_dom.php';

# At the end of the last tutorial we had downloaded the text of
for ($pn = 1; $pn < 6; $pn++) 
{
    $url = "http://en.600024.com/musicdirector/ar-rahman-movies-list/page/".$pn."/";
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find('div[class="movietitle"]') as $data)
    {
        //print "Hello, coding in the cloud!";
        //print $data->href;
        $divs = $data->find("a");
        //print $divs[0]->href;
        $url2 = trim($divs[0]->href);
        //print $url2;
        $html2 = scraperwiki::scrape($url2);
        $dom2 = new simple_html_dom();
        $dom2->load($html2);
        foreach($dom2->find('td[class="model"]') as $data2)
        {
           $detail = $data2->find('span');
           $label  = $data2->find('label');
           print trim($label[2]->plaintext);
    
           //$mname  = trim($detail[0]->plaintext);
           //$dname  = trim($detail[1]->plaintext);
           //$mdname = trim($detail[2]->plaintext);
           //$prod   = trim($detail[3]->plaintext);
           //$rel_year= trim($detail[4]->plaintext);

           print "\n"; 
           $record = array(trim($label[0]->plaintext)=>trim($detail[0]->plaintext),trim($label[1]->plaintext)=>trim($detail[1]->plaintext),trim($label[2]->plaintext)=>trim($detail[2]->plaintext),trim($label[3]->plaintext)=>trim($detail[3]->plaintext),trim($label[4]->plaintext)=>trim($detail[4]->plaintext)); 
           scraperwiki::save_sqlite(array(trim($label[0]->plaintext),trim($label[1]->plaintext),trim($label[2]->plaintext),trim($label[3]->plaintext),trim($label[4]->plaintext)),$record,"ARRahmanDB");

           //$record = array('MovieName'=>$mname,'Director'=>$dname,'MusicDirector'=>$mdname,'Production'=>$prod,'Release'=>$rel_year); 
           //scraperwiki::save_sqlite(array("MovieName","Director","MusicDirector","Production","Release"),$record,"ARRahmanDB");
            
        }
   }
}
  
?>


