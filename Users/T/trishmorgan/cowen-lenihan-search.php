<?php


# i need to find a way of excluding the first result in every search because that just says 'Twitter Search'


require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=cowen+idiot") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
    

##### second search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=lenihan+idiot") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}



##### third search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=cowen+gobshite") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}





##### fourth search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=lenihan+gobshite") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}



?>
<?php


# i need to find a way of excluding the first result in every search because that just says 'Twitter Search'


require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=cowen+idiot") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}
    

##### second search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=lenihan+idiot") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}



##### third search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=cowen+gobshite") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}





##### fourth search string

$html = scraperwiki::scrape ("http://search.twitter.com/search.rss?q=lenihan+gobshite") ;
#print $html;



    $dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find('title') as $data)
{
    print $data->plaintext . "\n";
}


foreach($dom->find('title') as $data)
{
    scraperwiki::save(array('data'), array('data' => $data->plaintext));
}



?>
