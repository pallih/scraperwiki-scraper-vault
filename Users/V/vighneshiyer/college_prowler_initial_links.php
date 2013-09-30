<?php

require 'scraperwiki/simple_html_dom.php';
$pages = array("http://collegeprowler.com/all/?LetterGroup=3-A", 
"http://collegeprowler.com/all/?LetterGroup=B", 
"http://collegeprowler.com/all/?LetterGroup=C",
"http://collegeprowler.com/all/?LetterGroup=D",
"http://collegeprowler.com/all/?LetterGroup=E",
"http://collegeprowler.com/all/?LetterGroup=F",
"http://collegeprowler.com/all/?LetterGroup=G",
"http://collegeprowler.com/all/?LetterGroup=H",
"http://collegeprowler.com/all/?LetterGroup=I",
"http://collegeprowler.com/all/?LetterGroup=J",
"http://collegeprowler.com/all/?LetterGroup=K",
"http://collegeprowler.com/all/?LetterGroup=L",
"http://collegeprowler.com/all/?LetterGroup=M",
"http://collegeprowler.com/all/?LetterGroup=N",
"http://collegeprowler.com/all/?LetterGroup=O",
"http://collegeprowler.com/all/?LetterGroup=P",
"http://collegeprowler.com/all/?LetterGroup=Q-R",
"http://collegeprowler.com/all/?LetterGroup=S",
"http://collegeprowler.com/all/?LetterGroup=T",
"http://collegeprowler.com/all/?LetterGroup=U",
"http://collegeprowler.com/all/?LetterGroup=V",
"http://collegeprowler.com/all/?LetterGroup=W",
"http://collegeprowler.com/all/?LetterGroup=X-Z");

foreach($pages as $page){
    $html_content = scraperwiki::scrape($page);
    $html = str_get_html($html_content);

    foreach ($html->find("div.columns ul li a") as $link) {  
        $name = $link -> innertext; 
        scraperwiki::save_sqlite(array("CollegeName"),array("CollegeName"=>html_entity_decode($name), "CollegeLink"=>$link -> href));       
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';
$pages = array("http://collegeprowler.com/all/?LetterGroup=3-A", 
"http://collegeprowler.com/all/?LetterGroup=B", 
"http://collegeprowler.com/all/?LetterGroup=C",
"http://collegeprowler.com/all/?LetterGroup=D",
"http://collegeprowler.com/all/?LetterGroup=E",
"http://collegeprowler.com/all/?LetterGroup=F",
"http://collegeprowler.com/all/?LetterGroup=G",
"http://collegeprowler.com/all/?LetterGroup=H",
"http://collegeprowler.com/all/?LetterGroup=I",
"http://collegeprowler.com/all/?LetterGroup=J",
"http://collegeprowler.com/all/?LetterGroup=K",
"http://collegeprowler.com/all/?LetterGroup=L",
"http://collegeprowler.com/all/?LetterGroup=M",
"http://collegeprowler.com/all/?LetterGroup=N",
"http://collegeprowler.com/all/?LetterGroup=O",
"http://collegeprowler.com/all/?LetterGroup=P",
"http://collegeprowler.com/all/?LetterGroup=Q-R",
"http://collegeprowler.com/all/?LetterGroup=S",
"http://collegeprowler.com/all/?LetterGroup=T",
"http://collegeprowler.com/all/?LetterGroup=U",
"http://collegeprowler.com/all/?LetterGroup=V",
"http://collegeprowler.com/all/?LetterGroup=W",
"http://collegeprowler.com/all/?LetterGroup=X-Z");

foreach($pages as $page){
    $html_content = scraperwiki::scrape($page);
    $html = str_get_html($html_content);

    foreach ($html->find("div.columns ul li a") as $link) {  
        $name = $link -> innertext; 
        scraperwiki::save_sqlite(array("CollegeName"),array("CollegeName"=>html_entity_decode($name), "CollegeLink"=>$link -> href));       
    }
}

?>
