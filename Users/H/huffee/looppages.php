<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
for ($i = 1; $i <= 77; $i++) {
    echo $i;
$htmlstr = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=" . $i;
    $html = scraperWiki::scrape($htmlstr);
    $html = str_get_html($html);

    foreach ($html->find("a.more") as $el) {
    print $el->href . "\n";
    }
}

?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
for ($i = 1; $i <= 77; $i++) {
    echo $i;
$htmlstr = "http://www.teamgb.com/athlete-search?field_games_term_tid=All&field_sport_term_tid=&name=&field_born_region_tid=All&field_lives_region_tid=All&page=" . $i;
    $html = scraperWiki::scrape($htmlstr);
    $html = str_get_html($html);

    foreach ($html->find("a.more") as $el) {
    print $el->href . "\n";
    }
}

?>
