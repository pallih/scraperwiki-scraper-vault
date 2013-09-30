<?php

require 'scraperwiki/simple_html_dom.php'; 

$id = 0;

$html = scraperWiki::scrape("http://roanokechamber.chambermaster.com/list/QuickLinkMembers/health-care-11.htm");           

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div#cm_2colmemberinfo") as $record){

        
        $page = $record->find("div#cm_2colmembername a",0);
        
        $childhtml = scraperWiki::scrape($page->href);

        print "parsing: " . $page->href . "\n";

        $child = new simple_html_dom();
        $child->load($childhtml);

        foreach ($child->find("div#cm_ml02_container_content") as $p) {

            $name = $p->find("div.cm_ml02_member_name_center h1",0);
            $address = $p->find("div.cm_ml02_sreet_address",0);
            $phone = $p->find("div.cm_ml02_phone",0);
            $fax = $p->find("div.cm_ml02_fax",0);
            $rep_name = $p->find("div.cm_ml02_rep_name",0);
            $website = $p->find("div.cm_ml02_website_address a",0);
            $about = $p->find("div.cm_ml02_about_us_desc",0);

            $id = $id + 1;

            scraperwiki::save_sqlite(array("id"),array(
                    "id"=> $id,
                    "name"=> $name->innertext,
                    "address"=> str_replace("<br/>",", ",$address->innertext),
                    "phone"=> $phone->innertext,
                    "fax"=> $fax->innertext,
                    "rep_name"=> str_replace("<br />"," ",$rep_name->innertext),
                    "website"=> $website->href,
                    "about"=> $about->innertext
                    ));

        };
   
}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

$id = 0;

$html = scraperWiki::scrape("http://roanokechamber.chambermaster.com/list/QuickLinkMembers/health-care-11.htm");           

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div#cm_2colmemberinfo") as $record){

        
        $page = $record->find("div#cm_2colmembername a",0);
        
        $childhtml = scraperWiki::scrape($page->href);

        print "parsing: " . $page->href . "\n";

        $child = new simple_html_dom();
        $child->load($childhtml);

        foreach ($child->find("div#cm_ml02_container_content") as $p) {

            $name = $p->find("div.cm_ml02_member_name_center h1",0);
            $address = $p->find("div.cm_ml02_sreet_address",0);
            $phone = $p->find("div.cm_ml02_phone",0);
            $fax = $p->find("div.cm_ml02_fax",0);
            $rep_name = $p->find("div.cm_ml02_rep_name",0);
            $website = $p->find("div.cm_ml02_website_address a",0);
            $about = $p->find("div.cm_ml02_about_us_desc",0);

            $id = $id + 1;

            scraperwiki::save_sqlite(array("id"),array(
                    "id"=> $id,
                    "name"=> $name->innertext,
                    "address"=> str_replace("<br/>",", ",$address->innertext),
                    "phone"=> $phone->innertext,
                    "fax"=> $fax->innertext,
                    "rep_name"=> str_replace("<br />"," ",$rep_name->innertext),
                    "website"=> $website->href,
                    "about"=> $about->innertext
                    ));

        };
   
}

?>
