<?php
######################################
# Basic PHP scraper
######################################
require  'scraperwiki/simple_html_dom.php';
    
    for($year = 2001; $year < 2011; $year++) {
    $n = 0;   
        
        $html = scraperwiki::scrape("http://www.esmeefairbairn.org.uk/grants_made{$year}.html");

        
        # Use the PHP Simple HTML DOM Parser to extract <td> tags
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find('li') as $data)
        {
            $href = $data->find("a",0)->href;
            $category = $data->find("a",0)->plaintext;
            $grantpagehtml = scraperwiki::scrape("http://www.esmeefairbairn.org.uk/".$href);
            $grantpage = new simple_html_dom();
            $grantpage->load($grantpagehtml);
            
            
            $grantsdata = split("<b>",$grantpage->find("td[width='421']",0)->innertext);
            $grantsdata = str_replace("<BR>","<br>",$grantsdata); 
            
            foreach($grantsdata as $grant) {
                if(strpos($grant,"&pound;") && !strpos($grant,"No. of Grants:")) {
 
                    $grantdetails = split("<br>",$grant); 
                    if(count($grantdetails) > 1) { 
                        $title = strip_tags(substr($grantdetails[0],0,strpos($grantdetails[0],"</b>")));
                        $amount = strip_tags(substr($grantdetails[0],strpos($grantdetails[0],"</b>")+14));
                        $description = trim(strip_tags($grantdetails[1]));
                        print $title . " - " . $amount . " ". $description . "\n";  
                        scraperwiki::save(array('id'), array('id'=> $year ."-".$n++,'year' => $year, 'category' => $category, 'title' => $title, 'amount' => $amount, 'description' => $description));                  
                    }
                }
            }

        }
    
    }

?>