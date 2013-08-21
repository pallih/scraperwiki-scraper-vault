<?php

# Scrape http://www.talkingwestcheshire.org/talking_chester/events_-_chester/local_community_groups.aspx

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// Set the source and grab it
$html_content = scraperwiki::scrape("http://www.talkingwestcheshire.org/talking_chester/events_-_chester/local_community_groups.aspx");
$html = str_get_html($html_content);

$cg = array(); // current group placeholder

foreach ($html->find("#content article", 0)->children() as $e){
    if ($e->tag == 'h3'){
        $cg['title'] = trim(str_replace("\xA0", ' ', html_entity_decode($e->innertext)));
    }

    if ($e->tag == 'p'){
        $cg['desc'] = $e->innertext;
    }

    if ($e->tag == 'ul'){

        foreach ($e->children() as $child){
            switch ($child->first_child()->innertext){
    
                case "Meet at:":
                    $cg['loc'] = trim(str_replace('Meet at:', '', $child->plaintext));
                    break;

                case "Contact:":
                    $cg['contact'] = trim(str_replace('Contact:', '', $child->plaintext));
                    break;

                case "Telephone:":
                    $cg['phone'] = trim(str_replace('Telephone:', '', $child->plaintext));
                    break;

                case "Email:":
                    $cg['email'] = trim(str_replace('Email:', '', $child->plaintext));
                    break;

                case "Website:":
                    $cg['website'] = $child->children(1)->href;
                    break;
                
            }
        }

        // add a unique identifier
        if (array_key_exists('title', $cg))
            $cg['id'] = md5($cg['title']);

        $i++;
    }

    if (array_key_exists('id', $cg))
        scraperwiki::save_sqlite(array('id'), $cg);

}


?>
