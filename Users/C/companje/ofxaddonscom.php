<?php
require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape("http://ofxaddons.com/");
$html = str_get_html($html_content);

foreach ($html->find("div.category") as $categories) {
    foreach ($categories->find("div.repo") as $addons) {
        //if ($ttl++>20) exit();

        $link = $addons->find("a.github_link");
        $link = $link[0]->href;
    
        $name = explode("/",$link);
        $name = $name[count($name)-1];
    
        $author = explode("/",$link);
        $author = $author[3];
    
        $category = $categories->find("h2 a");
        $category = $category[0]->plaintext;
    
        //print $category . " - " . $name . " - " . $author . " - " . $link . "\n";
    
        $records[] = array("link"=>$link, "name"=>$name, "author"=>$author, "category"=>$category);
    }
}

print "saving...\n";
$unique_keys = array("link");
$table_name = "repos";
scraperwiki::save_sqlite($unique_keys, $records, $table_name);
print "done\n";
?>
