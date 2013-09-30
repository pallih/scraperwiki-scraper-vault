<?php
# http://www.horsedeathwatch.com/
require 'scraperwiki/simple_html_dom.php'; 

for ($i=1; $i<=3200; $i++)
{
    print $i;    

    $html_content = scraperwiki::scrape("http://dribbble.com/designers/prospects?page=".$i);
    $html = str_get_html($html_content);
    foreach ($html->find("h2.vcard") as $el) {           
        if($el->find("a",0))
        {
            $address = "http://dribbble.com".$el->find("a",0)->href."";
            $html_content2 = scraperwiki::scrape($address);
            $html2 = str_get_html($html_content2);
        
            foreach ($html2->find("ul.profile-details") as $el) {           
                if($el->find("li",2)){
                    $record = array(
                        'address' => $el->find("a",2)->plaintext."", 
              
                    );
                scraperwiki::save(array('address'), $record); 
                }
            }
        }
    }

}
?><?php
# http://www.horsedeathwatch.com/
require 'scraperwiki/simple_html_dom.php'; 

for ($i=1; $i<=3200; $i++)
{
    print $i;    

    $html_content = scraperwiki::scrape("http://dribbble.com/designers/prospects?page=".$i);
    $html = str_get_html($html_content);
    foreach ($html->find("h2.vcard") as $el) {           
        if($el->find("a",0))
        {
            $address = "http://dribbble.com".$el->find("a",0)->href."";
            $html_content2 = scraperwiki::scrape($address);
            $html2 = str_get_html($html_content2);
        
            foreach ($html2->find("ul.profile-details") as $el) {           
                if($el->find("li",2)){
                    $record = array(
                        'address' => $el->find("a",2)->plaintext."", 
              
                    );
                scraperwiki::save(array('address'), $record); 
                }
            }
        }
    }

}
?>