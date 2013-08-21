<?php

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();



                $response_html  = scraperWiki::scrape("http://www.officemart.ru/messenge_service/company/company3029.htm");                
                $response = str_get_html($response_html);
        
                foreach($response->find("td.text") as $pagedata){
                      
                   $record = array(
                        'about' => $pagedata->find('p.p',0)->plaintext,
                        'common' => $pagedata->find('table.table_company',0)->plaintext,
                        //'contact' => $pagedata->find('table.table_company',1)->plaintext,
                        'adress'=> $pagedata->find('table.table_company',1)->find('tr',1)->find('td',1)->plaintext,
                        'phone'=> $pagedata->find('table.table_company',1)->find('tr',3)->find('td',1)->plaintext,
                        'site'=> $pagedata->find('table.table_company',1)->find('tr',4)->find('td',1)->plaintext,
                        'region'=> $pagedata->find('table.table_company',1)->find('tr',5)->find('td',1)->plaintext,
                        'bank' => $pagedata->find('table.table_company',2)->plaintext
                    );
                    
                    print_r($record);
                    //scraperwiki::save(array('title'), $record);
                
                }
        


?>
