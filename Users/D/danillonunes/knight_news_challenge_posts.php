<?php
define('MAIN_DOMAIN', 'http://newschallenge.tumblr.com');
define('DISQUS_DOMAIN', 'http://newschallenge.disqus.com');

init();

function init() {
    require 'scraperwiki/simple_html_dom.php';
    $dom = page_load(MAIN_DOMAIN . '/archive');
    $all_posts = array();

    do {
        $posts = get_posts($dom);
        $all_posts = array_merge($all_posts, $posts);
    } while ($dom = next_page_load($dom));

    posts_get_data($all_posts, 'save_posts');
}

/**
 * Get posts from DOM object.
 *
 * @param $dom
 *   DOM object from scraperWiki.
 *
 * @return
 *   Indexed array with loaded posts.
 */
function get_posts($dom) {
    $posts = array();

    foreach($dom->find('a.regular') as $post) {
        $id = explode('_', $post->getAttribute('id'));
        $id = $id[1];
        $posts[$id]['id'] = $id;

        $url = $post->getAttribute('href');
        $posts[$id]['url'] = $url;
    }
    return $posts;
}

function posts_get_data($posts, $callback = '') {
    foreach ($posts as $post) {
        $id = $post['id'];
        $url = $post['url'];
        $today = date('m-d');
        $post_page = page_load($url);

        $title = $post_page->find('div.single h2');
        $post['title'] = count($title) ? $title[0]->plaintext : NULL;

        $description = $post_page->find('div.single');
        $post['description'] = count($description) ? $description[0]->innertext() : NULL;

        $likes = $post_page->find('div.single a.like-link');
        $post['likes-' . $today] = count($likes) ? $likes[0]->plaintext : NULL;

        $disqus_count_url = DISQUS_DOMAIN . '/count.js?q=1&0,' . htmlspecialchars($url) . '&1=2,' . htmlspecialchars($url);
        $disqus_count_handle = fopen($disqus_count_url, 'r');
        $disqus_count = stream_get_contents($disqus_count_handle);
        fclose($disqus_count_handle);
        preg_match('/DISQUSWIDGETS.displayCount\((.*)\)/', $disqus_count, $disqus_count_matches);
        $disqus_count_json = json_decode($disqus_count_matches[1]);
        $comments = $disqus_count_json->counts[0]->comments;

        if (is_numeric($comments)) {
            $comments = $post_page->find('a.postComment');
            $post['comments-' . $today] = $comments;
        }
        else {
            print_r($comments);
            print "\n";
            print_r($disqus_count_url);
            print "\n";
        }

        if (function_exists($callback)) {
            $callback(array($id => $post));
        }
    }

//        $post_single = $post_page->find('div.single');

//        $title2 = $post_single[0]->children('h2');
/**
        $title = $post_single->find('h2');
        $description = $post->find('div.overprint');
        $likes = $post_single->find('a.like-link');
        $comments = $post_single->find('a.postComment');

print_r(array('likes' => $likes, 'comments' => $comments));
**/
}

/**
 * Save posts into database.
 *
 * @param $posts
 *   Array of posts to be saved.
 */
function save_posts($posts) {
    foreach ($posts as $id => $post) {
        scraperwiki::save(array('id'), $post);
    }
}

/**
 * Load a page as a DOM object.
 *
 * @param $url
 *   URL to load.
 *
 * @return
 *   DOM object from post page.
 */
function page_load($url) {
    $html = scraperWiki::scrape($url);

    $dom = str_get_html($html);

    return $dom;
}

/**
 * Load html content from next page.
 *
 * @param $dom
 *   DOM object from current page.
 *
 * @return
 *   DOM object from the next page.
 */
function next_page_load($dom) {
    $next = $dom->find('a#next_page_link');

    if (is_object($next[0])) {
        $nexturl = MAIN_DOMAIN . $next[0]->getAttribute('href');

        $dom = page_load($nexturl);

        return $dom;
    }

    return FALSE;
}

?>
<?php
define('MAIN_DOMAIN', 'http://newschallenge.tumblr.com');
define('DISQUS_DOMAIN', 'http://newschallenge.disqus.com');

init();

function init() {
    require 'scraperwiki/simple_html_dom.php';
    $dom = page_load(MAIN_DOMAIN . '/archive');
    $all_posts = array();

    do {
        $posts = get_posts($dom);
        $all_posts = array_merge($all_posts, $posts);
    } while ($dom = next_page_load($dom));

    posts_get_data($all_posts, 'save_posts');
}

/**
 * Get posts from DOM object.
 *
 * @param $dom
 *   DOM object from scraperWiki.
 *
 * @return
 *   Indexed array with loaded posts.
 */
function get_posts($dom) {
    $posts = array();

    foreach($dom->find('a.regular') as $post) {
        $id = explode('_', $post->getAttribute('id'));
        $id = $id[1];
        $posts[$id]['id'] = $id;

        $url = $post->getAttribute('href');
        $posts[$id]['url'] = $url;
    }
    return $posts;
}

function posts_get_data($posts, $callback = '') {
    foreach ($posts as $post) {
        $id = $post['id'];
        $url = $post['url'];
        $today = date('m-d');
        $post_page = page_load($url);

        $title = $post_page->find('div.single h2');
        $post['title'] = count($title) ? $title[0]->plaintext : NULL;

        $description = $post_page->find('div.single');
        $post['description'] = count($description) ? $description[0]->innertext() : NULL;

        $likes = $post_page->find('div.single a.like-link');
        $post['likes-' . $today] = count($likes) ? $likes[0]->plaintext : NULL;

        $disqus_count_url = DISQUS_DOMAIN . '/count.js?q=1&0,' . htmlspecialchars($url) . '&1=2,' . htmlspecialchars($url);
        $disqus_count_handle = fopen($disqus_count_url, 'r');
        $disqus_count = stream_get_contents($disqus_count_handle);
        fclose($disqus_count_handle);
        preg_match('/DISQUSWIDGETS.displayCount\((.*)\)/', $disqus_count, $disqus_count_matches);
        $disqus_count_json = json_decode($disqus_count_matches[1]);
        $comments = $disqus_count_json->counts[0]->comments;

        if (is_numeric($comments)) {
            $comments = $post_page->find('a.postComment');
            $post['comments-' . $today] = $comments;
        }
        else {
            print_r($comments);
            print "\n";
            print_r($disqus_count_url);
            print "\n";
        }

        if (function_exists($callback)) {
            $callback(array($id => $post));
        }
    }

//        $post_single = $post_page->find('div.single');

//        $title2 = $post_single[0]->children('h2');
/**
        $title = $post_single->find('h2');
        $description = $post->find('div.overprint');
        $likes = $post_single->find('a.like-link');
        $comments = $post_single->find('a.postComment');

print_r(array('likes' => $likes, 'comments' => $comments));
**/
}

/**
 * Save posts into database.
 *
 * @param $posts
 *   Array of posts to be saved.
 */
function save_posts($posts) {
    foreach ($posts as $id => $post) {
        scraperwiki::save(array('id'), $post);
    }
}

/**
 * Load a page as a DOM object.
 *
 * @param $url
 *   URL to load.
 *
 * @return
 *   DOM object from post page.
 */
function page_load($url) {
    $html = scraperWiki::scrape($url);

    $dom = str_get_html($html);

    return $dom;
}

/**
 * Load html content from next page.
 *
 * @param $dom
 *   DOM object from current page.
 *
 * @return
 *   DOM object from the next page.
 */
function next_page_load($dom) {
    $next = $dom->find('a#next_page_link');

    if (is_object($next[0])) {
        $nexturl = MAIN_DOMAIN . $next[0]->getAttribute('href');

        $dom = page_load($nexturl);

        return $dom;
    }

    return FALSE;
}

?>
