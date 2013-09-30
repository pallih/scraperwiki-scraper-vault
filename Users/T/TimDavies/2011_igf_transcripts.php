<?php

require 'scraperwiki/simple_html_dom.php';        


$html = scraperWiki::scrape("http://www.intgovforum.org/cms/transcripts");
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("a") as $link) {
    if(strpos($link->href,"-transcripts")) {
         $session = $link->plaintext;
         $title_parts = explode(":",$session);

         if(count($title_parts) == 1) {
            $code = $session;
         } else {
            $code = str_replace("/", ", ",$title_parts[0]);
         }

         print $code . "\n";

         $transcript = scraperWiki::scrape("http://www.intgovforum.org".$link->href);
         $tdom = new simple_html_dom();
         $tdom->load($transcript);

         $text = $tdom->find(".contentpaneopen",1);
       
        scraperwiki::save_sqlite(array("code"), array("code"=>$code, "title" => $session, "url" => "http://www.intgovforum.org".$link->href, "text" => (string)$text));
    }
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';        


$html = scraperWiki::scrape("http://www.intgovforum.org/cms/transcripts");
$dom = new simple_html_dom();
$dom->load($html);

foreach($dom->find("a") as $link) {
    if(strpos($link->href,"-transcripts")) {
         $session = $link->plaintext;
         $title_parts = explode(":",$session);

         if(count($title_parts) == 1) {
            $code = $session;
         } else {
            $code = str_replace("/", ", ",$title_parts[0]);
         }

         print $code . "\n";

         $transcript = scraperWiki::scrape("http://www.intgovforum.org".$link->href);
         $tdom = new simple_html_dom();
         $tdom->load($transcript);

         $text = $tdom->find(".contentpaneopen",1);
       
        scraperwiki::save_sqlite(array("code"), array("code"=>$code, "title" => $session, "url" => "http://www.intgovforum.org".$link->href, "text" => (string)$text));
    }
}


?>
