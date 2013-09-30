<?php
require 'scraperwiki/simple_html_dom.php';           

$arr = array();

for ($i = 0; $i < 1;++$i) {
  $html = scraperWiki::scrape("http://irma.dk/includefiles/MODULER/CCMS/show_page.asp?iMappeID=491&sSideNavn=OpskriftListning&section=" . $i . "&task=sog&OpskriftNavn=&Attribute=&AttributeList=&OpskriftValgt=&selectshow=&kampagneId=&Ingr1=&Ingr2=&Ingr3=");
  $dom = new simple_html_dom();
  $dom->load($html);
  foreach($dom->find("li.txt h2 a") as $name) {
    $recipe = scraperWiki::scrape('http://irma.dk' . $name->href);
    $recipe_dom = new simple_html_dom();
    $recipe_dom->load($recipe);
    $ingredients = array();
    foreach ($recipe_dom->find('#main_content') as $content) {
        $title = $content->find('h1',0)->plaintext;
        $link = $name->href;
        foreach ($content->find('#formIngredienser input[type=checkbox]') as $ingredient_data) {
            $ingredients[] = $ingredient_data->value;
        }
        $arr[] = array(
            'title' => $title,
            'link' => $link,
            'ingredients' => implode(';', $ingredients),
        );
    }
  }
}


scraperwiki::save(array('link'), $arr); 

?><?php
require 'scraperwiki/simple_html_dom.php';           

$arr = array();

for ($i = 0; $i < 1;++$i) {
  $html = scraperWiki::scrape("http://irma.dk/includefiles/MODULER/CCMS/show_page.asp?iMappeID=491&sSideNavn=OpskriftListning&section=" . $i . "&task=sog&OpskriftNavn=&Attribute=&AttributeList=&OpskriftValgt=&selectshow=&kampagneId=&Ingr1=&Ingr2=&Ingr3=");
  $dom = new simple_html_dom();
  $dom->load($html);
  foreach($dom->find("li.txt h2 a") as $name) {
    $recipe = scraperWiki::scrape('http://irma.dk' . $name->href);
    $recipe_dom = new simple_html_dom();
    $recipe_dom->load($recipe);
    $ingredients = array();
    foreach ($recipe_dom->find('#main_content') as $content) {
        $title = $content->find('h1',0)->plaintext;
        $link = $name->href;
        foreach ($content->find('#formIngredienser input[type=checkbox]') as $ingredient_data) {
            $ingredients[] = $ingredient_data->value;
        }
        $arr[] = array(
            'title' => $title,
            'link' => $link,
            'ingredients' => implode(';', $ingredients),
        );
    }
  }
}


scraperwiki::save(array('link'), $arr); 

?>