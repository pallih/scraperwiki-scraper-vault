<?php
//<a href="javascript:__doPostBack('ctl00$ContentPlaceHolder1$dgProduct$ctl08$ctl09','')" style="color:#330099;">60</a>
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://www.stormreaders.net/kedaiirtiyah");
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $cookie = 'cookies/cookie_file.txt';
    curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie);
   
    $html = curl_exec($ch);
    curl_close($ch);
    
    require 'scraperwiki/simple_html_dom.php';           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $column_name = array('title','author','thumbnail','product_code');
    scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `stormreader` (`title` TEXT, `author` TEXT, `thumbnail` TEXT,`product_code` TEXT UNIQUE )');

    $i = 0;
    foreach($dom->find('#ctl00_ContentPlaceHolder1_dgProduct',0)->find('tr') as $trs){
        if($i>1){
            foreach($trs->find('td') as $tds){
                
                //$data =  $tds->find('font',0);
                $thumbnail = $tds->find('img',0) ;
                $title = $tds->find('b',0) ;    
                $author = $tds->find('b',1) ; 
                if(!empty($thumbnail)){
                    $record = array();
                    
                    $record['title'] = $title->innertext;
                    $record['author'] = $author->innertext ;
                    $record['thumbnail'] = $thumbnail->src;
                    $record['product_code'] = substr(trim($title->innertext),0,strpos(trim($title->innertext),' '));
                   
                    //scraperwiki::save_sqlite($column_name, $record,$table_name="stormreader");
                    scraperwiki::sqliteexecute("insert or replace into stormreader values (:title,:author,:thumbnail,:product_code)", $record);
                    scraperwiki::sqlitecommit();  
                }           
            }
            
        }
        $i++;
    } 

?>
<?php
//<a href="javascript:__doPostBack('ctl00$ContentPlaceHolder1$dgProduct$ctl08$ctl09','')" style="color:#330099;">60</a>
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://www.stormreaders.net/kedaiirtiyah");
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, TRUE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $cookie = 'cookies/cookie_file.txt';
    curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie);
   
    $html = curl_exec($ch);
    curl_close($ch);
    
    require 'scraperwiki/simple_html_dom.php';           
    $dom = new simple_html_dom();
    $dom->load($html); 

    $column_name = array('title','author','thumbnail','product_code');
    scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `stormreader` (`title` TEXT, `author` TEXT, `thumbnail` TEXT,`product_code` TEXT UNIQUE )');

    $i = 0;
    foreach($dom->find('#ctl00_ContentPlaceHolder1_dgProduct',0)->find('tr') as $trs){
        if($i>1){
            foreach($trs->find('td') as $tds){
                
                //$data =  $tds->find('font',0);
                $thumbnail = $tds->find('img',0) ;
                $title = $tds->find('b',0) ;    
                $author = $tds->find('b',1) ; 
                if(!empty($thumbnail)){
                    $record = array();
                    
                    $record['title'] = $title->innertext;
                    $record['author'] = $author->innertext ;
                    $record['thumbnail'] = $thumbnail->src;
                    $record['product_code'] = substr(trim($title->innertext),0,strpos(trim($title->innertext),' '));
                   
                    //scraperwiki::save_sqlite($column_name, $record,$table_name="stormreader");
                    scraperwiki::sqliteexecute("insert or replace into stormreader values (:title,:author,:thumbnail,:product_code)", $record);
                    scraperwiki::sqlitecommit();  
                }           
            }
            
        }
        $i++;
    } 

?>
