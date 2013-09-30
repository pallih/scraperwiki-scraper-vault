<?php

require 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('Australia/Sydney');

info('Scraping foodauthority.nsw.gov.au...');

$html = scraperwiki::scrape('http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results');

info('Parsing HTML...');

$dom = new simple_html_dom();
$dom->load($html);

info('Parsing penalties...');

foreach($dom->find("#myTable tr") as $tr)
{
    $tds = $tr->find("td");

    $td_count = count($tds);
    if ($td_count != 7)
    {
        info("WARNING: Unexpected TD count: $td_count");
        continue;
    }
    
    $id = $tds[3]->plaintext;
    if ($id == '')
    {
        info("WARNING: Skipping row without ID...");
        continue;
    }

    if (scraperwiki::select("* from swdata where `id`='$id'"))
    {
        info("Skipping existing record $id...\n");
    } 
    else
    {
        $a = $tds[3]->find("a", 0);

        $date = $tds[4]->plaintext;
        $party_served = $tds[5]->plaintext;
        $trade_name = trim($tds[0]->plaintext);

        if ($trade_name == '' || $trade_name == '(NO TRADING NAME)')
            $trade_name = $party_served;

        $details_link = 'http://www.foodauthority.nsw.gov.au/penalty-notices/' . html_entity_decode($a->href);

        info("Fetching details ($id)...");

        $details_html = scraperwiki::scrape($details_link);
        $details_dom = new simple_html_dom();
        $details_dom->load($details_html);

        foreach($details_dom->find(".table-data-pd tr") as $details_tr)
        {
            $details_tds = $details_tr->find("td");

            switch (trim($details_tds[0]->plaintext))
            {
                case "Address\r\n(where offence occurred)":
                    $address = str_replace('/', ' ', trim($details_tds[1]->plaintext));
                    break;
                case 'Offence code':
                    $code = $details_tds[1]->plaintext;
                    break;
                case 'Amount of penalty':
                    $penalty = $details_tds[1]->plaintext;
                    break;
                case "Date penalty notice served\r\n(yyyy-mm-dd)":
                    $date_served = $details_tds[1]->plaintext;
                    if ($date_served == '-00-00')
                        $date_served = $date;
                    break;
                case 'Issued by':
                    $issued_by = $details_tds[1]->plaintext;
                    break;
            }
        }

        if ($address != '')
        {
            info("Fetching location ($address)...");

            $location_link = 'http://dev.virtualearth.net/REST/v1/Locations/AU/NSW/-/' . rawurlencode($address) . '?o=xml&key=Ar8AQgvFLU5GzfH9UXHzxFqme59PPjzN3mtd4azFC0ty73fGzyF-WNyhgl1MpuBL';
            $location_xml = scraperwiki::scrape($location_link);

            if ($location_xml != '')
            {
                $response = new SimpleXMLElement($location_xml);
                $point = $response->ResourceSets->ResourceSet->Resources->Location->Point;
                
                $latitude = $point->Latitude;
                $longitude = $point->Longitude;
            }
        }

        $penalty = array(
            'trade_name'   => $trade_name,
            'suburb'       => $tds[1]->plaintext,
            'council'      => $tds[2]->plaintext,
            'id'           => $tds[3]->plaintext,
            'notice'       => html_entity_decode($a->title),
            'date'         => $date,
            'party_served' => $party_served,
            'notes'        => $tds[6]->plaintext,
            'details_link' => $details_link,
            'address'      => $address,
            'code'         => $code,
            'penalty'      => $penalty,
            'date_served'  => $date_served,
            'issued_by'    => $issued_by,
            'latitude'     => (string)$latitude,
            'longitude'    => (string)$longitude,
            'date_scraped' => date('Y-m-d')
        );
    
        info("Saving new record $id...");

        scraperwiki::save_sqlite(array('id'), $penalty);
    }
}

function info($message)
{
    print '[' . date('Y-M-d H:m:s') . "] $message\n";
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';

date_default_timezone_set('Australia/Sydney');

info('Scraping foodauthority.nsw.gov.au...');

$html = scraperwiki::scrape('http://www.foodauthority.nsw.gov.au/penalty-notices/default.aspx?template=results');

info('Parsing HTML...');

$dom = new simple_html_dom();
$dom->load($html);

info('Parsing penalties...');

foreach($dom->find("#myTable tr") as $tr)
{
    $tds = $tr->find("td");

    $td_count = count($tds);
    if ($td_count != 7)
    {
        info("WARNING: Unexpected TD count: $td_count");
        continue;
    }
    
    $id = $tds[3]->plaintext;
    if ($id == '')
    {
        info("WARNING: Skipping row without ID...");
        continue;
    }

    if (scraperwiki::select("* from swdata where `id`='$id'"))
    {
        info("Skipping existing record $id...\n");
    } 
    else
    {
        $a = $tds[3]->find("a", 0);

        $date = $tds[4]->plaintext;
        $party_served = $tds[5]->plaintext;
        $trade_name = trim($tds[0]->plaintext);

        if ($trade_name == '' || $trade_name == '(NO TRADING NAME)')
            $trade_name = $party_served;

        $details_link = 'http://www.foodauthority.nsw.gov.au/penalty-notices/' . html_entity_decode($a->href);

        info("Fetching details ($id)...");

        $details_html = scraperwiki::scrape($details_link);
        $details_dom = new simple_html_dom();
        $details_dom->load($details_html);

        foreach($details_dom->find(".table-data-pd tr") as $details_tr)
        {
            $details_tds = $details_tr->find("td");

            switch (trim($details_tds[0]->plaintext))
            {
                case "Address\r\n(where offence occurred)":
                    $address = str_replace('/', ' ', trim($details_tds[1]->plaintext));
                    break;
                case 'Offence code':
                    $code = $details_tds[1]->plaintext;
                    break;
                case 'Amount of penalty':
                    $penalty = $details_tds[1]->plaintext;
                    break;
                case "Date penalty notice served\r\n(yyyy-mm-dd)":
                    $date_served = $details_tds[1]->plaintext;
                    if ($date_served == '-00-00')
                        $date_served = $date;
                    break;
                case 'Issued by':
                    $issued_by = $details_tds[1]->plaintext;
                    break;
            }
        }

        if ($address != '')
        {
            info("Fetching location ($address)...");

            $location_link = 'http://dev.virtualearth.net/REST/v1/Locations/AU/NSW/-/' . rawurlencode($address) . '?o=xml&key=Ar8AQgvFLU5GzfH9UXHzxFqme59PPjzN3mtd4azFC0ty73fGzyF-WNyhgl1MpuBL';
            $location_xml = scraperwiki::scrape($location_link);

            if ($location_xml != '')
            {
                $response = new SimpleXMLElement($location_xml);
                $point = $response->ResourceSets->ResourceSet->Resources->Location->Point;
                
                $latitude = $point->Latitude;
                $longitude = $point->Longitude;
            }
        }

        $penalty = array(
            'trade_name'   => $trade_name,
            'suburb'       => $tds[1]->plaintext,
            'council'      => $tds[2]->plaintext,
            'id'           => $tds[3]->plaintext,
            'notice'       => html_entity_decode($a->title),
            'date'         => $date,
            'party_served' => $party_served,
            'notes'        => $tds[6]->plaintext,
            'details_link' => $details_link,
            'address'      => $address,
            'code'         => $code,
            'penalty'      => $penalty,
            'date_served'  => $date_served,
            'issued_by'    => $issued_by,
            'latitude'     => (string)$latitude,
            'longitude'    => (string)$longitude,
            'date_scraped' => date('Y-m-d')
        );
    
        info("Saving new record $id...");

        scraperwiki::save_sqlite(array('id'), $penalty);
    }
}

function info($message)
{
    print '[' . date('Y-M-d H:m:s') . "] $message\n";
}

?>
