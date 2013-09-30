<?php

$sourcescraper = 'php_tokens';
scraperwiki::attach($sourcescraper);

$search = (isset($_GET['token']) && preg_match('/^T_[A-Z_]+$/D', $_GET['token'])) ? $_GET['token'] : FALSE;
if ($search !== FALSE) {
    $data = scraperwiki::select("* from php_tokens.tokens where token=? limit 1", array($search));
} else {
    $data = scraperwiki::select("* from php_tokens.tokens order by token desc limit 10");
}

$json = array();
foreach ($data as $row) {
    $token = $row['token'];
    unset($row['token']);
    $json[$token] = $row;
}

scraperwiki::httpresponseheader('Content-Type', 'application/json');
echo json_encode($json);
<?php

$sourcescraper = 'php_tokens';
scraperwiki::attach($sourcescraper);

$search = (isset($_GET['token']) && preg_match('/^T_[A-Z_]+$/D', $_GET['token'])) ? $_GET['token'] : FALSE;
if ($search !== FALSE) {
    $data = scraperwiki::select("* from php_tokens.tokens where token=? limit 1", array($search));
} else {
    $data = scraperwiki::select("* from php_tokens.tokens order by token desc limit 10");
}

$json = array();
foreach ($data as $row) {
    $token = $row['token'];
    unset($row['token']);
    $json[$token] = $row;
}

scraperwiki::httpresponseheader('Content-Type', 'application/json');
echo json_encode($json);
