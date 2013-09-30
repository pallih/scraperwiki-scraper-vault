<?php

# Blank PHP
echo "Init Scrapper";

$html = scraperWiki::scrape("http://google.com/");          
print $html . "TESTE";

?>
