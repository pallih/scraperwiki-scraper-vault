<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


$outerhtml = scraperwiki::scrape("http://www.oxford.gov.uk/PageRender/decH/Garages_to_rent_occw.htm");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$outerdom = new simple_html_dom();
$outerdom->load($outerhtml);

foreach($outerdom->find('li a') as $outerdata) {

        if(stristr($outerdata->plaintext,"Garage Locations")) {
            $outerdata->href=str_replace("/..","",$outerdata->href);
            $outerdata->href=str_replace("..","",$outerdata->href);
            print($outerdata->href);
    
            $html = scraperwiki::scrape("http://www.oxford.gov.uk".$outerdata->href);
        
        # Use the PHP Simple HTML DOM Parser to extract <td> tags
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find('div.pagewidget') as $data)
        {
            if(stristr($data->plaintext,"Site location")) {
                $values['source'] = "http://www.oxford.gov.uk".$outerdata->href;
                $values['image'] = "http://www.oxford.gov.uk" . $data->find("img",0)->src; #Use HTML Simple Dom to fetch the image;
                $lines = explode("<BR>",str_replace("<br>","<BR>",str_replace("<br />","<BR>",$data->innertext))); #Split on line-breaks. ->innertext returns the element with its HTML
        
                foreach($lines as $line) {
                    $line_detail = explode(':',strip_tags($line)); #Split out by ':'
                    if(count($line_detail) > 1) { #Check we have a : in the line, and it's not an image line.
                        $values[trim($line_detail[0])] = trim($line_detail[1]); #Use bit before : as array key
                    }
                }
        
                list($length, $maxHeight, $clearanceHeight, $maxWidth, $clearanceWidth) = explode("m,", $values['Garage dimensions']);
                $values['length'] = preg_replace("/[a-zA-Z]+/","",$length); $values['maxHeight'] = preg_replace("/[a-zA-Z]+/","",$maxHeight); $values['maxWidth'] = preg_replace("/[a-zA-Z]+/","",$maxWidth); $values['clearanceWidth'] = preg_replace("/[a-zA-Z]+/","",$clearanceWidth);

                $lat_lng = scraperwiki::gb_postcode_to_latlng($values['Postcode']);
                if ($lat_lng)
                {
                    $values["lat"] = $lat_lng[0]; 
                    $values["lng"] = $lat_lng[1]; 
                }              
                scraperwiki::save(array('Site location'), $values);
                
                unset($values);
            }
        }
    }
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


$outerhtml = scraperwiki::scrape("http://www.oxford.gov.uk/PageRender/decH/Garages_to_rent_occw.htm");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$outerdom = new simple_html_dom();
$outerdom->load($outerhtml);

foreach($outerdom->find('li a') as $outerdata) {

        if(stristr($outerdata->plaintext,"Garage Locations")) {
            $outerdata->href=str_replace("/..","",$outerdata->href);
            $outerdata->href=str_replace("..","",$outerdata->href);
            print($outerdata->href);
    
            $html = scraperwiki::scrape("http://www.oxford.gov.uk".$outerdata->href);
        
        # Use the PHP Simple HTML DOM Parser to extract <td> tags
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find('div.pagewidget') as $data)
        {
            if(stristr($data->plaintext,"Site location")) {
                $values['source'] = "http://www.oxford.gov.uk".$outerdata->href;
                $values['image'] = "http://www.oxford.gov.uk" . $data->find("img",0)->src; #Use HTML Simple Dom to fetch the image;
                $lines = explode("<BR>",str_replace("<br>","<BR>",str_replace("<br />","<BR>",$data->innertext))); #Split on line-breaks. ->innertext returns the element with its HTML
        
                foreach($lines as $line) {
                    $line_detail = explode(':',strip_tags($line)); #Split out by ':'
                    if(count($line_detail) > 1) { #Check we have a : in the line, and it's not an image line.
                        $values[trim($line_detail[0])] = trim($line_detail[1]); #Use bit before : as array key
                    }
                }
        
                list($length, $maxHeight, $clearanceHeight, $maxWidth, $clearanceWidth) = explode("m,", $values['Garage dimensions']);
                $values['length'] = preg_replace("/[a-zA-Z]+/","",$length); $values['maxHeight'] = preg_replace("/[a-zA-Z]+/","",$maxHeight); $values['maxWidth'] = preg_replace("/[a-zA-Z]+/","",$maxWidth); $values['clearanceWidth'] = preg_replace("/[a-zA-Z]+/","",$clearanceWidth);

                $lat_lng = scraperwiki::gb_postcode_to_latlng($values['Postcode']);
                if ($lat_lng)
                {
                    $values["lat"] = $lat_lng[0]; 
                    $values["lng"] = $lat_lng[1]; 
                }              
                scraperwiki::save(array('Site location'), $values);
                
                unset($values);
            }
        }
    }
}

?>