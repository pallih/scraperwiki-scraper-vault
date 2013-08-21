<?php
require 'scraperwiki/simple_html_dom.php';  


for ($i = 1; $i <= 5; $i++) {
    $urlstring = "http://www.nhs.uk/Scorecard/Pages/Results.aspx?OrgType=1&Coords=1619%2c3735&SortType=1&DistanceFrom=-1&TabId=300&PageNumber=".$i;
    $html = scraperWiki::scrape($urlstring);
    #echo $urlstring . "\n";
    $dom = new simple_html_dom();
    $dom->load($html);
    
    $panels = $dom->find('div.organisation-wrapper');

    foreach ($panels as $panel) {
        $name = $panel->find('h2.notranslate a', 0);
        $url = $name->href;
        #echo $url . "\n";        
        $name = $name->plaintext;
        #echo $name . "\n";
        #$address = $panel->find('li.first-item', 0)->plaintext;
        #echo $address . "\n";

            $Suburlstring = "http://www.nhs.uk".$url;
            $subhtml = scraperWiki::scrape($Suburlstring);
            echo $Suburlstring . "\n";
            $subdom = new simple_html_dom();
            $subdom->load($subhtml);
            $address = $subdom->find('p.notranslate', 0)->plaintext;
              
            $web = $subdom->find('#ctl00_PlaceHolderMain_MainContent_MainContent1_GPPageLayoutRow2_DisplayBranches1_rptBranch_ctl00_ucDisplayMainDetail_pnlWebsite a', 0)->href;
            if (empty($web))
                $web = null;
            
            #$subname = $subpanels->find('div.ctl00_PlaceHolderMain_MainContent_MainContent1_GPPageLayoutRow2_DisplayBranches1_rptBranch_ctl00_pnlMainTitle p', 0);
            #$subaddress = $subpanels->innertext;
            echo $web . "\n";

  
        $data = array (
                'name' => $name,
                'url' => $url,
                'address' => $address,
                'website' => $web
        #        'postcode' => $postcode,
        #        'lat' => $latlng->geo->lat,
        #        'lng' => $latlng->geo->lng
        );
                
        scraperwiki::save(array('url'), $data); 
    }
}
?>
