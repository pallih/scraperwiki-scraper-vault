<?php
error_reporting(E_ALL ^ E_NOTICE);
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://openlylocal.com/hyperlocal_sites?independent=true");
$html = str_get_html($html_content);

foreach ($html->find("li.country li") as $el) {           
    if ($el->find("a.twitter")){ // don't bother with non-Twitter folks
        
        // Get the site name
        $title = $el->find("a.hyperlocal_site_link",0);
        $title = $title->innertext;
        
        // Get the URL
        $url = $el->find("a.external",0);
        $url = $url->href;
        
        // Get Twitter
        $twitter = $el->find("a.twitter",0);
        $twitter = $twitter->href;
        
        // remove nonsense from the Twitter URL
        $remove = array('/', 'https', 'http', ':', 'twitter', '.com');
        $twitter = '@'.str_replace($remove, '', $twitter);
        
        // Create a number of different messages to use
        $msgs = array(
            "We've arranged some free training for site owners like you to help with sustainability. Details at http://bit.ly/Re5nV1", //120
            "Thought you'd be interested in our free training to help you with sustainability. Details at http://bit.ly/Re5nV1", //113
            "We've got free training in ad sales to help you with sustainability. Details and registration at http://bit.ly/Re5nV1", //117
            "There's some free ad sales training available to help you make your site more sustainable. Details are at http://bit.ly/Re5nV1", //126
            "If you struggle to make your site sustainabile, you might be interested in our free training: http://bit.ly/Re5nV1" //114
        );
        $message = $twitter.' '.$msgs[rand(0,4)];
        
        $save = array('name'=>$title, 'url'=>$url, 'twitter'=>$twitter, 'message'=>$message);
        
        scraperwiki::save(array('name','url','twitter','message'), $save);
    }
}

?>
<?php
error_reporting(E_ALL ^ E_NOTICE);
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://openlylocal.com/hyperlocal_sites?independent=true");
$html = str_get_html($html_content);

foreach ($html->find("li.country li") as $el) {           
    if ($el->find("a.twitter")){ // don't bother with non-Twitter folks
        
        // Get the site name
        $title = $el->find("a.hyperlocal_site_link",0);
        $title = $title->innertext;
        
        // Get the URL
        $url = $el->find("a.external",0);
        $url = $url->href;
        
        // Get Twitter
        $twitter = $el->find("a.twitter",0);
        $twitter = $twitter->href;
        
        // remove nonsense from the Twitter URL
        $remove = array('/', 'https', 'http', ':', 'twitter', '.com');
        $twitter = '@'.str_replace($remove, '', $twitter);
        
        // Create a number of different messages to use
        $msgs = array(
            "We've arranged some free training for site owners like you to help with sustainability. Details at http://bit.ly/Re5nV1", //120
            "Thought you'd be interested in our free training to help you with sustainability. Details at http://bit.ly/Re5nV1", //113
            "We've got free training in ad sales to help you with sustainability. Details and registration at http://bit.ly/Re5nV1", //117
            "There's some free ad sales training available to help you make your site more sustainable. Details are at http://bit.ly/Re5nV1", //126
            "If you struggle to make your site sustainabile, you might be interested in our free training: http://bit.ly/Re5nV1" //114
        );
        $message = $twitter.' '.$msgs[rand(0,4)];
        
        $save = array('name'=>$title, 'url'=>$url, 'twitter'=>$twitter, 'message'=>$message);
        
        scraperwiki::save(array('name','url','twitter','message'), $save);
    }
}

?>
