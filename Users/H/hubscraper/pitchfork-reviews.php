<?php

$url = sprintf('/reviews/albums/1/');

do {
    $dom = new DOMDocument;
    @$dom->loadHTMLFile('http://pitchfork.com' . $url);

    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//a[starts-with(@href, "/reviews/albums/")]');

    print "{$nodes->length} nodes\n";

    if (!$nodes->length) {
        break;
    }

    foreach ($nodes as $node) {
        $url = $node->getAttribute('href');

        $dateNodes = $xpath->query('div/h4', $node);

        if (!$dateNodes->length) {
            continue;
        }

        $date = $dateNodes->item(0)->textContent;

        preg_match('/(\d+)$/', $date, $matches);
        $year = $matches ? $matches[1] : null;

        $data = array(
            'artist' => $xpath->query('div/h1', $node)->item(0)->textContent,
            'title' => $xpath->query('div/h2', $node)->item(0)->textContent,
            'url' => $url,
            'date' => $date,
            'year' => $year,
        );

        scraperwiki::save(array('url'), $data);
    }

    $nextNodes = $xpath->query('//a[@class="next"][starts-with(@href, "/reviews/albums/")]');

    if (!$nextNodes->length) {
      break;
    }

    $url = $nextNodes->item(0)->getAttribute('href');
} while ($url);
