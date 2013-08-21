<?php
######################################
# PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

function scraper($url,$isco,$country)
 {
     $has_next = false;
     $base_url = "http://ec.europa.eu/eures/eures-searchengine/servlet";

     $html = scraperwiki::scrape($url);  

     $dom = new simple_html_dom();
     $dom->load($html);

     foreach($dom->find('table[class=JResult]') as $result)
     {
         foreach($result->find('td[class=JRTitle] a') as $job_page)
         {
           
            $chars = explode("'",$job_page->onclick);
        
            $url_job = $base_url.substr($chars[1], 1);
        
            print "JOB: " .$url_job . "<br />";
         };

        foreach($result->find('th') as $data)
         {   
    
             $text = trim($data->plaintext);
             
             if ($text == 'Description:')
             {
                 $description = trim($data->next_sibling()->plaintext);
                 echo "DESCRIPTION: " .$description . "\n";    
             }
    
             if ($text == 'Source:')
             {
                 $source = trim($data->next_sibling()->plaintext);
                 if ($source <> '' && $source <> '&nbsp;')
                    echo "SOURCE: " .$source . "\n";   
             }
         }
         scraperwiki::save(array('url_job'), array('url_job' => $url_job, 'description' => $description, 'source' => $source, 'url' => $url));
     }
   
     foreach($dom->find('div[class=prevNext] a') as $next_page)
     {
            $text = $next_page->plaintext;
    
            if ($text == "Next page")
            {
                $url_next = substr($next_page->href, 1);
           
                $url_next = $base_url.$url_next;
                
                $has_next = true;
            }   
             print "NEXT: " . $url_next . "<br />";
     };
/*

     if ($has_next == true){
         sleep(10);
         scraper($url_next);
     }
*/
}

$country = array('ES');

//'AT', 'BE','BG''CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IR','IT','LV','LI','LT','LU','MT','NL','NO','PL','PT','RO','SK','SI','ES','SE','CH','UK'

for ($i=0; $i < sizeof($country); $i++){
    $url_first = "http://ec.europa.eu/eures/eures-searchengine/servlet/BrowseCountryJVsServlet?lg=EN&isco=&country=".$country[$i]."&multipleRegions=%25&date=01%2F01%2F1975&title=&durex=&exp=&qual=&pageSize=99&totalCount=999999999&startIndexes=0-1o1-1o2-1I0-2o1-30o2-1I0-3o1-59o2-1I0-4o1-88o2-1I&page=1";
        scraper($url_first);
    }
}

?>