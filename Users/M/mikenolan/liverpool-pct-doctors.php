<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.nhs.uk/ServiceDirectories/Pages/Trust.aspx?id=5NL&v=2&pid=5NL');
print $html;
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('dt') as $data)
{
    $address = $data->next_sibling()->plaintext;
    $exp = explode(',', $address);
    $pc = array_pop($exp);
    //print $pc. "\n";
    print "\n";
    $ll = scraperwiki::gb_postcode_to_latlng($pc);
    //$ll['lat'] = $ll[0];
    //$ll['lng'] = $ll[1];
    $url = 'http://www.nhs.uk'.$data->first_child()->href;
    
    /*
    $doctor = scraperwiki::scrape($url);
    $docdom = new simple_html_dom();
    $docdom->load($doctor);
    $dd = $docdom->find('ul[class=dr-list]', 0);
    
    if ($dd && $dd->children()) 
    {
        $numdocs = sizeof($dd->children());
    } else
    {
        $numdocs = 0;
    }
    */
    

    scraperwiki::save(array('title', 'content', 'link'), array('title' => $data->first_child()->plaintext, 'link' => $url, 'content' => $address, 'postcode' => $pc, 'doctors' => $numdocs, 'georss:point' => $ll[0].' '.$ll[1]), null, $ll);
    unset($docdom);
}

?>