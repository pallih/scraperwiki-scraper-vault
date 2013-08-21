<?php
//   USER INPUT  //
$n_pages = 5 ;                      // number of pages in directory to get channels from, starting from the first
$directory = "entertainment" ;      // justin.tv directory to get channels from
///////////////////

scraperwiki::sqliteexecute( " DROP TABLE swdata " ) ; //drop the existing table so we only get new channels (channels go off-air very often)

require 'scraperwiki/simple_html_dom.php';


$url = "http://www.justin.tv/directory/" . $directory . "?lang=en&page=" ;

$i=0 ;

while ($i<=$n_pages) {
    $i++;
    
    $html = scraperwiki::scrape($url . $i);
    
    $html = str_get_html($html);
    
    $pos=0;

    foreach ($html->find("li.list_item") as $a) {

        $pos++ ;

        $pos = $pos + ( ( $i - 1 ) * 20) ;

        //if ($pos==21) break ;
            $title = $a->find("a.title",0) ; echo trim($title->innertext) . "  |  " ;
            $thumb = $a->find("img.cap",0) ; echo trim($thumb->src) . "  |  " ;
            $link  = $a->find("a.thumb",0) ; echo trim($link->href) . "\n" ;

        //if (!$link->href) continue ;
        scraperwiki::save(array("pos"), array("pos"=>$pos,"title"=>$title->innertext,"thumb"=>$thumb->src,"link"=>$link->href)) ;
    } ;

} ;

?>