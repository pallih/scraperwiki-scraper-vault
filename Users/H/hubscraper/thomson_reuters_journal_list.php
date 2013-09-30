<?php

function fetch_pages() {
    $dom = new DOMDocument;
    @$dom->loadHTMLFile("http://ip-science.thomsonreuters.com/cgi-bin/jrnlst/jlresults.cgi?FORMATALLFORPRINT.x=1&HIDDENQUERYSTRING=PC%3DMASTER&DISPLAY=QUERY");
    
    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//a');

    $items = array();

    foreach ($nodes as $node) {
        $items[] = 'http://ip-science.thomsonreuters.com/' . $node->getAttribute('href');
    }
    
    return $items;
}

function fetch_page($url) {
    $dom = new DOMDocument;
    @$dom->loadHTMLFile($url);
    
    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//dt');

    $items = array();

    foreach ($nodes as $node) {
        $name = preg_replace('/^\d+\.\s*/', '', trim($node->textContent));
        
        preg_match('/ISSN: (\w{4}-\w{4})/', $node->nextSibling->textContent, $matches);

        if (!$name || !$matches) {
            continue;
        }

        $items[] = array(
            'name' => $name,
            'issn' => $matches[1],
        );
    }

    return $items;
}

$pages = fetch_pages();

foreach ($pages as $page) {
    $items = fetch_page($page);

    foreach ($items as $item) {
        scraperwiki::save_sqlite(array('name'), $item);           
    }
}

<?php

function fetch_pages() {
    $dom = new DOMDocument;
    @$dom->loadHTMLFile("http://ip-science.thomsonreuters.com/cgi-bin/jrnlst/jlresults.cgi?FORMATALLFORPRINT.x=1&HIDDENQUERYSTRING=PC%3DMASTER&DISPLAY=QUERY");
    
    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//a');

    $items = array();

    foreach ($nodes as $node) {
        $items[] = 'http://ip-science.thomsonreuters.com/' . $node->getAttribute('href');
    }
    
    return $items;
}

function fetch_page($url) {
    $dom = new DOMDocument;
    @$dom->loadHTMLFile($url);
    
    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//dt');

    $items = array();

    foreach ($nodes as $node) {
        $name = preg_replace('/^\d+\.\s*/', '', trim($node->textContent));
        
        preg_match('/ISSN: (\w{4}-\w{4})/', $node->nextSibling->textContent, $matches);

        if (!$name || !$matches) {
            continue;
        }

        $items[] = array(
            'name' => $name,
            'issn' => $matches[1],
        );
    }

    return $items;
}

$pages = fetch_pages();

foreach ($pages as $page) {
    $items = fetch_page($page);

    foreach ($items as $item) {
        scraperwiki::save_sqlite(array('name'), $item);           
    }
}

