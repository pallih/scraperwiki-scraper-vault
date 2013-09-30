<?php

// JUST AN EXPERIMENT, JUST A BEGINNING
// Connected to https://github.com/okfn/publicbodies

define('BASE_URL', 'http://www.staatskalender.admin.ch/');

require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('UTC');
scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS swdata (created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)');

// First level of hierarchy
foreach (getHTML(BASE_URL . 'welcome.html')->find('a.navLevel2') as $el) {   
    
    $entity = array(
        'title' => $el->title,
        'source_url' => BASE_URL . str_replace(' ', '+', $el->href)
    );

    create($entity);   
}

// Get children of an entity
function getChildren($parent, $html) {
    foreach($html->find('div.infoblock a[href^=navigate.html?dn=]') as $childLink) {

        $childEntity = array(
            'title' => $parent['title'] . ' - ' . trim($childLink->innertext),
            'source_url' => BASE_URL . str_replace(' ', '+', $childLink->href),
            'parent_key' => $parent['key']
        );

        create($childEntity);
    }
}

// Get details of an entity
function create($entity) {
    $html = getHTML($entity['source_url']);

    if(!$html) {
        return error_log('Could not import ' + $entity['source_url']);
    }

    // Clean title
    $entity['title'] = trim(html_entity_decode($entity['title'], ENT_COMPAT, 'UTF-8'));

    // Generate key
    $entity['key'] = 'ch/' . makeSlug($entity['title']);

    // Extract email 
    $emailLink = $html->find('table.tabelleESK a[href^=mailto:]', 0);
    if($emailLink) {
        $entity['email'] = str_replace('mailto:', '', trim($emailLink->href));
    }
  
    // Extract URL 
    foreach($html->find('table.tabelleESK tr') as $row) {
        $name = trim($row->children(0)->innertext);

        if (stripos('homepage', $name) !== false) {
            foreach($row->children() as $i => $cell) {
                $link = $cell->find('a[href]', 0);
                if ($link) {
                    $entity['url'] = $link->href;
                    break;
                }
                // Ugly case: URL but no link
                if($i && !$cell->children()) {
                    $entity['url'] = $cell->innertext;
                    break; 
                }
            }
        }
    }

    // Find entity abbreviation
    $orgTitle = $html->find('h2.titleOrg', 0);

    if ($orgTitle) {
        $orgTitleParts = explode('-', $orgTitle->innertext);
        if(count($orgTitleParts) > 1) {
            $entity['abbr'] = trim(array_pop($orgTitleParts));
            $entity['abbr'] = html_entity_decode($entity['abbr'], ENT_COMPAT, 'UTF-8');  
        }
    } else {
        error_log('No title on ' + $entity['source_url']);
    }

    // Find entity address
    $infoBlock = $html->find('div.infoblock', 0)->innertext;
    if(preg_match('/<\/h2>(.+?)<div class="titleContent">/s', $infoBlock, $matches)) {
        $infoBlock = str_replace(array('<br>', '(neues Fenster)'), array(', ', ''), $matches[1]);
        $infoBlock = preg_replace('/\s\s+/', ' ', $infoBlock);
        $infoBlock = trim(html_entity_decode(strip_tags($infoBlock), ENT_COMPAT, 'UTF-8'));
        $entity['address'] = $infoBlock;
    }

    save($entity);
    getChildren($entity, $html);
}

// Store an entity
function save($entity) {

    $entity['updated_at'] = date('Y-m-d H:i:s');
    $entity['jurisdiction_code'] = 'CH';
    $entity['jurisdiction'] = 'Switzerland';
    $entity['source'] = 'Eidgenössischer Staatskalender';
    $entity['source_description'] = 'Federal-level entities of the Swiss government';
    $entity['category'] = 'Federal';

    if(!isset($entity['url'])) {
        $entity['url'] = $entity['source_url'];
    }
  
    return @scraperwiki::save_sqlite(array('key'), $entity);
}

// Create an URL-friendly identifier
function makeSlug($str) {
    return 
        preg_replace('/\W+/', '-', 
            strtr(
                strtolower(trim($str)), 
                array('ä' => 'ae', 'ö' => 'oe', 'ü' => 'ue', 'à' => 'a', 'è' => 'e', 'é' => 'e') // no iconv locales on Scraperwiki ..?
            )
        );
}

// Get DOM from URL
function getHTML($url) {
    return str_get_html(scraperwiki::scrape($url));
}

?>
<?php

// JUST AN EXPERIMENT, JUST A BEGINNING
// Connected to https://github.com/okfn/publicbodies

define('BASE_URL', 'http://www.staatskalender.admin.ch/');

require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('UTC');
scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS swdata (created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)');

// First level of hierarchy
foreach (getHTML(BASE_URL . 'welcome.html')->find('a.navLevel2') as $el) {   
    
    $entity = array(
        'title' => $el->title,
        'source_url' => BASE_URL . str_replace(' ', '+', $el->href)
    );

    create($entity);   
}

// Get children of an entity
function getChildren($parent, $html) {
    foreach($html->find('div.infoblock a[href^=navigate.html?dn=]') as $childLink) {

        $childEntity = array(
            'title' => $parent['title'] . ' - ' . trim($childLink->innertext),
            'source_url' => BASE_URL . str_replace(' ', '+', $childLink->href),
            'parent_key' => $parent['key']
        );

        create($childEntity);
    }
}

// Get details of an entity
function create($entity) {
    $html = getHTML($entity['source_url']);

    if(!$html) {
        return error_log('Could not import ' + $entity['source_url']);
    }

    // Clean title
    $entity['title'] = trim(html_entity_decode($entity['title'], ENT_COMPAT, 'UTF-8'));

    // Generate key
    $entity['key'] = 'ch/' . makeSlug($entity['title']);

    // Extract email 
    $emailLink = $html->find('table.tabelleESK a[href^=mailto:]', 0);
    if($emailLink) {
        $entity['email'] = str_replace('mailto:', '', trim($emailLink->href));
    }
  
    // Extract URL 
    foreach($html->find('table.tabelleESK tr') as $row) {
        $name = trim($row->children(0)->innertext);

        if (stripos('homepage', $name) !== false) {
            foreach($row->children() as $i => $cell) {
                $link = $cell->find('a[href]', 0);
                if ($link) {
                    $entity['url'] = $link->href;
                    break;
                }
                // Ugly case: URL but no link
                if($i && !$cell->children()) {
                    $entity['url'] = $cell->innertext;
                    break; 
                }
            }
        }
    }

    // Find entity abbreviation
    $orgTitle = $html->find('h2.titleOrg', 0);

    if ($orgTitle) {
        $orgTitleParts = explode('-', $orgTitle->innertext);
        if(count($orgTitleParts) > 1) {
            $entity['abbr'] = trim(array_pop($orgTitleParts));
            $entity['abbr'] = html_entity_decode($entity['abbr'], ENT_COMPAT, 'UTF-8');  
        }
    } else {
        error_log('No title on ' + $entity['source_url']);
    }

    // Find entity address
    $infoBlock = $html->find('div.infoblock', 0)->innertext;
    if(preg_match('/<\/h2>(.+?)<div class="titleContent">/s', $infoBlock, $matches)) {
        $infoBlock = str_replace(array('<br>', '(neues Fenster)'), array(', ', ''), $matches[1]);
        $infoBlock = preg_replace('/\s\s+/', ' ', $infoBlock);
        $infoBlock = trim(html_entity_decode(strip_tags($infoBlock), ENT_COMPAT, 'UTF-8'));
        $entity['address'] = $infoBlock;
    }

    save($entity);
    getChildren($entity, $html);
}

// Store an entity
function save($entity) {

    $entity['updated_at'] = date('Y-m-d H:i:s');
    $entity['jurisdiction_code'] = 'CH';
    $entity['jurisdiction'] = 'Switzerland';
    $entity['source'] = 'Eidgenössischer Staatskalender';
    $entity['source_description'] = 'Federal-level entities of the Swiss government';
    $entity['category'] = 'Federal';

    if(!isset($entity['url'])) {
        $entity['url'] = $entity['source_url'];
    }
  
    return @scraperwiki::save_sqlite(array('key'), $entity);
}

// Create an URL-friendly identifier
function makeSlug($str) {
    return 
        preg_replace('/\W+/', '-', 
            strtr(
                strtolower(trim($str)), 
                array('ä' => 'ae', 'ö' => 'oe', 'ü' => 'ue', 'à' => 'a', 'è' => 'e', 'é' => 'e') // no iconv locales on Scraperwiki ..?
            )
        );
}

// Get DOM from URL
function getHTML($url) {
    return str_get_html(scraperwiki::scrape($url));
}

?>
