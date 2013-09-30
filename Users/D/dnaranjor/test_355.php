<?php

# Cargamos la pagina a examinar en la variable $html...

require 'scraperwiki/simple_html_dom.php'; 
#$html_content = scraperwiki::scrape("http://venezuelaenforma.com/2-aminoacidos"); 
$html_content = scraperwiki::scrape("https://scraperwiki.com/");
$html = str_get_html($html_content); 

# Examinamos en donde esta el contenido de interes:

#foreach ($html->find("ajax_block_product first_item item clearfix") as $el) 
#    { 
#    print $el . "\n"; 
#    }

foreach ($html->find("div.featured a") as $el) { print $el . "\n"; print $el->href . "\n";}
?>
<?php

# Cargamos la pagina a examinar en la variable $html...

require 'scraperwiki/simple_html_dom.php'; 
#$html_content = scraperwiki::scrape("http://venezuelaenforma.com/2-aminoacidos"); 
$html_content = scraperwiki::scrape("https://scraperwiki.com/");
$html = str_get_html($html_content); 

# Examinamos en donde esta el contenido de interes:

#foreach ($html->find("ajax_block_product first_item item clearfix") as $el) 
#    { 
#    print $el . "\n"; 
#    }

foreach ($html->find("div.featured a") as $el) { print $el . "\n"; print $el->href . "\n";}
?>
