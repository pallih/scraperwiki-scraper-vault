<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.precariosinflexiveis.org/2011/05/testemunho-axes-market.html?commentPage=2");
$html = str_get_html($html_content);
$html_el = $html->find("div#Blog1_comments-block-wrapper dl", 0);

$name = '';
$comment = '';

$flag = 0;
foreach ($html_el->children() as $child1) {
    
    $flag = $flag + 1;
    
    if($flag>3) {
        $flag = 1;
    }


    if($flag == 1) {
        print "Nome: " . $child1->plaintext . "\n";
        $name = $child1->plaintext;
    } else if($flag == 2) {
        print "Comentário: " . $child1->plaintext . "\n";
        $comment = $child1->plaintext;
    } else if($flag == 3) {
        print "Timestamp: " . $child1->plaintext . "\n";
       
        $record = array('name' => $name, 'comment' => $comment, 'timestamp' => $child1->plaintext );
        scraperwiki::save(array('timestamp'), $record);

    }
   
    
     
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.precariosinflexiveis.org/2011/05/testemunho-axes-market.html?commentPage=2");
$html = str_get_html($html_content);
$html_el = $html->find("div#Blog1_comments-block-wrapper dl", 0);

$name = '';
$comment = '';

$flag = 0;
foreach ($html_el->children() as $child1) {
    
    $flag = $flag + 1;
    
    if($flag>3) {
        $flag = 1;
    }


    if($flag == 1) {
        print "Nome: " . $child1->plaintext . "\n";
        $name = $child1->plaintext;
    } else if($flag == 2) {
        print "Comentário: " . $child1->plaintext . "\n";
        $comment = $child1->plaintext;
    } else if($flag == 3) {
        print "Timestamp: " . $child1->plaintext . "\n";
       
        $record = array('name' => $name, 'comment' => $comment, 'timestamp' => $child1->plaintext );
        scraperwiki::save(array('timestamp'), $record);

    }
   
    
     
}

?>
