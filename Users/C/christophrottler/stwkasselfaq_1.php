<?php

require 'scraperwiki/simple_html_dom.php';           
$url = "http://www.studentenwerk-kassel.de/faq.html"; # die Seitenadresse. Hier ist das ein 1-Seiten-Bsp. Bei Unterseiten muss man sich die Links suchen und dann die scraperwiki::scrape-Funktion auch für die Unterseiten aufrufen
$html_content = scraperwiki::scrape($url); # lädt html runter
$html = str_get_html($html_content); # öffnet das HTML und analysiert die Struktur (war vorher nur ein langer Text glaube ich)

$first = true; # hilfsvariable

$results = array(); # hier kommen die Ergebnisse rein

foreach ($html->find("div.csc-frame-frame1") as $el) {  # jeden Div mit der Klasse csc-frame-frame1 suchen         
    if($first) { $first = false; continue; } # erstes überspringen, ist das Inhaltverzeichnis
    
    $title = $el->find("div.csc-header", 0);  # bei jedem csc-frame-frame1-Div ist in dieser Klasse der Titel der Frage 
    print strip_tags($title) . "\n";          # ausgeben. Strip-Tags entfernt HTML-Tags. Wenn du die brauchst für Formatierung und Links kannst du die auch u. U. drin lassen.
    
   
}

$html->__destruct(); # clean up


print "\n\n";

print "Array $results:\n";

var_dump($results); # ausgeben des Arrays.

# $results hat die Form [[FRAGE1, ANTWORT1], [FRAGE2, ANTWORT2], ...]

?>
