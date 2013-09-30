<?php



$linkscontainer="div[class='b-pager'] ul ";

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

for ($j = 1; $j <= 29; $j++) {

    for ($i = 0; $i <= 10; $i++) {
    
        $pageurl = "http://hh.ru/agenciesratings.mvc?area=1&professionalArea=".$j."&orderBy=1&page=".$i;
        //Getting all links in container $linkscontainer
        $html = scraperWiki::scrape($pageurl);
        $dom->load($html);
        $profarea=$dom->find("h1.b-karating-profarea-title",0)->plaintext;
        foreach($dom->find("tr.b-karating-tr") as $data){
            $kaname=$data->find("td");
            $record = array(
                'id' => $j."-".$i,
                'profarea' => $profarea,
                'agency' => $data->find('p.b-karating-ka-name',0)->plaintext,
                'vacancies' => $data->find('small.b-karating-ka-subdata',0)->plaintext
            );
            print_r($record);
            scraperwiki::save(array('id'), $record);
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
<?php



$linkscontainer="div[class='b-pager'] ul ";

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();

for ($j = 1; $j <= 29; $j++) {

    for ($i = 0; $i <= 10; $i++) {
    
        $pageurl = "http://hh.ru/agenciesratings.mvc?area=1&professionalArea=".$j."&orderBy=1&page=".$i;
        //Getting all links in container $linkscontainer
        $html = scraperWiki::scrape($pageurl);
        $dom->load($html);
        $profarea=$dom->find("h1.b-karating-profarea-title",0)->plaintext;
        foreach($dom->find("tr.b-karating-tr") as $data){
            $kaname=$data->find("td");
            $record = array(
                'id' => $j."-".$i,
                'profarea' => $profarea,
                'agency' => $data->find('p.b-karating-ka-name',0)->plaintext,
                'vacancies' => $data->find('small.b-karating-ka-subdata',0)->plaintext
            );
            print_r($record);
            scraperwiki::save(array('id'), $record);
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
