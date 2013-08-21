<?php
    require 'scraperwiki/simple_html_dom.php';
$urls[] ='http://www.opentable.com/info/banquets.aspx?m=3';
$urls[] ='http://www.opentable.com/chicago-bachelorette-party-places';
$urls[] ='http://www.opentable.com/chicago-birthday-party-venues';
$urls[] ='http://www.opentable.com/chicago-christmas-party-venues';
$urls[] ='http://www.opentable.com/chicago-graduation-party-places';
$urls[] ='http://www.opentable.com/chicago-graduation-party-places';
$urls[] ='http://www.opentable.com/chicago-wedding-reception-venues';

foreach($urls as $url){
    $html = scraperWiki::scrape($url); 
           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("tr") as $row){
       $url = $row->find('a.GDRNmLk');
       $venueHtml = scraperWiki::scrape($url[0]->href);
        $domInner = new simple_html_dom();
        $domInner->load($venueHtml); 
        $name = $domInner->find('h1.RestProfileTitle span');
        $description = $domInner->find('#RestaurantProfile_RestProfileGroupDiningTab_lblPrivateDiningContent, #RestaurantProfile_RestaurantProfileInfo_lblDescription');
        //$type = $domInner->find('#Header_trType td');
        $location = $domInner->find('div.RestProfileAddress span');
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
            'type'=>'Restaruant',//$type[0]->innertext,
            'description' =>$description[0]->innertext
        );
        scraperwiki::save(array('name'), $record); 
    }

}

?>
