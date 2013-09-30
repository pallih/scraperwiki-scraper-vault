<?php

require 'scraperwiki/simple_html_dom.php';           


$baseurl = 'http://www.svz.de/';

# Übersichtsseite mit kommentierten Beiträgen laden
$html_content = scraperWiki::scrape("http://www.svz.de/kommentare-svz/zuletzt-kommentiert.html");
$html = str_get_html($html_content);

# Links zu kommentierten Beiträgen auslesen
foreach ($html->find("h3.news-list-header a") as $el) {           
    $beitrags_url = $baseurl . $el->href;

    # Detailseite des kommentierten Beitrags laden
    $beitrags_html_content =  scraperWiki::scrape($beitrags_url);
    $beitrags_html = str_get_html($beitrags_html_content);

    # einzelne Kommentare einlesen
    foreach ($beitrags_html->find("div.user_dim_pagecomments-commentlisting") as $kommentar) {        
        # Benutzername
        $benutzername = utf8_encode($kommentar->find("span.user_dim_pagecomments-name",0)->innertext);
        # Datum + Uhrzeit
        $datum_uhrzeit = $kommentar->find("span.user_dim_pagecomments-date",0)->innertext;
        $datum_timestamp = strtotime ($datum_uhrzeit);
        # Überschrift
        $ueberschrift = utf8_encode($kommentar->find("div.user_dim_pagecomments-commenttitle",0)->innertext);
        # Text
        $text = $kommentar->find("div.user_dim_pagecomments-comment",0)->innertext;
        # Hash aus den Daten generieren
        $hash = md5($beitrags_url . $benutzername . $datum_uhrzeit . $ueberschrift . $text) . "\n";
        try {
            print $benutzername . "\n";
            print $datum_timestamp . "\n";
            print $ueberschrift . "\n";
            print $text . "\n";
            print $beitrags_url . "\n";

            scraperwiki::save_sqlite(array('Hash'), array(
                "Benutzername"=>$benutzername, 
                "Datum"=>$datum_timestamp,
                "Ueberschrift"=>$ueberschrift,
                "Text"=>$text,
                "Beitrag"=>$beitrags_url,
                "Hash"=>$hash
            ), 'SVZ_Kommentare');
        } catch(Exception $e) {
            print $benutzername . "\n";
            print $datum_timestamp . "\n";
            print $ueberschrift . "\n";
            print $text . "\n";
            print $beitrags_url . "\n";
        }
    }
    $beitrags_html->__destruct();
}


?>
<?php

require 'scraperwiki/simple_html_dom.php';           


$baseurl = 'http://www.svz.de/';

# Übersichtsseite mit kommentierten Beiträgen laden
$html_content = scraperWiki::scrape("http://www.svz.de/kommentare-svz/zuletzt-kommentiert.html");
$html = str_get_html($html_content);

# Links zu kommentierten Beiträgen auslesen
foreach ($html->find("h3.news-list-header a") as $el) {           
    $beitrags_url = $baseurl . $el->href;

    # Detailseite des kommentierten Beitrags laden
    $beitrags_html_content =  scraperWiki::scrape($beitrags_url);
    $beitrags_html = str_get_html($beitrags_html_content);

    # einzelne Kommentare einlesen
    foreach ($beitrags_html->find("div.user_dim_pagecomments-commentlisting") as $kommentar) {        
        # Benutzername
        $benutzername = utf8_encode($kommentar->find("span.user_dim_pagecomments-name",0)->innertext);
        # Datum + Uhrzeit
        $datum_uhrzeit = $kommentar->find("span.user_dim_pagecomments-date",0)->innertext;
        $datum_timestamp = strtotime ($datum_uhrzeit);
        # Überschrift
        $ueberschrift = utf8_encode($kommentar->find("div.user_dim_pagecomments-commenttitle",0)->innertext);
        # Text
        $text = $kommentar->find("div.user_dim_pagecomments-comment",0)->innertext;
        # Hash aus den Daten generieren
        $hash = md5($beitrags_url . $benutzername . $datum_uhrzeit . $ueberschrift . $text) . "\n";
        try {
            print $benutzername . "\n";
            print $datum_timestamp . "\n";
            print $ueberschrift . "\n";
            print $text . "\n";
            print $beitrags_url . "\n";

            scraperwiki::save_sqlite(array('Hash'), array(
                "Benutzername"=>$benutzername, 
                "Datum"=>$datum_timestamp,
                "Ueberschrift"=>$ueberschrift,
                "Text"=>$text,
                "Beitrag"=>$beitrags_url,
                "Hash"=>$hash
            ), 'SVZ_Kommentare');
        } catch(Exception $e) {
            print $benutzername . "\n";
            print $datum_timestamp . "\n";
            print $ueberschrift . "\n";
            print $text . "\n";
            print $beitrags_url . "\n";
        }
    }
    $beitrags_html->__destruct();
}


?>
