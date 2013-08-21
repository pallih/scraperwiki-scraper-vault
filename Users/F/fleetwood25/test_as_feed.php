<?php

        $url = 'http://daringfireball.net/';
        $title = 'Daring Fireball links';
        $description = 'Links';

        $userAgent = 'Googlebot/2.1 (http://www.googlebot.com/bot.html)';

        header('Content-type: text/xml; charset=utf-8', true);

        echo '<?xml version="1.0" encoding="UTF-8"?'.'>' . "n";
        echo '<rss version="2.0">' . "n";
        echo '<channel>' . "n";
        echo '  <title>' . $title . '</title>' . "n";
        echo '  <link>' . $url . '</link>' . "n";
        echo '  <description>' . $description . '</description>' . "n";

        $curl = curl_init($url);
        curl_setopt($curl, CURLOPT_USERAGENT, $userAgent);
        curl_setopt($curl, CURLOPT_AUTOREFERER, true);
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1 );
        curl_setopt($curl, CURLOPT_TIMEOUT, 2 );                

        $html = curl_exec( $curl );

        $html = @mb_convert_encoding($html, 'HTML-ENTITIES', 'utf-8');   

        curl_close( $curl );

        $dom = new DOMDocument();

        @$dom->loadHTML($html);

        $nodes = $dom->getElementsByTagName('*');

        $date = '';

        foreach($nodes as $node){

                if($node->nodeName == 'h2'){
                        $date =  strtotime($node->nodeValue);
                }

                if($node->nodeName == 'dt'){

                        $inodes = $node->childNodes;

                        foreach($inodes as $inode){

                                if($inode->nodeName == 'a' && $inode->getAttribute('class') == 'permalink'){
                                        echo '<item>' . "n";
                                        echo '<title>' . @mb_convert_encoding(htmlspecialchars($inode->getAttribute('title')), 'utf-8') . '</title>' . "n";
                                        echo '<link>' . $inode->getAttribute('href') . '</link>' . "n";
                                        if($date){
                                                echo '<pubDate>' . date(DATE_RSS, $date) . '</pubDate>' . "n";
                                        }
                                        echo '</item>' . "n";
                                }
                        }
                }
        }

        echo '</channel></rss>';

?>
