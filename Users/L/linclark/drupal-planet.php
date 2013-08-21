<?php
require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();

//foreach (get_roster() as $blog_name => $blog_link) {
$blog_name = 'Nick Lewis';
$blog_link = 'http://www.nicklewis.org/drupal?page=6';

    $record = array(
        'blog_name' => $blog_name,
        'blog_link' => $blog_link,
    );
    save_nodes($blog_link, $record);
//}

function get_roster() {
    $blogs = array();
    $dom = new simple_html_dom();
    $planet = scraperwiki::scrape('http://drupal.org/planet');
    $dom->load($planet);

    foreach ($dom->find('#block-drupalorg_news-planet-list .item-list li') as $li) {
        $a = $li->find('a');
        $blog = $a[0];
        $blogs[$blog->plaintext] = $blog->href;
    }

    return $blogs;
}

function save_nodes($blog_link, $record) {
    $parsed_url = parse_url($record['blog_link']);
    $site_link = $parsed_url['host'];

    $dom = new simple_html_dom();
    $html = scraperwiki::scrape($blog_link);

    $dom->load($html);

    if ($nodes = $dom->find('.node')) { }
    elseif ($nodes = $dom->find('#content .blog')) { }
    elseif ($nodes = $dom->find('.view-id-planet_drupal .view-content .even')) { }
    elseif ($nodes = $dom->find('.archive')) { }
    elseif ($nodes = $dom->find('.post')) { }
    elseif ($nodes = $dom->find('.page-section-notfirst .page-section-inner')) { }
    elseif ($nodes = $dom->find('.article')) { }
    //elseif ($nodes = $dom->find('.blog-post')) { }
    elseif ($nodes = $dom->find('.view-blogs .views-row')) { }
    elseif ($nodes = $dom->find('.views-row .blog-right')) { }
    elseif ($nodes = $dom->find('#content-area .views-row')) { }
    elseif ($nodes = $dom->find('#content-area .panel-pane-blogs .views-row')) { }
    elseif ($nodes = $dom->find('.center-column .panel-pane .views-row')) { }
    elseif ($nodes = $dom->find('.entry')) { }
    elseif ($nodes = $dom->find('.main-column')) { }
    elseif ($nodes = $dom->find('.main')) { }
    elseif ($nodes = $dom->find('.serendipity_Entry_Date')) {}
    elseif ($nodes = $dom->find('#main-content .node-inner')) { }
    elseif ($nodes = $dom->find('.regularitem')) { }
    elseif ($nodes = $dom->find('.title')) { }
    // Becca's blog
    /*elseif ($nodes = $dom->find('#thing-navigation .left')) { 
        $next = $dom->find('#thing-navigation .left a');
        if (!empty($next)) {
            $link = $next[0]->href;
            save_nodes($link, $record);
        } 
        $nodes = $dom->find('.thing-wrap');
    }*/

unset($nodes[0]);
unset($nodes[1]);


    foreach ($nodes as $node) {
//print $node->plaintext;
        if ($h = $node->find('.serendipity_title')) { $h_level = 'h1'; }
        elseif ($h = $node->find('.entry-title h3')) { $h_level = 'h1'; }
        elseif ($h = $node->find('h1')) { $h_level = 'h1'; }
        elseif ($h = $node->find('h2')) { $h_level = 'h2'; }
        elseif ($h = $node->find('h3')) { $h_level = 'h3'; }
        elseif ($h = $node->find('h4')) { $h_level = 'h4'; }
        elseif ($h = $node->find('.views-field-title')) { }
        elseif ($h = $node->find('.blog-title')) { }
        elseif ($h = $node->find('.title')) { }
        elseif ($h = $node->find('.titulo')) { }
        elseif ($h = $node->find('.node-readmore')) {
        }

        $record['title'] = $h[0]->plaintext;
        $record['teaser'] = $node->plaintext;
print $record['title'];
        if ($link = $h[0]->find('a')) { }
        elseif ($link = $node->find('.views-field-title a')) { }

        $full_text = new simple_html_dom();
        $uri = $site_link . $link[0]->href;
        $record['uri'] = $uri;
        $html = scraperwiki::scrape($uri);

        $full_text->load($html);

        // Get taxonomy terms.
        $terms = array();
        if ($term_li = $full_text->find('.field-type-taxonomy-term-reference a')) { }
        elseif ($term_li = $full_text->find('#block-swentel-topics a')) { }
        elseif ($term_li = $node->find('.serendipity_entryFooter a')) { }
        elseif ($term_li = $full_text->find('.the_category a')) { }
        elseif ($term_li = $full_text->find('.p-cat a')) { }
        elseif ($term_li = $full_text->find('.terms a')) { }
        elseif ($term_li = $full_text->find('.tags a')) { }
        elseif ($term_li = $full_text->find('.taxonomy a')) { }
        elseif ($term_li = $full_text->find('.field-terms a')) { }            
        elseif ($term_li = $full_text->find('.views-field-field-topic a')) { }
        //elseif ($term_li = $full_text->find('.inline a')) { }
        elseif ($term_li = $full_text->find('.meta a')) { }
        //elseif ($term_li = $full_text->find('.node .links a')) { }
        elseif ($term_li = $full_text->find('.pane-node-terms a')) { }
        elseif ($term_li = $full_text->find('.category')) { }
        elseif ($term_li = $full_text->find('.post-category a')) { }
        elseif ($term_li = $full_text->find('.terms a')) { }
        elseif ($term_li = $full_text->find('.term-list a')) { }
        elseif ($term_li = $full_text->find('.entryterms a')) { }
        elseif ($term_li = $full_text->find('.entry-info a')) { }
        elseif ($term_li = $full_text->find('.entry-utility a')) { }
        //elseif ($term_li = $full_text->find('.submitted a')) { }
        elseif ($term_li = $full_text->find('.post-subhead a')) { }
        elseif ($term_li = $full_text->find('.catlist a')) { }
        elseif ($term_li = $full_text->find('small a')) { }
        //elseif ($term_li = $full_text->find('.content a')) { }
        elseif ($term_li = $full_text->find('.thing-meta')) { }
        foreach ($term_li as $term) {
            $terms[] = $term->plaintext;
        }
        $record['terms'] = implode(', ', $terms);

        // Get submitted line.
        if ($sub = $full_text->find('.dateblock')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.submitted span')) { $record['submitted'] = $sub[0]->content; }
        elseif ($sub = $full_text->find('.pubdate')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.p-time')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.post-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.submitted em')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.contentdate')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.datestamp')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.posted-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.post-info')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.the_time')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('time')) { $record['submitted'] = $sub[0]->datetime; }
        elseif ($sub = $full_text->find('.field-post-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.field-name-post-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.entry-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.entrydate')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.creation-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.views-field-created')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.meta')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.info')) { $record['submitted'] = $sub[0]->plaintext; }
        //elseif ($sub = $full_text->find('.node .links')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.node_submitted')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('#submitted')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.terms')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.node-submitted')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.thing-meta')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.comment-date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.pane-node-created')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.post-subhead')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.post-calendar')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.date-tab')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.info')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('small')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.node-meta')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $node->find('.serendipity_date')) { $record['submitted'] = $sub[0]->plaintext; }
        elseif ($sub = $full_text->find('.section-sideblock')) { $record['submitted'] = $sub[0]->plaintext; }
        else {
            $sub = $full_text->find('.submitted');
            $record['submitted'] = $sub[0]->plaintext;
        }

        // For archived posts.
        /*$parts = explode('/', $link[0]);
        $timestamp = mktime(0, 0, 0, $parts[3], $parts[4], $parts[2]);
        $sub = date("M d Y", $timestamp);
        $record['submitted'] = $sub;*/

            // Get body.
            if ($n = $full_text->find('.node .content')) { }
            elseif ($n = $full_text->find('.node_content')) { }
            elseif ($n = $node->find('.serendipity_entry')) { }
            elseif ($n = $full_text->find('.main')) { }
            elseif ($n = $full_text->find('.content')) { }
            elseif ($n = $full_text->find('.field-name-body')) { }
            elseif ($n = $full_text->find('.body')) { }
            elseif ($n = $full_text->find('.node .node-content')) { }
            elseif ($n = $full_text->find('.node')) { }
            elseif ($n = $full_text->find('.entry')) { }
            elseif ($n = $full_text->find('.post')) { }
            elseif ($n = $full_text->find('.node-inner')) { }
            elseif ($n = $full_text->find('.nodeContent')) { }
            elseif ($n = $full_text->find('.pane-node-body')) { }
            elseif ($n = $full_text->find('.field-body')) { }
            elseif ($n = $full_text->find('.post-body')) { }
            elseif ($n = $full_text->find('.more-description')) { }
            elseif ($n = $full_text->find('.thing-content')) { }
            $record['body'] = $n[0]->plaintext;

        scraperwiki::save(array('uri'), $record);
    }
    if ($next = $dom->find('.pager-next a')) {  }
    elseif ($next = $dom->find('.pager-next')) {  }
    elseif ($next = $dom->find('.blog-pager-older-link')) {  }
    elseif ($next = $dom->find('.nav-previous')) {  }
    if (!empty($next)) {
        $link = str_replace('0%2C', '', $next[0]->href);
        print $link;
        save_nodes($site_link . $link, $record);
    }
}

?>
