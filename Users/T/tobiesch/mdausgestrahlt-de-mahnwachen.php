<?php
######################################
# Basic PHP scraper
######################################

#Anti-Atom-Mahnwachen von ausgestrahlt.de

require  'scraperwiki/simple_html_dom.php';

function md_scrape ($url){
    $curl = curl_init ($url );
    curl_setopt ($curl, CURLOPT_RETURNTRANSFER, true);
    $res  = curl_exec ($curl);
    curl_close ($curl);
    return $res;
}

#Änderung für ULR dann muss auch Datum und eventuell Link geändert werden
#$datum = "14.03.2011";
#$html  =  md_scrape("http://maps.google.de/maps/ms?ie=UTF8&hl=de&source=embed&msa=0&output=georss&msid=210032955720989679175.00049e44f048b474277d5");
#$baselink="http://www.ausgestrahlt.de/anti-atom-kette-2011.html";

$datum = "21.03.2011";
$html =  md_scrape("http://maps.google.de/maps/ms?ie=UTF8&hl=de&source=embed&msa=0&output=georss&msid=210032955720989679175.00049e754dabd7cc7cf0c");
$baselink="http://www.ausgestrahlt.de/mitmachen/fukushima.html";

#print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$i=1;
foreach($dom->find('item') as $item)
{
    $ort=$item->getElementByTagName ('title' )->plaintext;
    #$ort=utf8_decode($ort);
    if(($ort == 'Brüssel') | ($ort == 'Salzburg')| ($ort == 'Wien')){
        continue;
    }
    $description=$item->getElementByTagName ('description' )->innertext;
    $description=preg_replace('/<!\[CDATA\[<div dir=\"ltr\">(.*)<\/div>\]\]>/', '${1}', $description);
    $description='Anti-Atom Mahnwache in ' . $ort . "<br />" . $description;
    $georss=$item->getElementByTagName ('georss:point' )->plaintext;
    $zuordnung='Ort';
    $author='ausgestrahlt.de';
    #add location as anchor to link - does not do anything on the site but helps to keep it distinct in meine-demokratie.de database
    $link=$baselink . '#' . $ort ."-".$datum;
    #print $ort . "\n";
    #print $item . "\n";

    # Store data in the datastore
    #unique identification via title (includes location) and link
    #there are some events at the same place but these seem most of the time refer to updates of previous ones so just overwrite
    scraperwiki::save(array('title'), 
            array('md:address' => $ort,
                  'title' => 'Anti-Atom Mahnwache in ' . $ort . ' (' . $datum . ')',
                  'georss:point' => $georss,
                  'md:zuordnung' => $zuordnung,
                  'md:author' => $author,
                  'description' => $description,
                  'category' => 'Demonstration',
                  'md:tag1' => 'Mahnwache',
                  'md:tag2' => 'Atomkraft',
                  'md:start_date' => $datum . ' 18:00:00',
                  'md:expiration_date' => $datum . ' 20:00:00',
                  'guid' => $link,
                  'date' => $datum
                    )
    );
    $i++;
    #if($i >10){    
    #    exit;
    #}

}

?>