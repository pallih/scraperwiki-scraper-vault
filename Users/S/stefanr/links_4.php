<?php 
require 'scraperwiki/simple_html_dom.php';

$location = "http://www.bertelsmann-stiftung.de/cps/rde/xchg/bst/hs.xsl/index.html";
/*
scraperwiki::sqliteexecute("create table if not exists pages (`url` string, `processed` int)");
scraperwiki::sqlitecommit();
*/
// initial call -> pages table is empty or has no entries with processed = 0
$waiting = scraperwiki::select("count(*) as c from pages where processed=0");
$waiting = $waiting[0]['c'];
if ($waiting == 0) {
    print "initial call - starting with url " . $location . "\n";
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 0), "pages", 0);
    $waiting = 1;
}
/*
scraperwiki::sqliteexecute("delete from pages where url like '%mpeg'");            
scraperwiki::sqlitecommit();
*/

$processed = scraperwiki::select("count(*) as c from pages where processed=1");
$processed = $processed[0]['c'];

while ($waiting > 0) {
    $externals = scraperwiki::select("count(*) as c from swdata where type like 'external'");
    $externals = $externals[0]['c'];

    print "pages waiting: " . $waiting . " | pages processed: " . $processed . " | external links found: " . $externals . "\n";
    $location = scraperwiki::select("url from pages where processed=0 limit 0,1");
    $location = $location[0]['url'];
    
    findLinksOnPage($location);
    
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 1), "pages", 0);
    
    $waiting = scraperwiki::select("count(*) as c from pages where processed=0");
    $waiting = $waiting[0]['c'];
    
    $processed = scraperwiki::select("count(*) as c from pages  where processed=1");
    $processed = $processed[0]['c'];
}

function findLinksOnPage($location) {
    print "loading page " . $location . "\n";
    $html = scraperWiki::scrape($location);           
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("a") as $anchor){
        $href = $anchor->getAttribute('href');
        $href = preg_replace("/SID-[0-9a-fA-F]+\-[0-9a-fA-F]+\//i", "", $href);
        $type = "";
        if (preg_match("/(http|https|ftp):\/\/([\w-\d]+\.)+[\w-\d]+/i", $href, $m)) {
            if ("bertelsmann-stiftung." == $m[2]) 
                $type = 'internal';
            else
                $type = 'external';
        } else if (preg_match("/(\/[\w~,;\-\.\/?%&+#=]*)/i", $href)) {
            $type = 'internal';
            $href = url_to_absolute($location, $href);
        } else {
            $type = 'unknown';
        }
        scraperwiki::save(array('href'), array('on_page' => $location, 'href' => $href, 'type' => $type, 'exported' => 0));
        
        // remember to follow an internal link, if not already done
        if ($type == 'internal') {
            if (!preg_match("/.*\.mpeg$/i", $href) && !preg_match("/.*\.exe$/i", $href) && !preg_match("/.*\.pdf$/i", $href) && !preg_match("/.*\.mp3$/i", $href) && !preg_match("/.*\.jpg$/i", $href) && !preg_match("/.*\.zip$/i", $href) && !preg_match("/.*\.doc$/i", $href) && !preg_match("/.*\.ppt$/i", $href)) {
                $count = scraperwiki::select("count(*) as c from pages where url like '" . ($href) . "'");
                $count = $count[0]['c'];
                if ($count > 0) {
                    //print "page already processed (or reserved): " . $href . "\n";
                } else {
                    scraperwiki::save_sqlite(array('url'), array('url' => ($href), 'processed' => 0), "pages", 0);
                }
            }
        }
    }
}

function url_to_absolute( $baseUrl, $relativeUrl )
{
    // If relative URL has a scheme, clean path and return.
    $r = split_url( $relativeUrl );
    if ( $r === FALSE )
        return FALSE;
    if ( !empty( $r['scheme'] ) )
    {
        if ( !empty( $r['path'] ) && $r['path'][0] == '/' )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
 
    // Make sure the base URL is absolute.
    $b = split_url( $baseUrl );
    if ( $b === FALSE || empty( $b['scheme'] ) || empty( $b['host'] ) )
        return FALSE;
    $r['scheme'] = $b['scheme'];
 
    // If relative URL has an authority, clean path and return.
    if ( isset( $r['host'] ) )
    {
        if ( !empty( $r['path'] ) )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
    unset( $r['port'] );
    unset( $r['user'] );
    unset( $r['pass'] );
 
    // Copy base authority.
    $r['host'] = $b['host'];
    if ( isset( $b['port'] ) ) $r['port'] = $b['port'];
    if ( isset( $b['user'] ) ) $r['user'] = $b['user'];
    if ( isset( $b['pass'] ) ) $r['pass'] = $b['pass'];
 
    // If relative URL has no path, use base path
    if ( empty( $r['path'] ) )
    {
        if ( !empty( $b['path'] ) )
            $r['path'] = $b['path'];
        if ( !isset( $r['query'] ) && isset( $b['query'] ) )
            $r['query'] = $b['query'];
        return join_url( $r );
    }
 
    // If relative URL path doesn't start with /, merge with base path
    if ( $r['path'][0] != '/' )
    {
        $base = mb_strrchr( $b['path'], '/', TRUE, 'UTF-8' );
        if ( $base === FALSE ) $base = '';
        $r['path'] = $base . '/' . $r['path'];
    }
    $r['path'] = url_remove_dot_segments( $r['path'] );
    return join_url( $r );
}

function split_url( $url, $decode=TRUE )
{
    $xunressub     = 'a-zA-Z\d\-._~\!$&\'()*+,;=';
    $xpchar        = $xunressub . ':@%';

    $xscheme       = '([a-zA-Z][a-zA-Z\d+-.]*)';

    $xuserinfo     = '((['  . $xunressub . '%]*)' .
                     '(:([' . $xunressub . ':%]*))?)';

    $xipv4         = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})';

    $xipv6         = '(\[([a-fA-F\d.:]+)\])';

    $xhost_name    = '([a-zA-Z\d-.%]+)';

    $xhost         = '(' . $xhost_name . '|' . $xipv4 . '|' . $xipv6 . ')';
    $xport         = '(\d*)';
    $xauthority    = '((' . $xuserinfo . '@)?' . $xhost .
                     '?(:' . $xport . ')?)';

    $xslash_seg    = '(/[' . $xpchar . ']*)';
    $xpath_authabs = '((//' . $xauthority . ')((/[' . $xpchar . ']*)*))';
    $xpath_rel     = '([' . $xpchar . ']+' . $xslash_seg . '*)';
    $xpath_abs     = '(/(' . $xpath_rel . ')?)';
    $xapath        = '(' . $xpath_authabs . '|' . $xpath_abs .
                     '|' . $xpath_rel . ')';

    $xqueryfrag    = '([' . $xpchar . '/?' . ']*)';

    $xurl          = '^(' . $xscheme . ':)?' .  $xapath . '?' .
                     '(\?' . $xqueryfrag . ')?(#' . $xqueryfrag . ')?$';
 
 
    // Split the URL into components.
    if ( !preg_match( '!' . $xurl . '!', $url, $m ) )
        return FALSE;
 
    if ( !empty($m[2]) )        $parts['scheme']  = strtolower($m[2]);
 
    if ( !empty($m[7]) ) {
        if ( isset( $m[9] ) )   $parts['user']    = $m[9];
        else            $parts['user']    = '';
    }
    if ( !empty($m[10]) )       $parts['pass']    = $m[11];
 
    if ( !empty($m[13]) )       $h=$parts['host'] = $m[13];
    else if ( !empty($m[14]) )  $parts['host']    = $m[14];
    else if ( !empty($m[16]) )  $parts['host']    = $m[16];
    else if ( !empty( $m[5] ) ) $parts['host']    = '';
    if ( !empty($m[17]) )       $parts['port']    = $m[18];
 
    if ( !empty($m[19]) )       $parts['path']    = $m[19];
    else if ( !empty($m[21]) )  $parts['path']    = $m[21];
    else if ( !empty($m[25]) )  $parts['path']    = $m[25];
 
    if ( !empty($m[27]) )       $parts['query']   = $m[28];
    if ( !empty($m[29]) )       $parts['fragment']= $m[30];
 
    if ( !$decode )
        return $parts;
    if ( !empty($parts['user']) )
        $parts['user']     = rawurldecode( $parts['user'] );
    if ( !empty($parts['pass']) )
        $parts['pass']     = rawurldecode( $parts['pass'] );
    if ( !empty($parts['path']) )
        $parts['path']     = rawurldecode( $parts['path'] );
    if ( isset($h) )
        $parts['host']     = rawurldecode( $parts['host'] );
    if ( !empty($parts['query']) )
        $parts['query']    = rawurldecode( $parts['query'] );
    if ( !empty($parts['fragment']) )
        $parts['fragment'] = rawurldecode( $parts['fragment'] );
    return $parts;
}

function join_url( $parts, $encode=TRUE )
{
    if ( $encode )
    {
        if ( isset( $parts['user'] ) )
            $parts['user']     = rawurlencode( $parts['user'] );
        if ( isset( $parts['pass'] ) )
            $parts['pass']     = rawurlencode( $parts['pass'] );
        if ( isset( $parts['host'] ) &&
            !preg_match( '!^(\[[\da-f.:]+\]])|([\da-f.:]+)$!ui', $parts['host'] ) )
            $parts['host']     = rawurlencode( $parts['host'] );
        if ( !empty( $parts['path'] ) )
            $parts['path']     = preg_replace( '!%2F!ui', '/',
                rawurlencode( $parts['path'] ) );
        if ( isset( $parts['query'] ) )
            $parts['query']    = rawurlencode( $parts['query'] );
        if ( isset( $parts['fragment'] ) )
            $parts['fragment'] = rawurlencode( $parts['fragment'] );
    }
 
    $url = '';
    if ( !empty( $parts['scheme'] ) )
        $url .= $parts['scheme'] . ':';
    if ( isset( $parts['host'] ) )
    {
        $url .= '//';
        if ( isset( $parts['user'] ) )
        {
            $url .= $parts['user'];
            if ( isset( $parts['pass'] ) )
                $url .= ':' . $parts['pass'];
            $url .= '@';
        }
        if ( preg_match( '!^[\da-f]*:[\da-f.:]+$!ui', $parts['host'] ) )
            $url .= '[' . $parts['host'] . ']'; // IPv6
        else
            $url .= $parts['host'];             // IPv4 or name
        if ( isset( $parts['port'] ) )
            $url .= ':' . $parts['port'];
        if ( !empty( $parts['path'] ) && $parts['path'][0] != '/' )
            $url .= '/';
    }
    if ( !empty( $parts['path'] ) )
        $url .= $parts['path'];
    if ( isset( $parts['query'] ) )
        $url .= '?' . $parts['query'];
    if ( isset( $parts['fragment'] ) )
        $url .= '#' . $parts['fragment'];
    return $url;
}

function url_remove_dot_segments( $path )
{
    // multi-byte character explode
    $inSegs  = preg_split( '!/!u', $path );
    $outSegs = array( );
    foreach ( $inSegs as $seg )
    {
        if ( $seg == '' || $seg == '.')
            continue;
        if ( $seg == '..' )
            array_pop( $outSegs );
        else
            array_push( $outSegs, $seg );
    }
    $outPath = implode( '/', $outSegs );
    if ( $path[0] == '/' )
        $outPath = '/' . $outPath;
    // compare last multi-byte character against '/'
    if ( $outPath != '/' &&
        (mb_strlen($path)-1) == mb_strrpos( $path, '/', 'UTF-8' ) )
        $outPath .= '/';
    return $outPath;
}

?><?php 
require 'scraperwiki/simple_html_dom.php';

$location = "http://www.bertelsmann-stiftung.de/cps/rde/xchg/bst/hs.xsl/index.html";
/*
scraperwiki::sqliteexecute("create table if not exists pages (`url` string, `processed` int)");
scraperwiki::sqlitecommit();
*/
// initial call -> pages table is empty or has no entries with processed = 0
$waiting = scraperwiki::select("count(*) as c from pages where processed=0");
$waiting = $waiting[0]['c'];
if ($waiting == 0) {
    print "initial call - starting with url " . $location . "\n";
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 0), "pages", 0);
    $waiting = 1;
}
/*
scraperwiki::sqliteexecute("delete from pages where url like '%mpeg'");            
scraperwiki::sqlitecommit();
*/

$processed = scraperwiki::select("count(*) as c from pages where processed=1");
$processed = $processed[0]['c'];

while ($waiting > 0) {
    $externals = scraperwiki::select("count(*) as c from swdata where type like 'external'");
    $externals = $externals[0]['c'];

    print "pages waiting: " . $waiting . " | pages processed: " . $processed . " | external links found: " . $externals . "\n";
    $location = scraperwiki::select("url from pages where processed=0 limit 0,1");
    $location = $location[0]['url'];
    
    findLinksOnPage($location);
    
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 1), "pages", 0);
    
    $waiting = scraperwiki::select("count(*) as c from pages where processed=0");
    $waiting = $waiting[0]['c'];
    
    $processed = scraperwiki::select("count(*) as c from pages  where processed=1");
    $processed = $processed[0]['c'];
}

function findLinksOnPage($location) {
    print "loading page " . $location . "\n";
    $html = scraperWiki::scrape($location);           
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("a") as $anchor){
        $href = $anchor->getAttribute('href');
        $href = preg_replace("/SID-[0-9a-fA-F]+\-[0-9a-fA-F]+\//i", "", $href);
        $type = "";
        if (preg_match("/(http|https|ftp):\/\/([\w-\d]+\.)+[\w-\d]+/i", $href, $m)) {
            if ("bertelsmann-stiftung." == $m[2]) 
                $type = 'internal';
            else
                $type = 'external';
        } else if (preg_match("/(\/[\w~,;\-\.\/?%&+#=]*)/i", $href)) {
            $type = 'internal';
            $href = url_to_absolute($location, $href);
        } else {
            $type = 'unknown';
        }
        scraperwiki::save(array('href'), array('on_page' => $location, 'href' => $href, 'type' => $type, 'exported' => 0));
        
        // remember to follow an internal link, if not already done
        if ($type == 'internal') {
            if (!preg_match("/.*\.mpeg$/i", $href) && !preg_match("/.*\.exe$/i", $href) && !preg_match("/.*\.pdf$/i", $href) && !preg_match("/.*\.mp3$/i", $href) && !preg_match("/.*\.jpg$/i", $href) && !preg_match("/.*\.zip$/i", $href) && !preg_match("/.*\.doc$/i", $href) && !preg_match("/.*\.ppt$/i", $href)) {
                $count = scraperwiki::select("count(*) as c from pages where url like '" . ($href) . "'");
                $count = $count[0]['c'];
                if ($count > 0) {
                    //print "page already processed (or reserved): " . $href . "\n";
                } else {
                    scraperwiki::save_sqlite(array('url'), array('url' => ($href), 'processed' => 0), "pages", 0);
                }
            }
        }
    }
}

function url_to_absolute( $baseUrl, $relativeUrl )
{
    // If relative URL has a scheme, clean path and return.
    $r = split_url( $relativeUrl );
    if ( $r === FALSE )
        return FALSE;
    if ( !empty( $r['scheme'] ) )
    {
        if ( !empty( $r['path'] ) && $r['path'][0] == '/' )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
 
    // Make sure the base URL is absolute.
    $b = split_url( $baseUrl );
    if ( $b === FALSE || empty( $b['scheme'] ) || empty( $b['host'] ) )
        return FALSE;
    $r['scheme'] = $b['scheme'];
 
    // If relative URL has an authority, clean path and return.
    if ( isset( $r['host'] ) )
    {
        if ( !empty( $r['path'] ) )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
    unset( $r['port'] );
    unset( $r['user'] );
    unset( $r['pass'] );
 
    // Copy base authority.
    $r['host'] = $b['host'];
    if ( isset( $b['port'] ) ) $r['port'] = $b['port'];
    if ( isset( $b['user'] ) ) $r['user'] = $b['user'];
    if ( isset( $b['pass'] ) ) $r['pass'] = $b['pass'];
 
    // If relative URL has no path, use base path
    if ( empty( $r['path'] ) )
    {
        if ( !empty( $b['path'] ) )
            $r['path'] = $b['path'];
        if ( !isset( $r['query'] ) && isset( $b['query'] ) )
            $r['query'] = $b['query'];
        return join_url( $r );
    }
 
    // If relative URL path doesn't start with /, merge with base path
    if ( $r['path'][0] != '/' )
    {
        $base = mb_strrchr( $b['path'], '/', TRUE, 'UTF-8' );
        if ( $base === FALSE ) $base = '';
        $r['path'] = $base . '/' . $r['path'];
    }
    $r['path'] = url_remove_dot_segments( $r['path'] );
    return join_url( $r );
}

function split_url( $url, $decode=TRUE )
{
    $xunressub     = 'a-zA-Z\d\-._~\!$&\'()*+,;=';
    $xpchar        = $xunressub . ':@%';

    $xscheme       = '([a-zA-Z][a-zA-Z\d+-.]*)';

    $xuserinfo     = '((['  . $xunressub . '%]*)' .
                     '(:([' . $xunressub . ':%]*))?)';

    $xipv4         = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})';

    $xipv6         = '(\[([a-fA-F\d.:]+)\])';

    $xhost_name    = '([a-zA-Z\d-.%]+)';

    $xhost         = '(' . $xhost_name . '|' . $xipv4 . '|' . $xipv6 . ')';
    $xport         = '(\d*)';
    $xauthority    = '((' . $xuserinfo . '@)?' . $xhost .
                     '?(:' . $xport . ')?)';

    $xslash_seg    = '(/[' . $xpchar . ']*)';
    $xpath_authabs = '((//' . $xauthority . ')((/[' . $xpchar . ']*)*))';
    $xpath_rel     = '([' . $xpchar . ']+' . $xslash_seg . '*)';
    $xpath_abs     = '(/(' . $xpath_rel . ')?)';
    $xapath        = '(' . $xpath_authabs . '|' . $xpath_abs .
                     '|' . $xpath_rel . ')';

    $xqueryfrag    = '([' . $xpchar . '/?' . ']*)';

    $xurl          = '^(' . $xscheme . ':)?' .  $xapath . '?' .
                     '(\?' . $xqueryfrag . ')?(#' . $xqueryfrag . ')?$';
 
 
    // Split the URL into components.
    if ( !preg_match( '!' . $xurl . '!', $url, $m ) )
        return FALSE;
 
    if ( !empty($m[2]) )        $parts['scheme']  = strtolower($m[2]);
 
    if ( !empty($m[7]) ) {
        if ( isset( $m[9] ) )   $parts['user']    = $m[9];
        else            $parts['user']    = '';
    }
    if ( !empty($m[10]) )       $parts['pass']    = $m[11];
 
    if ( !empty($m[13]) )       $h=$parts['host'] = $m[13];
    else if ( !empty($m[14]) )  $parts['host']    = $m[14];
    else if ( !empty($m[16]) )  $parts['host']    = $m[16];
    else if ( !empty( $m[5] ) ) $parts['host']    = '';
    if ( !empty($m[17]) )       $parts['port']    = $m[18];
 
    if ( !empty($m[19]) )       $parts['path']    = $m[19];
    else if ( !empty($m[21]) )  $parts['path']    = $m[21];
    else if ( !empty($m[25]) )  $parts['path']    = $m[25];
 
    if ( !empty($m[27]) )       $parts['query']   = $m[28];
    if ( !empty($m[29]) )       $parts['fragment']= $m[30];
 
    if ( !$decode )
        return $parts;
    if ( !empty($parts['user']) )
        $parts['user']     = rawurldecode( $parts['user'] );
    if ( !empty($parts['pass']) )
        $parts['pass']     = rawurldecode( $parts['pass'] );
    if ( !empty($parts['path']) )
        $parts['path']     = rawurldecode( $parts['path'] );
    if ( isset($h) )
        $parts['host']     = rawurldecode( $parts['host'] );
    if ( !empty($parts['query']) )
        $parts['query']    = rawurldecode( $parts['query'] );
    if ( !empty($parts['fragment']) )
        $parts['fragment'] = rawurldecode( $parts['fragment'] );
    return $parts;
}

function join_url( $parts, $encode=TRUE )
{
    if ( $encode )
    {
        if ( isset( $parts['user'] ) )
            $parts['user']     = rawurlencode( $parts['user'] );
        if ( isset( $parts['pass'] ) )
            $parts['pass']     = rawurlencode( $parts['pass'] );
        if ( isset( $parts['host'] ) &&
            !preg_match( '!^(\[[\da-f.:]+\]])|([\da-f.:]+)$!ui', $parts['host'] ) )
            $parts['host']     = rawurlencode( $parts['host'] );
        if ( !empty( $parts['path'] ) )
            $parts['path']     = preg_replace( '!%2F!ui', '/',
                rawurlencode( $parts['path'] ) );
        if ( isset( $parts['query'] ) )
            $parts['query']    = rawurlencode( $parts['query'] );
        if ( isset( $parts['fragment'] ) )
            $parts['fragment'] = rawurlencode( $parts['fragment'] );
    }
 
    $url = '';
    if ( !empty( $parts['scheme'] ) )
        $url .= $parts['scheme'] . ':';
    if ( isset( $parts['host'] ) )
    {
        $url .= '//';
        if ( isset( $parts['user'] ) )
        {
            $url .= $parts['user'];
            if ( isset( $parts['pass'] ) )
                $url .= ':' . $parts['pass'];
            $url .= '@';
        }
        if ( preg_match( '!^[\da-f]*:[\da-f.:]+$!ui', $parts['host'] ) )
            $url .= '[' . $parts['host'] . ']'; // IPv6
        else
            $url .= $parts['host'];             // IPv4 or name
        if ( isset( $parts['port'] ) )
            $url .= ':' . $parts['port'];
        if ( !empty( $parts['path'] ) && $parts['path'][0] != '/' )
            $url .= '/';
    }
    if ( !empty( $parts['path'] ) )
        $url .= $parts['path'];
    if ( isset( $parts['query'] ) )
        $url .= '?' . $parts['query'];
    if ( isset( $parts['fragment'] ) )
        $url .= '#' . $parts['fragment'];
    return $url;
}

function url_remove_dot_segments( $path )
{
    // multi-byte character explode
    $inSegs  = preg_split( '!/!u', $path );
    $outSegs = array( );
    foreach ( $inSegs as $seg )
    {
        if ( $seg == '' || $seg == '.')
            continue;
        if ( $seg == '..' )
            array_pop( $outSegs );
        else
            array_push( $outSegs, $seg );
    }
    $outPath = implode( '/', $outSegs );
    if ( $path[0] == '/' )
        $outPath = '/' . $outPath;
    // compare last multi-byte character against '/'
    if ( $outPath != '/' &&
        (mb_strlen($path)-1) == mb_strrpos( $path, '/', 'UTF-8' ) )
        $outPath .= '/';
    return $outPath;
}

?><?php 
require 'scraperwiki/simple_html_dom.php';

$location = "http://www.bertelsmann-stiftung.de/cps/rde/xchg/bst/hs.xsl/index.html";
/*
scraperwiki::sqliteexecute("create table if not exists pages (`url` string, `processed` int)");
scraperwiki::sqlitecommit();
*/
// initial call -> pages table is empty or has no entries with processed = 0
$waiting = scraperwiki::select("count(*) as c from pages where processed=0");
$waiting = $waiting[0]['c'];
if ($waiting == 0) {
    print "initial call - starting with url " . $location . "\n";
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 0), "pages", 0);
    $waiting = 1;
}
/*
scraperwiki::sqliteexecute("delete from pages where url like '%mpeg'");            
scraperwiki::sqlitecommit();
*/

$processed = scraperwiki::select("count(*) as c from pages where processed=1");
$processed = $processed[0]['c'];

while ($waiting > 0) {
    $externals = scraperwiki::select("count(*) as c from swdata where type like 'external'");
    $externals = $externals[0]['c'];

    print "pages waiting: " . $waiting . " | pages processed: " . $processed . " | external links found: " . $externals . "\n";
    $location = scraperwiki::select("url from pages where processed=0 limit 0,1");
    $location = $location[0]['url'];
    
    findLinksOnPage($location);
    
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 1), "pages", 0);
    
    $waiting = scraperwiki::select("count(*) as c from pages where processed=0");
    $waiting = $waiting[0]['c'];
    
    $processed = scraperwiki::select("count(*) as c from pages  where processed=1");
    $processed = $processed[0]['c'];
}

function findLinksOnPage($location) {
    print "loading page " . $location . "\n";
    $html = scraperWiki::scrape($location);           
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("a") as $anchor){
        $href = $anchor->getAttribute('href');
        $href = preg_replace("/SID-[0-9a-fA-F]+\-[0-9a-fA-F]+\//i", "", $href);
        $type = "";
        if (preg_match("/(http|https|ftp):\/\/([\w-\d]+\.)+[\w-\d]+/i", $href, $m)) {
            if ("bertelsmann-stiftung." == $m[2]) 
                $type = 'internal';
            else
                $type = 'external';
        } else if (preg_match("/(\/[\w~,;\-\.\/?%&+#=]*)/i", $href)) {
            $type = 'internal';
            $href = url_to_absolute($location, $href);
        } else {
            $type = 'unknown';
        }
        scraperwiki::save(array('href'), array('on_page' => $location, 'href' => $href, 'type' => $type, 'exported' => 0));
        
        // remember to follow an internal link, if not already done
        if ($type == 'internal') {
            if (!preg_match("/.*\.mpeg$/i", $href) && !preg_match("/.*\.exe$/i", $href) && !preg_match("/.*\.pdf$/i", $href) && !preg_match("/.*\.mp3$/i", $href) && !preg_match("/.*\.jpg$/i", $href) && !preg_match("/.*\.zip$/i", $href) && !preg_match("/.*\.doc$/i", $href) && !preg_match("/.*\.ppt$/i", $href)) {
                $count = scraperwiki::select("count(*) as c from pages where url like '" . ($href) . "'");
                $count = $count[0]['c'];
                if ($count > 0) {
                    //print "page already processed (or reserved): " . $href . "\n";
                } else {
                    scraperwiki::save_sqlite(array('url'), array('url' => ($href), 'processed' => 0), "pages", 0);
                }
            }
        }
    }
}

function url_to_absolute( $baseUrl, $relativeUrl )
{
    // If relative URL has a scheme, clean path and return.
    $r = split_url( $relativeUrl );
    if ( $r === FALSE )
        return FALSE;
    if ( !empty( $r['scheme'] ) )
    {
        if ( !empty( $r['path'] ) && $r['path'][0] == '/' )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
 
    // Make sure the base URL is absolute.
    $b = split_url( $baseUrl );
    if ( $b === FALSE || empty( $b['scheme'] ) || empty( $b['host'] ) )
        return FALSE;
    $r['scheme'] = $b['scheme'];
 
    // If relative URL has an authority, clean path and return.
    if ( isset( $r['host'] ) )
    {
        if ( !empty( $r['path'] ) )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
    unset( $r['port'] );
    unset( $r['user'] );
    unset( $r['pass'] );
 
    // Copy base authority.
    $r['host'] = $b['host'];
    if ( isset( $b['port'] ) ) $r['port'] = $b['port'];
    if ( isset( $b['user'] ) ) $r['user'] = $b['user'];
    if ( isset( $b['pass'] ) ) $r['pass'] = $b['pass'];
 
    // If relative URL has no path, use base path
    if ( empty( $r['path'] ) )
    {
        if ( !empty( $b['path'] ) )
            $r['path'] = $b['path'];
        if ( !isset( $r['query'] ) && isset( $b['query'] ) )
            $r['query'] = $b['query'];
        return join_url( $r );
    }
 
    // If relative URL path doesn't start with /, merge with base path
    if ( $r['path'][0] != '/' )
    {
        $base = mb_strrchr( $b['path'], '/', TRUE, 'UTF-8' );
        if ( $base === FALSE ) $base = '';
        $r['path'] = $base . '/' . $r['path'];
    }
    $r['path'] = url_remove_dot_segments( $r['path'] );
    return join_url( $r );
}

function split_url( $url, $decode=TRUE )
{
    $xunressub     = 'a-zA-Z\d\-._~\!$&\'()*+,;=';
    $xpchar        = $xunressub . ':@%';

    $xscheme       = '([a-zA-Z][a-zA-Z\d+-.]*)';

    $xuserinfo     = '((['  . $xunressub . '%]*)' .
                     '(:([' . $xunressub . ':%]*))?)';

    $xipv4         = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})';

    $xipv6         = '(\[([a-fA-F\d.:]+)\])';

    $xhost_name    = '([a-zA-Z\d-.%]+)';

    $xhost         = '(' . $xhost_name . '|' . $xipv4 . '|' . $xipv6 . ')';
    $xport         = '(\d*)';
    $xauthority    = '((' . $xuserinfo . '@)?' . $xhost .
                     '?(:' . $xport . ')?)';

    $xslash_seg    = '(/[' . $xpchar . ']*)';
    $xpath_authabs = '((//' . $xauthority . ')((/[' . $xpchar . ']*)*))';
    $xpath_rel     = '([' . $xpchar . ']+' . $xslash_seg . '*)';
    $xpath_abs     = '(/(' . $xpath_rel . ')?)';
    $xapath        = '(' . $xpath_authabs . '|' . $xpath_abs .
                     '|' . $xpath_rel . ')';

    $xqueryfrag    = '([' . $xpchar . '/?' . ']*)';

    $xurl          = '^(' . $xscheme . ':)?' .  $xapath . '?' .
                     '(\?' . $xqueryfrag . ')?(#' . $xqueryfrag . ')?$';
 
 
    // Split the URL into components.
    if ( !preg_match( '!' . $xurl . '!', $url, $m ) )
        return FALSE;
 
    if ( !empty($m[2]) )        $parts['scheme']  = strtolower($m[2]);
 
    if ( !empty($m[7]) ) {
        if ( isset( $m[9] ) )   $parts['user']    = $m[9];
        else            $parts['user']    = '';
    }
    if ( !empty($m[10]) )       $parts['pass']    = $m[11];
 
    if ( !empty($m[13]) )       $h=$parts['host'] = $m[13];
    else if ( !empty($m[14]) )  $parts['host']    = $m[14];
    else if ( !empty($m[16]) )  $parts['host']    = $m[16];
    else if ( !empty( $m[5] ) ) $parts['host']    = '';
    if ( !empty($m[17]) )       $parts['port']    = $m[18];
 
    if ( !empty($m[19]) )       $parts['path']    = $m[19];
    else if ( !empty($m[21]) )  $parts['path']    = $m[21];
    else if ( !empty($m[25]) )  $parts['path']    = $m[25];
 
    if ( !empty($m[27]) )       $parts['query']   = $m[28];
    if ( !empty($m[29]) )       $parts['fragment']= $m[30];
 
    if ( !$decode )
        return $parts;
    if ( !empty($parts['user']) )
        $parts['user']     = rawurldecode( $parts['user'] );
    if ( !empty($parts['pass']) )
        $parts['pass']     = rawurldecode( $parts['pass'] );
    if ( !empty($parts['path']) )
        $parts['path']     = rawurldecode( $parts['path'] );
    if ( isset($h) )
        $parts['host']     = rawurldecode( $parts['host'] );
    if ( !empty($parts['query']) )
        $parts['query']    = rawurldecode( $parts['query'] );
    if ( !empty($parts['fragment']) )
        $parts['fragment'] = rawurldecode( $parts['fragment'] );
    return $parts;
}

function join_url( $parts, $encode=TRUE )
{
    if ( $encode )
    {
        if ( isset( $parts['user'] ) )
            $parts['user']     = rawurlencode( $parts['user'] );
        if ( isset( $parts['pass'] ) )
            $parts['pass']     = rawurlencode( $parts['pass'] );
        if ( isset( $parts['host'] ) &&
            !preg_match( '!^(\[[\da-f.:]+\]])|([\da-f.:]+)$!ui', $parts['host'] ) )
            $parts['host']     = rawurlencode( $parts['host'] );
        if ( !empty( $parts['path'] ) )
            $parts['path']     = preg_replace( '!%2F!ui', '/',
                rawurlencode( $parts['path'] ) );
        if ( isset( $parts['query'] ) )
            $parts['query']    = rawurlencode( $parts['query'] );
        if ( isset( $parts['fragment'] ) )
            $parts['fragment'] = rawurlencode( $parts['fragment'] );
    }
 
    $url = '';
    if ( !empty( $parts['scheme'] ) )
        $url .= $parts['scheme'] . ':';
    if ( isset( $parts['host'] ) )
    {
        $url .= '//';
        if ( isset( $parts['user'] ) )
        {
            $url .= $parts['user'];
            if ( isset( $parts['pass'] ) )
                $url .= ':' . $parts['pass'];
            $url .= '@';
        }
        if ( preg_match( '!^[\da-f]*:[\da-f.:]+$!ui', $parts['host'] ) )
            $url .= '[' . $parts['host'] . ']'; // IPv6
        else
            $url .= $parts['host'];             // IPv4 or name
        if ( isset( $parts['port'] ) )
            $url .= ':' . $parts['port'];
        if ( !empty( $parts['path'] ) && $parts['path'][0] != '/' )
            $url .= '/';
    }
    if ( !empty( $parts['path'] ) )
        $url .= $parts['path'];
    if ( isset( $parts['query'] ) )
        $url .= '?' . $parts['query'];
    if ( isset( $parts['fragment'] ) )
        $url .= '#' . $parts['fragment'];
    return $url;
}

function url_remove_dot_segments( $path )
{
    // multi-byte character explode
    $inSegs  = preg_split( '!/!u', $path );
    $outSegs = array( );
    foreach ( $inSegs as $seg )
    {
        if ( $seg == '' || $seg == '.')
            continue;
        if ( $seg == '..' )
            array_pop( $outSegs );
        else
            array_push( $outSegs, $seg );
    }
    $outPath = implode( '/', $outSegs );
    if ( $path[0] == '/' )
        $outPath = '/' . $outPath;
    // compare last multi-byte character against '/'
    if ( $outPath != '/' &&
        (mb_strlen($path)-1) == mb_strrpos( $path, '/', 'UTF-8' ) )
        $outPath .= '/';
    return $outPath;
}

?><?php 
require 'scraperwiki/simple_html_dom.php';

$location = "http://www.bertelsmann-stiftung.de/cps/rde/xchg/bst/hs.xsl/index.html";
/*
scraperwiki::sqliteexecute("create table if not exists pages (`url` string, `processed` int)");
scraperwiki::sqlitecommit();
*/
// initial call -> pages table is empty or has no entries with processed = 0
$waiting = scraperwiki::select("count(*) as c from pages where processed=0");
$waiting = $waiting[0]['c'];
if ($waiting == 0) {
    print "initial call - starting with url " . $location . "\n";
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 0), "pages", 0);
    $waiting = 1;
}
/*
scraperwiki::sqliteexecute("delete from pages where url like '%mpeg'");            
scraperwiki::sqlitecommit();
*/

$processed = scraperwiki::select("count(*) as c from pages where processed=1");
$processed = $processed[0]['c'];

while ($waiting > 0) {
    $externals = scraperwiki::select("count(*) as c from swdata where type like 'external'");
    $externals = $externals[0]['c'];

    print "pages waiting: " . $waiting . " | pages processed: " . $processed . " | external links found: " . $externals . "\n";
    $location = scraperwiki::select("url from pages where processed=0 limit 0,1");
    $location = $location[0]['url'];
    
    findLinksOnPage($location);
    
    scraperwiki::save_sqlite(array('url'), array('url' => ($location), 'processed' => 1), "pages", 0);
    
    $waiting = scraperwiki::select("count(*) as c from pages where processed=0");
    $waiting = $waiting[0]['c'];
    
    $processed = scraperwiki::select("count(*) as c from pages  where processed=1");
    $processed = $processed[0]['c'];
}

function findLinksOnPage($location) {
    print "loading page " . $location . "\n";
    $html = scraperWiki::scrape($location);           
    
    $dom = new simple_html_dom();
    $dom->load($html);
    
    foreach($dom->find("a") as $anchor){
        $href = $anchor->getAttribute('href');
        $href = preg_replace("/SID-[0-9a-fA-F]+\-[0-9a-fA-F]+\//i", "", $href);
        $type = "";
        if (preg_match("/(http|https|ftp):\/\/([\w-\d]+\.)+[\w-\d]+/i", $href, $m)) {
            if ("bertelsmann-stiftung." == $m[2]) 
                $type = 'internal';
            else
                $type = 'external';
        } else if (preg_match("/(\/[\w~,;\-\.\/?%&+#=]*)/i", $href)) {
            $type = 'internal';
            $href = url_to_absolute($location, $href);
        } else {
            $type = 'unknown';
        }
        scraperwiki::save(array('href'), array('on_page' => $location, 'href' => $href, 'type' => $type, 'exported' => 0));
        
        // remember to follow an internal link, if not already done
        if ($type == 'internal') {
            if (!preg_match("/.*\.mpeg$/i", $href) && !preg_match("/.*\.exe$/i", $href) && !preg_match("/.*\.pdf$/i", $href) && !preg_match("/.*\.mp3$/i", $href) && !preg_match("/.*\.jpg$/i", $href) && !preg_match("/.*\.zip$/i", $href) && !preg_match("/.*\.doc$/i", $href) && !preg_match("/.*\.ppt$/i", $href)) {
                $count = scraperwiki::select("count(*) as c from pages where url like '" . ($href) . "'");
                $count = $count[0]['c'];
                if ($count > 0) {
                    //print "page already processed (or reserved): " . $href . "\n";
                } else {
                    scraperwiki::save_sqlite(array('url'), array('url' => ($href), 'processed' => 0), "pages", 0);
                }
            }
        }
    }
}

function url_to_absolute( $baseUrl, $relativeUrl )
{
    // If relative URL has a scheme, clean path and return.
    $r = split_url( $relativeUrl );
    if ( $r === FALSE )
        return FALSE;
    if ( !empty( $r['scheme'] ) )
    {
        if ( !empty( $r['path'] ) && $r['path'][0] == '/' )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
 
    // Make sure the base URL is absolute.
    $b = split_url( $baseUrl );
    if ( $b === FALSE || empty( $b['scheme'] ) || empty( $b['host'] ) )
        return FALSE;
    $r['scheme'] = $b['scheme'];
 
    // If relative URL has an authority, clean path and return.
    if ( isset( $r['host'] ) )
    {
        if ( !empty( $r['path'] ) )
            $r['path'] = url_remove_dot_segments( $r['path'] );
        return join_url( $r );
    }
    unset( $r['port'] );
    unset( $r['user'] );
    unset( $r['pass'] );
 
    // Copy base authority.
    $r['host'] = $b['host'];
    if ( isset( $b['port'] ) ) $r['port'] = $b['port'];
    if ( isset( $b['user'] ) ) $r['user'] = $b['user'];
    if ( isset( $b['pass'] ) ) $r['pass'] = $b['pass'];
 
    // If relative URL has no path, use base path
    if ( empty( $r['path'] ) )
    {
        if ( !empty( $b['path'] ) )
            $r['path'] = $b['path'];
        if ( !isset( $r['query'] ) && isset( $b['query'] ) )
            $r['query'] = $b['query'];
        return join_url( $r );
    }
 
    // If relative URL path doesn't start with /, merge with base path
    if ( $r['path'][0] != '/' )
    {
        $base = mb_strrchr( $b['path'], '/', TRUE, 'UTF-8' );
        if ( $base === FALSE ) $base = '';
        $r['path'] = $base . '/' . $r['path'];
    }
    $r['path'] = url_remove_dot_segments( $r['path'] );
    return join_url( $r );
}

function split_url( $url, $decode=TRUE )
{
    $xunressub     = 'a-zA-Z\d\-._~\!$&\'()*+,;=';
    $xpchar        = $xunressub . ':@%';

    $xscheme       = '([a-zA-Z][a-zA-Z\d+-.]*)';

    $xuserinfo     = '((['  . $xunressub . '%]*)' .
                     '(:([' . $xunressub . ':%]*))?)';

    $xipv4         = '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})';

    $xipv6         = '(\[([a-fA-F\d.:]+)\])';

    $xhost_name    = '([a-zA-Z\d-.%]+)';

    $xhost         = '(' . $xhost_name . '|' . $xipv4 . '|' . $xipv6 . ')';
    $xport         = '(\d*)';
    $xauthority    = '((' . $xuserinfo . '@)?' . $xhost .
                     '?(:' . $xport . ')?)';

    $xslash_seg    = '(/[' . $xpchar . ']*)';
    $xpath_authabs = '((//' . $xauthority . ')((/[' . $xpchar . ']*)*))';
    $xpath_rel     = '([' . $xpchar . ']+' . $xslash_seg . '*)';
    $xpath_abs     = '(/(' . $xpath_rel . ')?)';
    $xapath        = '(' . $xpath_authabs . '|' . $xpath_abs .
                     '|' . $xpath_rel . ')';

    $xqueryfrag    = '([' . $xpchar . '/?' . ']*)';

    $xurl          = '^(' . $xscheme . ':)?' .  $xapath . '?' .
                     '(\?' . $xqueryfrag . ')?(#' . $xqueryfrag . ')?$';
 
 
    // Split the URL into components.
    if ( !preg_match( '!' . $xurl . '!', $url, $m ) )
        return FALSE;
 
    if ( !empty($m[2]) )        $parts['scheme']  = strtolower($m[2]);
 
    if ( !empty($m[7]) ) {
        if ( isset( $m[9] ) )   $parts['user']    = $m[9];
        else            $parts['user']    = '';
    }
    if ( !empty($m[10]) )       $parts['pass']    = $m[11];
 
    if ( !empty($m[13]) )       $h=$parts['host'] = $m[13];
    else if ( !empty($m[14]) )  $parts['host']    = $m[14];
    else if ( !empty($m[16]) )  $parts['host']    = $m[16];
    else if ( !empty( $m[5] ) ) $parts['host']    = '';
    if ( !empty($m[17]) )       $parts['port']    = $m[18];
 
    if ( !empty($m[19]) )       $parts['path']    = $m[19];
    else if ( !empty($m[21]) )  $parts['path']    = $m[21];
    else if ( !empty($m[25]) )  $parts['path']    = $m[25];
 
    if ( !empty($m[27]) )       $parts['query']   = $m[28];
    if ( !empty($m[29]) )       $parts['fragment']= $m[30];
 
    if ( !$decode )
        return $parts;
    if ( !empty($parts['user']) )
        $parts['user']     = rawurldecode( $parts['user'] );
    if ( !empty($parts['pass']) )
        $parts['pass']     = rawurldecode( $parts['pass'] );
    if ( !empty($parts['path']) )
        $parts['path']     = rawurldecode( $parts['path'] );
    if ( isset($h) )
        $parts['host']     = rawurldecode( $parts['host'] );
    if ( !empty($parts['query']) )
        $parts['query']    = rawurldecode( $parts['query'] );
    if ( !empty($parts['fragment']) )
        $parts['fragment'] = rawurldecode( $parts['fragment'] );
    return $parts;
}

function join_url( $parts, $encode=TRUE )
{
    if ( $encode )
    {
        if ( isset( $parts['user'] ) )
            $parts['user']     = rawurlencode( $parts['user'] );
        if ( isset( $parts['pass'] ) )
            $parts['pass']     = rawurlencode( $parts['pass'] );
        if ( isset( $parts['host'] ) &&
            !preg_match( '!^(\[[\da-f.:]+\]])|([\da-f.:]+)$!ui', $parts['host'] ) )
            $parts['host']     = rawurlencode( $parts['host'] );
        if ( !empty( $parts['path'] ) )
            $parts['path']     = preg_replace( '!%2F!ui', '/',
                rawurlencode( $parts['path'] ) );
        if ( isset( $parts['query'] ) )
            $parts['query']    = rawurlencode( $parts['query'] );
        if ( isset( $parts['fragment'] ) )
            $parts['fragment'] = rawurlencode( $parts['fragment'] );
    }
 
    $url = '';
    if ( !empty( $parts['scheme'] ) )
        $url .= $parts['scheme'] . ':';
    if ( isset( $parts['host'] ) )
    {
        $url .= '//';
        if ( isset( $parts['user'] ) )
        {
            $url .= $parts['user'];
            if ( isset( $parts['pass'] ) )
                $url .= ':' . $parts['pass'];
            $url .= '@';
        }
        if ( preg_match( '!^[\da-f]*:[\da-f.:]+$!ui', $parts['host'] ) )
            $url .= '[' . $parts['host'] . ']'; // IPv6
        else
            $url .= $parts['host'];             // IPv4 or name
        if ( isset( $parts['port'] ) )
            $url .= ':' . $parts['port'];
        if ( !empty( $parts['path'] ) && $parts['path'][0] != '/' )
            $url .= '/';
    }
    if ( !empty( $parts['path'] ) )
        $url .= $parts['path'];
    if ( isset( $parts['query'] ) )
        $url .= '?' . $parts['query'];
    if ( isset( $parts['fragment'] ) )
        $url .= '#' . $parts['fragment'];
    return $url;
}

function url_remove_dot_segments( $path )
{
    // multi-byte character explode
    $inSegs  = preg_split( '!/!u', $path );
    $outSegs = array( );
    foreach ( $inSegs as $seg )
    {
        if ( $seg == '' || $seg == '.')
            continue;
        if ( $seg == '..' )
            array_pop( $outSegs );
        else
            array_push( $outSegs, $seg );
    }
    $outPath = implode( '/', $outSegs );
    if ( $path[0] == '/' )
        $outPath = '/' . $outPath;
    // compare last multi-byte character against '/'
    if ( $outPath != '/' &&
        (mb_strlen($path)-1) == mb_strrpos( $path, '/', 'UTF-8' ) )
        $outPath .= '/';
    return $outPath;
}

?>