<?php
//Fork of my Planning Application scraper, this time for appeals. Props goes to my awesome girlfriend for being awesome.

if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
        $data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz"); 
        file_put_contents("simpletest.tar.gz", $data);
        exec('tar -xzvf simpletest.tar.gz');
}
/*if (!file_exists('phpcoord-2.3.php')){ //next need to download phpCoord
        $data2 = file_get_contents("http://www.jstott.me.uk/phpcoord/phpcoord-2.3.tar.gz"); 
        file_put_contents("phpcoord-2.3.tar.gz", $data2);
        exec('tar -xzvf phpcoord-2.3.tar.gz');
}*/
    require_once('simpletest/browser.php'); //Here we go now!
   // require_once('phpcoord-2.3.php');  PHPcoord commented out because there is no easting/westing data for Hackney appeals!
    $browser = new SimpleBrowser();
    $browser->useCookies();
    $browser->get('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/AppealsSearch.aspx?blah='.rand(1,99)); //the "blah" flag disables caching on SW.
    $viewstate = $browser->getField('__VIEWSTATE');
    $eventValidation = $browser->getField('__EVENTVALIDATION');
    $browser->setField('__VIEWSTATE', $viewstate);
    $browser->setField('__EVENTVALIDATION', $eventValidation);
    $browser->setField('cboSelectDateValue', 'DATE_RECEIVED');
    $browser->setField('cboMonths', '1');    
    $browser->setField('rbGroup', 'rbMonth');
    $browser->setField('cboDays', '7');
    $browser->clickSubmitByName('csbtnSearch');
    $url = $browser->getUrl();
    $xmlloc = 'http://apps.hackney.gov.uk' . preg_replace('/.*XMLLoc=(.*)$/', '\1', $url);
    $apps = simplexml_load_file($xmlloc);
    foreach ($apps->M3_AP_APPEALS_QUERY_LIST as $app){
    $regex = "/([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)/"; //useful -- regex for all UK postcodes
    $address = (string) $app->SITE_ADDRESS;
    preg_match($regex, $address, $matches);
    if(isset($matches[0])){
        $coords = scraperwiki::gb_postcode_to_latlng($matches[0]);
    }
        $appscrape = scraperwiki::scrape('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$app->PK.'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetailsAppealCosts.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
        preg_match('/<span>Wards<\/span>(.*)<\/div>/i', $appscrape, $wardmatches);


        $rows[] = array(       
            "PK" => integer $app->PK,
            "Appeal Description" => string $app->APPEAL_DESCRIPTION,
            "Appeal Received Date" => string $app->DATE_APPEAL_RECEIVED,
            "Appeal Start Date" => string $app->DATE_APPEAL_START,
            "Local Authority Reference" => string $app->LOCAL_AUTHORITY_REFERENCE,
            "Site Address" => string $app->SITE_ADDRESS,
            "Restricted" => string $app->RESTRICTED,
            "Latitude" => $coords[0],
            "Longitude" => $coords[1],
            "Wards" => string $wardmatches[1]
);
    }
    $unique_keys = array("PK");
    $table = "Planning_Appeals";
    if (isset($rows)){ 
        scraperwiki::save_sqlite($unique_keys, $rows, $table);
    }
 // print_r($rows);
?><?php
//Fork of my Planning Application scraper, this time for appeals. Props goes to my awesome girlfriend for being awesome.

if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
        $data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz"); 
        file_put_contents("simpletest.tar.gz", $data);
        exec('tar -xzvf simpletest.tar.gz');
}
/*if (!file_exists('phpcoord-2.3.php')){ //next need to download phpCoord
        $data2 = file_get_contents("http://www.jstott.me.uk/phpcoord/phpcoord-2.3.tar.gz"); 
        file_put_contents("phpcoord-2.3.tar.gz", $data2);
        exec('tar -xzvf phpcoord-2.3.tar.gz');
}*/
    require_once('simpletest/browser.php'); //Here we go now!
   // require_once('phpcoord-2.3.php');  PHPcoord commented out because there is no easting/westing data for Hackney appeals!
    $browser = new SimpleBrowser();
    $browser->useCookies();
    $browser->get('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/AppealsSearch.aspx?blah='.rand(1,99)); //the "blah" flag disables caching on SW.
    $viewstate = $browser->getField('__VIEWSTATE');
    $eventValidation = $browser->getField('__EVENTVALIDATION');
    $browser->setField('__VIEWSTATE', $viewstate);
    $browser->setField('__EVENTVALIDATION', $eventValidation);
    $browser->setField('cboSelectDateValue', 'DATE_RECEIVED');
    $browser->setField('cboMonths', '1');    
    $browser->setField('rbGroup', 'rbMonth');
    $browser->setField('cboDays', '7');
    $browser->clickSubmitByName('csbtnSearch');
    $url = $browser->getUrl();
    $xmlloc = 'http://apps.hackney.gov.uk' . preg_replace('/.*XMLLoc=(.*)$/', '\1', $url);
    $apps = simplexml_load_file($xmlloc);
    foreach ($apps->M3_AP_APPEALS_QUERY_LIST as $app){
    $regex = "/([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)/"; //useful -- regex for all UK postcodes
    $address = (string) $app->SITE_ADDRESS;
    preg_match($regex, $address, $matches);
    if(isset($matches[0])){
        $coords = scraperwiki::gb_postcode_to_latlng($matches[0]);
    }
        $appscrape = scraperwiki::scrape('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$app->PK.'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetailsAppealCosts.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
        preg_match('/<span>Wards<\/span>(.*)<\/div>/i', $appscrape, $wardmatches);


        $rows[] = array(       
            "PK" => integer $app->PK,
            "Appeal Description" => string $app->APPEAL_DESCRIPTION,
            "Appeal Received Date" => string $app->DATE_APPEAL_RECEIVED,
            "Appeal Start Date" => string $app->DATE_APPEAL_START,
            "Local Authority Reference" => string $app->LOCAL_AUTHORITY_REFERENCE,
            "Site Address" => string $app->SITE_ADDRESS,
            "Restricted" => string $app->RESTRICTED,
            "Latitude" => $coords[0],
            "Longitude" => $coords[1],
            "Wards" => string $wardmatches[1]
);
    }
    $unique_keys = array("PK");
    $table = "Planning_Appeals";
    if (isset($rows)){ 
        scraperwiki::save_sqlite($unique_keys, $rows, $table);
    }
 // print_r($rows);
?>