<?php
    require 'scraperwiki/simple_html_dom.php';

    $url = "http://www.values.com/inspirational-quotes?page=1" ;

    $html = file_get_html($url);

 foreach($html->find('.index_card') as $card )
{
        
    $quote =  $card->find('.quotation',0)->innertext;       
    $author = $card->find('.quotation_author',0)->plaintext;
            
    $quote = cleanQuotes($quote);
    $author = cleanAuthor($author);

    echo '$quote = '.$quote."\n";
    echo '$author = '.$author."\n";
    
}


function cleanQuotes($str)
{
$str= str_replace("&ldquo;", "", $str);
$str= str_replace("&rdquo;", "", $str);
return $str;
}

function cleanAuthor($a)
{
$a = str_replace("&nbsp;&nbsp;&nbsp;Share or Discuss This Quote", "", $a);
$a = trim($a);
return $a;
}

?>
<?php
    require 'scraperwiki/simple_html_dom.php';

    $url = "http://www.values.com/inspirational-quotes?page=1" ;

    $html = file_get_html($url);

 foreach($html->find('.index_card') as $card )
{
        
    $quote =  $card->find('.quotation',0)->innertext;       
    $author = $card->find('.quotation_author',0)->plaintext;
            
    $quote = cleanQuotes($quote);
    $author = cleanAuthor($author);

    echo '$quote = '.$quote."\n";
    echo '$author = '.$author."\n";
    
}


function cleanQuotes($str)
{
$str= str_replace("&ldquo;", "", $str);
$str= str_replace("&rdquo;", "", $str);
return $str;
}

function cleanAuthor($a)
{
$a = str_replace("&nbsp;&nbsp;&nbsp;Share or Discuss This Quote", "", $a);
$a = trim($a);
return $a;
}

?>
