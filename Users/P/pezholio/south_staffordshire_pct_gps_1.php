<?php
require 'scraperwiki/simple_html_dom.php';  

function IsPostcode($postcode) {
$postcode = strtoupper($postcode);
$pattern = "((GIR 0AA)|(TDCU 1ZZ)|(ASCN 1ZZ)|(BIQQ 1ZZ)|(BBND 1ZZ)"
."|(FIQQ 1ZZ)|(PCRN 1ZZ)|(STHL 1ZZ)|(SIQQ 1ZZ)|(TKCA 1ZZ)"
."|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]"
."|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))"
."|[0-9][A-HJKS-UW])( {0,1})[0-9][ABD-HJLNP-UW-Z]{2})"; 
   
    if(preg_match($pattern, $postcode, $matches)) {
        return $matches[0];
    } else {
        return FALSE;
    }
}

for ($i = 1; $i <= 5; $i++) {
    $html = scraperWiki::scrape("http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=3092%2c4117&TreatmentID=0&PageNumber=".$i."&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=WS13+6YY&DistanceFrom=10&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters="); 

    $dom = new simple_html_dom();
    $dom->load($html);
    
    $panels = $dom->find('.organisation');

    foreach ($panels as $panel) {
        $name = $panel->find('h2.notranslate', 0);
        $url = "http://www.nhs.uk". $name->find('a', 0)->href;
        $name = $name->plaintext;
        $address = $panel->find('.address .first-item', 0)->plaintext;
        $postcode = IsPostcode($address);
        $postcode = str_replace(" ", "", strtoupper($postcode));
        $latlng = json_decode(file_get_contents("http://www.uk-postcodes.com/postcode/". $postcode .".json"));
    
        $data = array (
                'name' => $name,
                'url' => $url,
                'address' => $address,
                'postcode' => $postcode,
                'lat' => $latlng->geo->lat,
                'lng' => $latlng->geo->lng
        );
                
        scraperwiki::save_sqlite(array('url'), $data); 
    }
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';  

function IsPostcode($postcode) {
$postcode = strtoupper($postcode);
$pattern = "((GIR 0AA)|(TDCU 1ZZ)|(ASCN 1ZZ)|(BIQQ 1ZZ)|(BBND 1ZZ)"
."|(FIQQ 1ZZ)|(PCRN 1ZZ)|(STHL 1ZZ)|(SIQQ 1ZZ)|(TKCA 1ZZ)"
."|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]"
."|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))"
."|[0-9][A-HJKS-UW])( {0,1})[0-9][ABD-HJLNP-UW-Z]{2})"; 
   
    if(preg_match($pattern, $postcode, $matches)) {
        return $matches[0];
    } else {
        return FALSE;
    }
}

for ($i = 1; $i <= 5; $i++) {
    $html = scraperWiki::scrape("http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=3092%2c4117&TreatmentID=0&PageNumber=".$i."&PageSize=0&TabId=30&SortType=1&LookupType=1&LocationType=1&SearchTerm=WS13+6YY&DistanceFrom=10&SortByMetric=0&TrustCode=&TrustName=&DisambiguatedSearchTerm=&LookupTypeWasSwitched=False&MatchedOrganisationPostcode=&MatchedOrganisationCoords=&ServiceIDs=&ScorecardTypeCode=&NoneEnglishCountry=&HasMultipleNames=False&OriginalLookupType=1&ServiceLaunchFrom=&Filters=&TopLevelFilters="); 

    $dom = new simple_html_dom();
    $dom->load($html);
    
    $panels = $dom->find('.organisation');

    foreach ($panels as $panel) {
        $name = $panel->find('h2.notranslate', 0);
        $url = "http://www.nhs.uk". $name->find('a', 0)->href;
        $name = $name->plaintext;
        $address = $panel->find('.address .first-item', 0)->plaintext;
        $postcode = IsPostcode($address);
        $postcode = str_replace(" ", "", strtoupper($postcode));
        $latlng = json_decode(file_get_contents("http://www.uk-postcodes.com/postcode/". $postcode .".json"));
    
        $data = array (
                'name' => $name,
                'url' => $url,
                'address' => $address,
                'postcode' => $postcode,
                'lat' => $latlng->geo->lat,
                'lng' => $latlng->geo->lng
        );
                
        scraperwiki::save_sqlite(array('url'), $data); 
    }
}
?>
