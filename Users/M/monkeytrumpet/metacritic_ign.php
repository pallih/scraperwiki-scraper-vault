<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
$records = array();
$j = 0;
for ($i = 0; $i <= 30; $i++) {
    $html_content = scraperwiki::scrape("http://www.metacritic.com/publication/ign?filter=games&num_items=100&sort_options=critic_score&page=" . $i);
    echo "http://www.metacritic.com/publication/ign?filter=games&num_items=100&sort_options=critic_score&page=" . $i;
    $html = str_get_html($html_content);
    
    $ret = $html->find('.critic_review');
    foreach ($ret as $value) {
        $j++;
        $title = $value->find('.review_product',0);
        $record = 
            array(
               'title' => $title->find('a',0)->plaintext, 
               'score' => intval($value->find('.critscore',0)->plaintext));
            
            scraperwiki::save(array('title'), $record);   
    }
    $html->clear(); 
    unset($html);
}
echo $j;
/*scraperwiki::save_sqlite($titles, $scores);*/

?>
<?php

# Blank PHP

require 'scraperwiki/simple_html_dom.php';
$records = array();
$j = 0;
for ($i = 0; $i <= 30; $i++) {
    $html_content = scraperwiki::scrape("http://www.metacritic.com/publication/ign?filter=games&num_items=100&sort_options=critic_score&page=" . $i);
    echo "http://www.metacritic.com/publication/ign?filter=games&num_items=100&sort_options=critic_score&page=" . $i;
    $html = str_get_html($html_content);
    
    $ret = $html->find('.critic_review');
    foreach ($ret as $value) {
        $j++;
        $title = $value->find('.review_product',0);
        $record = 
            array(
               'title' => $title->find('a',0)->plaintext, 
               'score' => intval($value->find('.critscore',0)->plaintext));
            
            scraperwiki::save(array('title'), $record);   
    }
    $html->clear(); 
    unset($html);
}
echo $j;
/*scraperwiki::save_sqlite($titles, $scores);*/

?>
