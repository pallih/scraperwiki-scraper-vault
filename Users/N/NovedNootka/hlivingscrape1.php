<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$url = 'http://www.harbourliving.ca/central-island/rss/';
$rawFeed = file_get_contents($url); 

$rss = new SimpleXMLElement($rawFeed);
$currentlink = "";
$locationcol = false;
$address = "";
$event = "";
$description = "";
foreach ($rss->channel->item as $item )
{
    $currentlink = $item->link;
    $title = $item->title;
    $desc = $item->description;
    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($currentlink);
    $dom->load($html);    
    foreach($dom->find('table td') as $data)
    {       
        if ($locationcol)
        {
            $address = $data->plaintext;
            if (!strpos($address, "</td>") === false)
                $address = substr($address, 0, strpos($address, "</td>"));
            //$address = "Argh";
            //print $address . "\n";
            $locationcol = false;
            break;
        }
        if($data->plaintext =="Location:")
        {
            $locationcol = true;
        }
    }
    //Get the lat long for the address
    //First convert the address
    $htmaddress = urlencode($address);
    //Then pass it into the geocoder
    $geocode = "http://maps.google.com/maps/geo?q=".$htmaddress."&output=xml";
    $page = file_get_contents($geocode);     

    print $title . "\n";
    print $desc . "\n";
    print $address . "\n";
    print $currentlink . "\n";
    print $page . "\n\n";

}

?>