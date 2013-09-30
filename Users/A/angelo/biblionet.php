<?php
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$base_url = "http://biblionet.gr/main.asp?page=showbook&bookid=";

for ($i=15000; $i<=17000; $i++){
    $url = $base_url . $i;
    if ($html = file_get_html($url)){
    
    //    $html2 = $html->find('div[id=overview] div[class]'); 
    // $dom->load($html);
    
        $title = $html->find("h1[class='book_title']");
        if (count($title)>0){
            $author = $html->find("a[class='booklink']");
            $title2 = $title[0]->plaintext;
            $record = array(
                'id' => $i, 
                'title' => $title2, 
                'author' => $author[0]->plaintext
            );
            print_r($record);
            scraperwiki::save(array('id'),$record); 
        }
        
    }
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$base_url = "http://biblionet.gr/main.asp?page=showbook&bookid=";

for ($i=15000; $i<=17000; $i++){
    $url = $base_url . $i;
    if ($html = file_get_html($url)){
    
    //    $html2 = $html->find('div[id=overview] div[class]'); 
    // $dom->load($html);
    
        $title = $html->find("h1[class='book_title']");
        if (count($title)>0){
            $author = $html->find("a[class='booklink']");
            $title2 = $title[0]->plaintext;
            $record = array(
                'id' => $i, 
                'title' => $title2, 
                'author' => $author[0]->plaintext
            );
            print_r($record);
            scraperwiki::save(array('id'),$record); 
        }
        
    }
}
?>
