<?php

foreach (range(1, 10) as $page) {
    $dom = new DOMDocument();
    @$dom->loadHTMLFile('http://www.journaltocs.ac.uk/index.php?action=browse&subAction=pub&local_page=' . $page);
    $xpath = new DOMXPath($dom);
    $nodes = $xpath->query('//div[@id="column1"]//td/a/u');

    if (!$nodes->length) {
        print 'No more publishers found';
        break;
    }

    foreach ($nodes as $node) {
        preg_match('/publisherID=(\d+)/', $node->parentNode->getAttribute('href'), $matches);

        $data = array(
            'id' => $matches[1],
            'name' => $node->textContent,
            'link' => null
        );

        $linkNodes = $xpath->query('a[@target="_blank"]', $node->parentNode->parentNode);
        if ($linkNodes->length) {
            $data['link'] = $linkNodes->item(0)->getAttribute('href');
        }

        scraperwiki::save(array('id'), $data);     
    }
}
