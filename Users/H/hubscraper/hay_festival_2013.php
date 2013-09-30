<?php

$dom = new DOMDocument;
@$dom->loadHTMLFile('http://www.hayfestival.com/archive');

$xpath = new DOMXPath($dom);
$nodes = $xpath->query('//a[text() = "Hay Festival 2013"]'); // TODO: not storing category cookie, so actually fetching everything

if (!$nodes->length) {
    exit("Archive link not found\n");
}

$url = 'http://www.hayfestival.com/' . $nodes->item(0)->getAttribute('href');

do {
    print "$url\n";
    $dom = new DOMDocument;
    @$dom->loadHTMLFile($url);

    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//ul[@class="search-results"]/li');

    if (!$nodes->length) {
        exit("No events found\n");
    }

    foreach ($nodes as $node) {
        $linkNodes = $xpath->query('h3/a', $node);

        if (!$linkNodes->length) {
            continue;
        }

        $link = $linkNodes->item(0);
        $title = $link->parentNode->nextSibling->nextSibling->textContent;
        $description = $xpath->query('div[@class="description"]', $node)->item(0)->textContent;

        $data = array(
            'url' => 'http://www.hayfestival.com/' . $link->getAttribute('href'),
            'speaker' => $link->textContent,
            'title' => ($title !== $description) ? $title : '',
            'description' => $description,
        );

        scraperwiki::save(array('url'), $data);
    }

    $nextNodes = $xpath->query('//div[@class="page-numbers"]/a[@class="PageNumber"][text() = "»"]');

    if (!$nextNodes->length) {
        break;
    }

    $url = 'http://www.hayfestival.com/' . $nextNodes->item(0)->getAttribute('href');
} while ($url);

<?php

$dom = new DOMDocument;
@$dom->loadHTMLFile('http://www.hayfestival.com/archive');

$xpath = new DOMXPath($dom);
$nodes = $xpath->query('//a[text() = "Hay Festival 2013"]'); // TODO: not storing category cookie, so actually fetching everything

if (!$nodes->length) {
    exit("Archive link not found\n");
}

$url = 'http://www.hayfestival.com/' . $nodes->item(0)->getAttribute('href');

do {
    print "$url\n";
    $dom = new DOMDocument;
    @$dom->loadHTMLFile($url);

    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//ul[@class="search-results"]/li');

    if (!$nodes->length) {
        exit("No events found\n");
    }

    foreach ($nodes as $node) {
        $linkNodes = $xpath->query('h3/a', $node);

        if (!$linkNodes->length) {
            continue;
        }

        $link = $linkNodes->item(0);
        $title = $link->parentNode->nextSibling->nextSibling->textContent;
        $description = $xpath->query('div[@class="description"]', $node)->item(0)->textContent;

        $data = array(
            'url' => 'http://www.hayfestival.com/' . $link->getAttribute('href'),
            'speaker' => $link->textContent,
            'title' => ($title !== $description) ? $title : '',
            'description' => $description,
        );

        scraperwiki::save(array('url'), $data);
    }

    $nextNodes = $xpath->query('//div[@class="page-numbers"]/a[@class="PageNumber"][text() = "»"]');

    if (!$nextNodes->length) {
        break;
    }

    $url = 'http://www.hayfestival.com/' . $nextNodes->item(0)->getAttribute('href');
} while ($url);

