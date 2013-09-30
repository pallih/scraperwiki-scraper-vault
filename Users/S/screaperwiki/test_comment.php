<?php

$commenti_url=str_replace(".html#commenti", "/index.html#commenti",$data->href);
$commenti_html = scraperWiki::scrape($commenti_url);                 
$dom_commenti = new simple_html_dom();
$dom_commenti->load($commenti_html);
foreach($dom_commenti->find("div.rate") as $comment)
{
        $comment_id= trim($comment->id,'ratercomment');
        echo $comment_id."\t"; 
        $tds = $comment->find("td.numvote");
        foreach ($tds as $td)
        {
            echo $td->plaintext."\t";
        }
        echo "\n";
}

?>
<?php

$commenti_url=str_replace(".html#commenti", "/index.html#commenti",$data->href);
$commenti_html = scraperWiki::scrape($commenti_url);                 
$dom_commenti = new simple_html_dom();
$dom_commenti->load($commenti_html);
foreach($dom_commenti->find("div.rate") as $comment)
{
        $comment_id= trim($comment->id,'ratercomment');
        echo $comment_id."\t"; 
        $tds = $comment->find("td.numvote");
        foreach ($tds as $td)
        {
            echo $td->plaintext."\t";
        }
        echo "\n";
}

?>
