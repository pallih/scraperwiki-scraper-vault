<?php

# http://www.horsedeathwatch.com/

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.horsedeathwatch.com/");
$html = str_get_html($html_content);

foreach ($html->find("div#datatable tr") as $el) {           
    if($el->find("td",0))
    {
        $record = array(
            'horse' => $el->find("td",0)->plaintext."", 
            'date' => $el->find("td",1)->innertext."", 
            'course' => $el->find("td",2)->innertext."", 
            'cause_of_death' => $el->find("td",3)->innertext.""
        );
        scraperwiki::save(array('horse'), $record);  
    }
}

?>
<?php

# http://www.horsedeathwatch.com/

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://www.horsedeathwatch.com/");
$html = str_get_html($html_content);

foreach ($html->find("div#datatable tr") as $el) {           
    if($el->find("td",0))
    {
        $record = array(
            'horse' => $el->find("td",0)->plaintext."", 
            'date' => $el->find("td",1)->innertext."", 
            'course' => $el->find("td",2)->innertext."", 
            'cause_of_death' => $el->find("td",3)->innertext.""
        );
        scraperwiki::save(array('horse'), $record);  
    }
}

?>
