<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';  

//scraperwiki::sqliteexecute("create table uri (id int, 'id_bg' string, 'url' string)"); 
//scraperwiki::sqliteexecute("drop table uri");
//scraperwiki::sqlitecommit();  
//print_r(scraperwiki::sqliteexecute("desc uri")); 

$html = scraperWiki::scrape("http://www.beppegrillo.it");                 
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[id='post_principale' h3 a") as $k=>$data)
{
    //echo $data->parent->id;
    $uri=$data->href;
    $id_bg=$data->parent->id;
    scraperwiki::sqliteexecute("insert into uri values (?,?,?)", array($k, $id_bg, $uri));
    scraperwiki::sqlitecommit(); 
    //print_r(scraperwiki::sqliteexecute("select * from uri")); 

    $commenti_url=str_replace(".html#commenti", "/index.html#commenti",$data->href);
    $commenti_html = scraperWiki::scrape($commenti_url);                 
    $dom_commenti = new simple_html_dom();
    sleep(20);
    for ($i = 1; $i <= 10; $i++) 
    {
        try {
            $dom_commenti->load($commenti_html);
            if (!$dom_commenti)
                throw new Exception('$a è negativo');
            break;
        }
        catch (Exception $e) {
        }        
    }
    //$dom_commenti->load($commenti_html);
    foreach($dom_commenti->find("div.rate") as $comment)
    {
        $comment_id= trim($comment->id,'ratercomment');
        echo $comment_id."\t"; 
        $tds = $comment->find("td.numvote");
        foreach ($tds as $td)
        {
            echo $td->plaintext."\t";
        }
        $rate=$comment->find("li.current-rating");
        foreach ($rate as $r)
        {
            echo $r->plaintext."\t";
            $currently=trim($r->plaintext,'Currently ');
            $currently=trim($currently[1],'/5');
            //echo $currently[0]."\t";
        }
        echo "\n";
    }
}


?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';  

//scraperwiki::sqliteexecute("create table uri (id int, 'id_bg' string, 'url' string)"); 
//scraperwiki::sqliteexecute("drop table uri");
//scraperwiki::sqlitecommit();  
//print_r(scraperwiki::sqliteexecute("desc uri")); 

$html = scraperWiki::scrape("http://www.beppegrillo.it");                 
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[id='post_principale' h3 a") as $k=>$data)
{
    //echo $data->parent->id;
    $uri=$data->href;
    $id_bg=$data->parent->id;
    scraperwiki::sqliteexecute("insert into uri values (?,?,?)", array($k, $id_bg, $uri));
    scraperwiki::sqlitecommit(); 
    //print_r(scraperwiki::sqliteexecute("select * from uri")); 

    $commenti_url=str_replace(".html#commenti", "/index.html#commenti",$data->href);
    $commenti_html = scraperWiki::scrape($commenti_url);                 
    $dom_commenti = new simple_html_dom();
    sleep(20);
    for ($i = 1; $i <= 10; $i++) 
    {
        try {
            $dom_commenti->load($commenti_html);
            if (!$dom_commenti)
                throw new Exception('$a è negativo');
            break;
        }
        catch (Exception $e) {
        }        
    }
    //$dom_commenti->load($commenti_html);
    foreach($dom_commenti->find("div.rate") as $comment)
    {
        $comment_id= trim($comment->id,'ratercomment');
        echo $comment_id."\t"; 
        $tds = $comment->find("td.numvote");
        foreach ($tds as $td)
        {
            echo $td->plaintext."\t";
        }
        $rate=$comment->find("li.current-rating");
        foreach ($rate as $r)
        {
            echo $r->plaintext."\t";
            $currently=trim($r->plaintext,'Currently ');
            $currently=trim($currently[1],'/5');
            //echo $currently[0]."\t";
        }
        echo "\n";
    }
}


?>
