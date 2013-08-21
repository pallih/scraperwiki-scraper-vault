<?php
    require 'scraperwiki/simple_html_dom.php';

for($i = 96; $i< 98; $i++){
    $html = scraperWiki::scrape("http://www.cvent.com/RFP/venues.aspx?ma=80&csn=1&amp;wt.mc_id=CSN_Search_Homepage&vtt=16&pnum=$i");           
    
           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.result") as $row){
       $url = $row->find('a');
       $venueHtml = scraperWiki::scrape("http://www.cvent.com".$url[0]->href);
        $domInner = new simple_html_dom();
        $domInner->load($venueHtml); 
        $name = $domInner->find('h1');
        $description = $domInner->find('#ctl05_UpdatePanelDescription pre');
        $type = $domInner->find('#Header_trType td');
        $location = $domInner->find('table[summary="Venue Address"] th');
        $parts = explode("<br/>", $location[0]->innertext); 
        $addr2 = '';
        $city_state = $parts[1];
        if(count($parts)==4){
            $addr2 = $parts[1];
            $city_state = $parts[2];
        }
        //print_r($city_state);
        preg_match("/([^,]+),\s*(\w+)\s*(\d{5}(?:-\d{4})?)/", $city_state, $matches);

       list($arr['addr'], $arr['city'], $arr['state'], $arr['zip']) = $matches;
        //print_r($arr);
        $record = array(
            'name' => $name[0]->innertext,
            'address1' =>$parts[0],
            'address2' =>$addr2,
            'city'=>$arr['city'],
            'state'=>$arr['state'],
            'zip'=>$arr['zip'],
            'type'=>$type[0]->innertext,
            'description' =>$description[0]->innertext
        );
        scraperwiki::save(array('name'), $record); 
    }

}

?>
