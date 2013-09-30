<?php
/* SETTINGS */

require 'scraperwiki/simple_html_dom.php'; 
$source="http://www.driesbultynck.be";
$utmSource="";
$utmMedium="";
$utmTerm="";
$utmContent="";
$utmCampaign="";

scrape($source);

function scrape($source){
    global $source, $utmSource, $utmMedium, $utmTerm, $utmContent, $utmCampaign;
            $link = scraperwiki::scrape($source);
            $html = str_get_html($link);   
        foreach ($html->find('a[href]') as $a) {
            $href = $a->href;
            $a->href = $href.'#utm_source='.$utmSource.'&utm_medium='.$utmMedium.'&utm_term='.$utmTerm.'&utm_content='.$utmContent.'&utm_campaign='.$utmCampaign;
        } 
print $html;            
}


?>
<?php
/* SETTINGS */

require 'scraperwiki/simple_html_dom.php'; 
$source="http://www.driesbultynck.be";
$utmSource="";
$utmMedium="";
$utmTerm="";
$utmContent="";
$utmCampaign="";

scrape($source);

function scrape($source){
    global $source, $utmSource, $utmMedium, $utmTerm, $utmContent, $utmCampaign;
            $link = scraperwiki::scrape($source);
            $html = str_get_html($link);   
        foreach ($html->find('a[href]') as $a) {
            $href = $a->href;
            $a->href = $href.'#utm_source='.$utmSource.'&utm_medium='.$utmMedium.'&utm_term='.$utmTerm.'&utm_content='.$utmContent.'&utm_campaign='.$utmCampaign;
        } 
print $html;            
}


?>
