<?php

require 'scraperwiki/simple_html_dom.php'; 

$id = 0;

$html = scraperWiki::scrape("http://roanokechamber.chambermaster.com/list/searchalpha/0-9.htm");           

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span.cm_alphaprevnext a") as $link){

        
        print "parsing: " . $link->href . "\n";

        $childhtml = scraperWiki::scrape($link->href);

        $child = new simple_html_dom();
        $child->load($childhtml);


        foreach ($child->find("div#cm_2colmembername a") as $c) {

            print "fetching Member: " . $c->innertext;

            $memberhtml = scraperWiki::scrape($c->href);
            $member = new simple_html_dom();
            $member->load($memberhtml);

            
            

            $name = $member->find("div.cm_ml02_member_name_center h1",0);
            $address = $member->find("div.cm_ml02_sreet_address",0);
            $phone = $member->find("div.cm_ml02_phone",0);
            $fax = $member->find("div.cm_ml02_fax",0);
            $rep_name = $member->find("div.cm_ml02_rep_name",0);
            $website = $member->find("div.cm_ml02_website_address a",0);
            $about = $member->find("div.cm_ml02_about_us_desc",0);
            $cat = $member->find("div.cm_ml02_member_categories_center",0);
           

            $id = $id + 1;

            scraperwiki::save_sqlite(array("id"),array(
                    "id"=> $id,
                    "name"=> $name->innertext,
                    "address"=> str_replace("<br/>",", ",$address->innertext),
                    "phone"=> $phone->innertext,
                    "fax"=> $fax->innertext,
                    "rep_name"=> str_replace("<br />"," ",$rep_name->innertext),
                    "website"=> $website->href,
                    "about"=> $about->innertext,
                    "cat"=> $cat->innertext,
                    ));

        };


}

?>
<?php

require 'scraperwiki/simple_html_dom.php'; 

$id = 0;

$html = scraperWiki::scrape("http://roanokechamber.chambermaster.com/list/searchalpha/0-9.htm");           

$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("span.cm_alphaprevnext a") as $link){

        
        print "parsing: " . $link->href . "\n";

        $childhtml = scraperWiki::scrape($link->href);

        $child = new simple_html_dom();
        $child->load($childhtml);


        foreach ($child->find("div#cm_2colmembername a") as $c) {

            print "fetching Member: " . $c->innertext;

            $memberhtml = scraperWiki::scrape($c->href);
            $member = new simple_html_dom();
            $member->load($memberhtml);

            
            

            $name = $member->find("div.cm_ml02_member_name_center h1",0);
            $address = $member->find("div.cm_ml02_sreet_address",0);
            $phone = $member->find("div.cm_ml02_phone",0);
            $fax = $member->find("div.cm_ml02_fax",0);
            $rep_name = $member->find("div.cm_ml02_rep_name",0);
            $website = $member->find("div.cm_ml02_website_address a",0);
            $about = $member->find("div.cm_ml02_about_us_desc",0);
            $cat = $member->find("div.cm_ml02_member_categories_center",0);
           

            $id = $id + 1;

            scraperwiki::save_sqlite(array("id"),array(
                    "id"=> $id,
                    "name"=> $name->innertext,
                    "address"=> str_replace("<br/>",", ",$address->innertext),
                    "phone"=> $phone->innertext,
                    "fax"=> $fax->innertext,
                    "rep_name"=> str_replace("<br />"," ",$rep_name->innertext),
                    "website"=> $website->href,
                    "about"=> $about->innertext,
                    "cat"=> $cat->innertext,
                    ));

        };


}

?>
