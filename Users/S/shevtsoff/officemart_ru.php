<?php

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();


    for ($i = 1; $i <= 10; $i++) {
    
        $pageurl = "http://www.officemart.ru/messenge_service/company/".$i."0.htm?region=&brend=";
        //$pageurl = "http://www.officemart.ru/messenge_service/company/0.htm?region=&brend=";

        //Getting all links in container $linkscontainer
        $html = scraperWiki::scrape($pageurl);
        $dom->load($html);


        foreach($dom->find("div.company a") as $url){
            
            $link = $url->href;    
            $title = $url->plaintext;
        
            //run thruogh all links
                $response_html  = scraperWiki::scrape("http://www.officemart.ru/".$link);                
                $response = str_get_html($response_html);
        
                foreach($response->find("td.text") as $pagedata){
                   $contactman="";
                   $contactadress="";
                   $contactmail="";
                   $contactphone="";
                   $contactsite="";
                   $contactregion="";
                   foreach($pagedata->find('table.table_company',1)->find('tr') as $contactinfo){
                    $tabletitle = $contactinfo->find('td',0)->plaintext;
                    $tabletitle = iconv("windows-1251", "UTF-8",$tabletitle);
                        switch ($tabletitle) {
                            case "Контактное лицо:":
                                $contactman=$contactinfo->find('td',1)->plaintext;
                                break;
                            case "Адрес почтовый:":
                                $contactadress=$contactinfo->find('td',1)->plaintext;                               
                                break;
                            case "Email":
                                $contactmail=$contactinfo->find('td',1)->plaintext;                                
                                break;
                            case "Телефон:":
                                $contactphone=$contactinfo->find('td',1)->plaintext;                                 
                                break;
                            case "Адрес сайта:":
                                $contactsite=$contactinfo->find('td',1)->plaintext;                                  
                                break;
                            case "Регион РФ:":
                                $contactregion=$contactinfo->find('td',1)->plaintext;                                
                                break;
                        }
                    }

                   $aboutinfo = iconv("windows-1251", "UTF-8",$pagedata->find('p.p',0)->plaintext);

                   $record = array(
                        'title'=>iconv("windows-1251", "UTF-8",$title),
                        'about' => $aboutinfo,
                        'common' => iconv("windows-1251", "UTF-8",$pagedata->find('table.table_company',0)->plaintext),
                        'adress'=> iconv("windows-1251", "UTF-8",$contactadress),
                        'phone'=> iconv("windows-1251", "UTF-8",$contactphone),
                        'site'=> iconv("windows-1251", "UTF-8",$contactsite),
                        'region'=> iconv("windows-1251", "UTF-8",$contactregion),
                        'bank' => iconv("windows-1251", "UTF-8",$pagedata->find('table.table_company',2)->plaintext)
                    );
                    
                    //print_r($record);
                    scraperwiki::save(array('title'), $record);
                
                }
        
        }

    
    }




/*$sourceurl="http://hh.ru/agenciesratings.mvc?professionalArea=5"; //page url containing links
$linkscontainer="div[id='table'] "; //links container

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

//Getting all links in container $linkscontainer
$html = scraperWiki::scrape($sourceurl);
$dom->load($html);
foreach($dom->find($linkscontainer."a") as $url){
    
    $link = $url->href;    
    $title = $url->innertext;

    //run thruogh all links
        $response_html  = scraperWiki::scrape("http://vhre.ru/".$link);                
        $response = str_get_html($response_html);

        foreach($response->find("div[id='p_info'] table") as $pagedata){
              
           $record = array(
                'title' => $title, 
                'city' => $pagedata->find('tr',4)->find('td',1)->plaintext,
                'services' => "",
                'phone' => $pagedata->find('tr',0)->find('td',1)->plaintext,
                'site' => $pagedata->find('tr',3)->find('td',1)->plaintext
            );
            
            print_r($record);
            //scraperwiki::save(array('title'), $record);
        
        }

}
*/


?>
