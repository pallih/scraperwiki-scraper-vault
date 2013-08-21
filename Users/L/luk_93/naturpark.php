<?php

$url = 'http://www.naturparke.de/parks/'; 

######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


for ($i = 1; $i < 3 ; $i++) {
$html = scraperwiki::scrape($url.$i);
print $html;

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find('div[id=box-red] div[class=box-right-content]') as $data)
{
    $name = $data->find('strong');

    $name = $name[0]->plaintext;
    echo($name); 


    $text = $data->find('br');
        echo($text->plaintext);

   # Store data in the datastore
    //print $name->plaintext . "\n";
    //scraperwiki::save(array('str'), array('str' => $str->plaintext));


}

foreach($dom->find('a[class=link-globe]') as $web)
   {
       # Store data in the datastore
        $web = $web->href;
       print $web . "\n";
       //scraperwiki::save(array('plz'), array('plz' => $plz->plaintext));
   }


foreach($dom->find('a[class=link-globe]') as $mail)
   {
       # Store data in the datastore
        $mail= $mail->innertext;
       print $mail. "\n";
       //scraperwiki::save(array('plz'), array('plz' => $plz->plaintext));
   }

//<a class="link-mail" href="mailto:info@naturpark-altmuehltal.de">info@naturpark-altmuehltal.de</a>

/*
$mail = $dom->find('div[id=box-red] div[class=box-right-content] a');
print_r($mail);
*/



}

?>