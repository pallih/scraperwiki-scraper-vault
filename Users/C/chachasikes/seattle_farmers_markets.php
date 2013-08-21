<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.wafarmersmarkets.com/washingtonfarmersmarketdirectory.php");
print $html;


# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);
$record = array();

foreach($dom->find('div#list tr td') as $row) {
    $market = split('<br />', cleanup($row));
    $name = cleanup($market[0]);
    $record['name'] = strip_tags($name);
    $record['address'] = cleanup($market[1]);

    $date = split(',', cleanup($market[2]));   
    $record['day_of_week'] = $date[0];
    $record['time'] = $date[1];
    $record['season'] = $date[2];

    $record['payment_method'] = $market[3];
    // @TODO This is not splitting well, needs to actually split on the last space.
    $contact = explode(' ', $market[4]);
    if(count($contact > 0)){
        $record['contact_phone'] = array_pop($contact);  
        $record['contact_name'] = implode(' ', $contact);
    }


    if($market[6] != null){
        $record['website'] = strip_tags($market[5]);
        $record['contact_email'] = strip_tags($market[6]);   

    }
    else {  
        $record['website'] = '';
        $record['contact_email'] = strip_tags($market[5]); 
    }
print_r($record);
   scraperwiki::save(array('name', 'address', 'day_of_week', 'time', 'season', 'payment_method', 'contact_phone', 'contact_name', 'website', 'contact_email'), $record);

}
    

function cleanup($data){
    $data = trim($data);
    return $data;
}
?>