<?php

require 'scraperwiki/simple_html_dom.php';


// 1m monsters
$html_content0 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1000000");
$html0 = str_get_html($html_content0);

$arr = array(); 

foreach ($html0->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1m"));
}

// 1.5m monsters
$html_content = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1500000");
$html = str_get_html($html_content); 

foreach ($html->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1.5m"));
}

// 2m monsters
$html_content2 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=2000000");
$html2 = str_get_html($html_content2);

foreach ($html2->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"2m"));
}

// 3m monsters
$html_content3 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=3000000");
$html3 = str_get_html($html_content3);

foreach ($html3->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"3m"));
}

// 4m monsters
$html_content4 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=4000000");
$html4 = str_get_html($html_content4);

foreach ($html4->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"4m"));
}

// 5m monsters
$html_content5 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=5000000");
$html5 = str_get_html($html_content5);

foreach ($html5->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"5m"));
}

print_r($records); 

?>
<?php

require 'scraperwiki/simple_html_dom.php';


// 1m monsters
$html_content0 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1000000");
$html0 = str_get_html($html_content0);

$arr = array(); 

foreach ($html0->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1m"));
}

// 1.5m monsters
$html_content = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1500000");
$html = str_get_html($html_content); 

foreach ($html->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1.5m"));
}

// 2m monsters
$html_content2 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=2000000");
$html2 = str_get_html($html_content2);

foreach ($html2->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"2m"));
}

// 3m monsters
$html_content3 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=3000000");
$html3 = str_get_html($html_content3);

foreach ($html3->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"3m"));
}

// 4m monsters
$html_content4 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=4000000");
$html4 = str_get_html($html_content4);

foreach ($html4->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"4m"));
}

// 5m monsters
$html_content5 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=5000000");
$html5 = str_get_html($html_content5);

foreach ($html5->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"5m"));
}

print_r($records); 

?>
<?php

require 'scraperwiki/simple_html_dom.php';


// 1m monsters
$html_content0 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1000000");
$html0 = str_get_html($html_content0);

$arr = array(); 

foreach ($html0->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1m"));
}

// 1.5m monsters
$html_content = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1500000");
$html = str_get_html($html_content); 

foreach ($html->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1.5m"));
}

// 2m monsters
$html_content2 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=2000000");
$html2 = str_get_html($html_content2);

foreach ($html2->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"2m"));
}

// 3m monsters
$html_content3 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=3000000");
$html3 = str_get_html($html_content3);

foreach ($html3->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"3m"));
}

// 4m monsters
$html_content4 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=4000000");
$html4 = str_get_html($html_content4);

foreach ($html4->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"4m"));
}

// 5m monsters
$html_content5 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=5000000");
$html5 = str_get_html($html_content5);

foreach ($html5->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"5m"));
}

print_r($records); 

?>
<?php

require 'scraperwiki/simple_html_dom.php';


// 1m monsters
$html_content0 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1000000");
$html0 = str_get_html($html_content0);

$arr = array(); 

foreach ($html0->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1m"));
}

// 1.5m monsters
$html_content = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=1500000");
$html = str_get_html($html_content); 

foreach ($html->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"1.5m"));
}

// 2m monsters
$html_content2 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=2000000");
$html2 = str_get_html($html_content2);

foreach ($html2->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"2m"));
}

// 3m monsters
$html_content3 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=3000000");
$html3 = str_get_html($html_content3);

foreach ($html3->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"3m"));
}

// 4m monsters
$html_content4 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=4000000");
$html4 = str_get_html($html_content4);

foreach ($html4->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"4m"));
}

// 5m monsters
$html_content5 = scraperwiki::scrape("http://www.puzzledragonx.com/en/experiencechart.asp?c=5000000");
$html5 = str_get_html($html_content5);

foreach ($html5->find("td.icon img.onload") as $el) {  
    $monster = $el->title;
    array_push($arr, $monster);
    $records = scraperwiki::save_sqlite(array("monster"), array("monster"=>$monster, "growth"=>"5m"));
}

print_r($records); 

?>
