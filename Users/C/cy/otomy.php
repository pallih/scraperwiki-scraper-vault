<?php

error_reporting(-1);

$whitelist = array('localhost', '127.0.0.1');

if( isset($_SERVER['HTTP_HOST']) && in_array($_SERVER['HTTP_HOST'], $whitelist) )
{
    // script is on localhost
    require 'scraperwiki/scraperwiki.php';
    require 'scraperwiki/simple_html_dom.php';

    $url        = "http://localhost/scraperwiki/source/oto.my.html";
    $url_listing    = "http://localhost/scraperwiki/source/oto.listing.my.html";
}
else
{
    // script is online
    require 'scraperwiki/simple_html_dom.php';
    
    $url        = "http://www.oto.my/cars-for-sale/";
    $url_listing    = "http://www.oto.my/car-for-sale/24204/used-2005-mercedes-benz-cls-class-cls350-brabus-kuala-lumpur";
}

$verbose    = true;

class autoParser
{
    var $totalPages    = 0;
    var $html    = null;
    var $dom    = null;
    var $url    = null;
    var $verbose    = true;
    
    function __construct()
    {
        $this->dom = new simple_html_dom();
    }
    
    function isOnline()
    {
        if( isset($_SERVER['HTTP_HOST']) && in_array($_SERVER['HTTP_HOST'], array('localhost','127.0.0.1')) )
        {
            return false;
        }
        else
        {
            return true;
        }
    }

    function setURL( $url )
    {
        $this->url = $url;
    }

    function loadHTML()
    {
        $this->html = scraperWiki::scrape($this->url);
        $this->dom->load($this->html);
    }

    function getTotalPages()
    {
        $list_items = $this->dom->find( 'div[@class="pagination right"]/ul[1]/*' );

        foreach( $list_items AS $list_item )
        {
            $text = trim($list_item->text());

            if( ord($text) == 38 )
            {
                $result = $list_item->find('a');
                parse_str($result[0]->getAttribute('href'), $url_var);
                
                $this->totalPages = $url_var['pg'];
                return $this->totalPages;

                break;
            }
            
        }
    }
    
    function saveData( $data )
    {
        if( empty($data) ) 
        {
            return;
        }
        
        $datasw = $data;
        unset($datasw['photos']);
        
        $i=0;
        foreach( $data['photos'] AS $photo )
        {
            $datasw['photo'.($i+1)] = $photo;
            $i++;
        }

        if( $this->isOnline() )
        {
                scraperwiki::save_sqlite(array('id'), $datasw); 
        }
        
        $this->printMsg( 'Saving "'.$data['title'].'"... done.' );
    }
    
    function crawlAll( $max_listings=0 )
    {
        if( $this->totalPages <= 0 )
        {
            $this->getTotalPages();
        }
        
        $crawled = 0;
        
        for( $page=1; $page <= $this->totalPages; $page ++ )
        {
            $url = 'http://www.oto.my/cars-for-sale/?&pg=' . $page;
            $this->printMsg( 'Crawling page ' . $page . ' at ' . $url );

            $listing_urls = $this->crawlListingURLs( $url );
            
            foreach( $listing_urls AS $listing_url )
            {
                $data = $this->crawlListing( $listing_url );
                $this->saveData( $data );
                $crawled++;
                
                if( $max_listings > 0 && $crawled >= $max_listings )
                {
                    break 2;
                }
            }
            
        }
    }
    
    function crawlListingURLs( $url )
    {
        $results = array();
        
        if( !empty($url) )
        {
            $this->setURL($url);
            $this->loadHTML();
        }

        if( empty($this->html) )
        {
            $this->loadHTML();
        }
        
        $listings = $this->dom->find( 'div[@class="span12 search-result-holder"]/a' );
        
        if( !empty($listings) )
        {
            foreach( $listings AS $listing )
            {
                $results[] = $listing->getAttribute('href');
            }
        }
        
        $this->printMsg( 'Found ' . count($results) . ' listings.' );
        return $results;
    }
    
    function crawlListing( $url )
    {

        if( !empty($url) )
        {
            $this->setURL($url);
            $this->loadHTML();
        }

        if( empty($this->html) )
        {
            $this->loadHTML();
        }

        $this->printMsg( 'Crawling listing page ' . $url );
        
        // Get listing's specification
        $results = $this->dom->find( 'div[@class="span2"]/small' );
        if( empty($results) || is_null($results) )
        {
            $this->printMsg( 'This is not a listing page.' );
            return array();
        }
        

        $captions = array('Car Make', 'Car Model', 'Car Variant', 'Year', 'Condition', 'Mileage', 'Transmission', 'Engine Capacity', 'Body Type', 'Location', 'Time Posted', 'Last Updated');
        $data = array();
        $i = 0;
        foreach( $results AS $result )
        {
            $arrResults[] = $result->text();
            $i++;
        }

        $i=0;
        foreach( $arrResults AS $result )
        {
            if( $key = array_search($result,$captions) )
            {
                $data[str_replace(' ', '_', strtolower($captions[$key]))] = $arrResults[$i+1];
            }
            $i++;
        }
        
        // Get price
        $price = $this->dom->find( 'input[@id="loan-total"]' );
        if( is_object($price[0]) )
        {
            $data['price'] = $price[0]->getAttribute('value');
        }
        else
        {
            $this->printMsg( 'Can not retrieve price.' );
        }

        // Get listing description
        $description = $this->dom->find( 'div[@id="description-content"]/small' );
        if( isset($description[0]) && is_object($description[0]) )
        {
            $data['description'] = $description[1]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve description.' );
        }

        // Get photos
        $photos_small = $this->dom->find( 'div[@class="thumbnail-image"]/a/img' );
        $photos_medium = $this->dom->find( 'div[@class="listing-big-image-inner-holder"]/a/img' );
        $photos_large = $this->dom->find( 'div[@class="thumbnail-image"]/a' );
        
        $photos = array();
        $i=0;
        foreach( $photos_small AS $photo )
        {
            // echo '<br />';
            // echo 'Thumbnail: ';
            // echo $photo->getAttribute('src');
            // echo '<br />';
            // echo 'Medium: ';
            // echo $photos_medium[$i]->getAttribute('src');
            // echo '<br />';
            // echo 'Large: ';
            // echo $photos_large[$i]->getAttribute('href');
            $photos[] = $photos_large[$i]->getAttribute('href');
            $i++;
        }
        $data['photos'] = $photos;
        
        // Get listing title
        $data['title'] = $photos_large[0]->getAttribute('title');
        
        // Get listing URL
        $listing_id = $this->dom->find( 'link[@rel="canonical"]' );
        $data['url'] = $listing_id[0]->getAttribute( 'href' );
        
        // Get listing ID
        $data['id'] = basename(dirname($data['url']));
        
        // Get seller type
        $seller_type['company'] = $this->dom->find( 'span[@class="label label-info listing-badge-style company-account-badge"]' );
        $seller_type['individual'] = $this->dom->find( 'span[@class="label label-info listing-badge-style individual-account-badge"]' );
        $seller_type['sales_agent'] = $this->dom->find( 'span[@class="label label-info listing-badge-style sales-agent-account-badge"]' );

        if( !empty($seller_type['individual']) )
        {
            $data['seller_type'] = 'individual';
        }
        elseif( !empty($seller_type['company']) )
        {
            $data['seller_type'] = 'company';
        }
        elseif( !empty($seller_type['sales_agent']) )
        {
            $data['seller_type'] = 'sales_agent';
        }
        
        // Get seller name
        $seller_name = $this->dom->find( 'small[@class="pull-left listing-posted-by-name"]' );
        $data['seller_name'] = '';
        if( !is_null($seller_name[0]) && is_object($seller_name[0]) )
        {
            $data['seller_name'] = $seller_name[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve seller name.' );
        }
        
        // Get seller details
        $seller_details = $this->dom->find( 'div[@class="seller-detail-info-right"]' );

        switch( $data['seller_type'] )
        {
            case 'company':
                $data['seller_address'] = trim($seller_details[1]->text());
                break;
            case 'sales_agent':
                $data['seller_address'] = trim($seller_details[2]->text());
                break;
            case 'individual':
                $data['seller_address'] = '';
                break;
            
        }

        return $data;
        
    }
    
    function printMsg( $msg )
    {
        if( $this->verbose )
        {
            echo $msg;
        }
    }
}

$parser = new autoParser();

$parser->setURL( $url );
$parser->loadHTML();
$parser->crawlAll();

// $url        = "http://localhost/scraperwiki/source/oto.my.html";
// $parser->crawlListingURLs( $url );

// $data = $parser->crawlListing( $url_listing );
// $parser->saveData( $data );

$parser->printMsg( 'Crawl Completed!' );
?><?php

error_reporting(-1);

$whitelist = array('localhost', '127.0.0.1');

if( isset($_SERVER['HTTP_HOST']) && in_array($_SERVER['HTTP_HOST'], $whitelist) )
{
    // script is on localhost
    require 'scraperwiki/scraperwiki.php';
    require 'scraperwiki/simple_html_dom.php';

    $url        = "http://localhost/scraperwiki/source/oto.my.html";
    $url_listing    = "http://localhost/scraperwiki/source/oto.listing.my.html";
}
else
{
    // script is online
    require 'scraperwiki/simple_html_dom.php';
    
    $url        = "http://www.oto.my/cars-for-sale/";
    $url_listing    = "http://www.oto.my/car-for-sale/24204/used-2005-mercedes-benz-cls-class-cls350-brabus-kuala-lumpur";
}

$verbose    = true;

class autoParser
{
    var $totalPages    = 0;
    var $html    = null;
    var $dom    = null;
    var $url    = null;
    var $verbose    = true;
    
    function __construct()
    {
        $this->dom = new simple_html_dom();
    }
    
    function isOnline()
    {
        if( isset($_SERVER['HTTP_HOST']) && in_array($_SERVER['HTTP_HOST'], array('localhost','127.0.0.1')) )
        {
            return false;
        }
        else
        {
            return true;
        }
    }

    function setURL( $url )
    {
        $this->url = $url;
    }

    function loadHTML()
    {
        $this->html = scraperWiki::scrape($this->url);
        $this->dom->load($this->html);
    }

    function getTotalPages()
    {
        $list_items = $this->dom->find( 'div[@class="pagination right"]/ul[1]/*' );

        foreach( $list_items AS $list_item )
        {
            $text = trim($list_item->text());

            if( ord($text) == 38 )
            {
                $result = $list_item->find('a');
                parse_str($result[0]->getAttribute('href'), $url_var);
                
                $this->totalPages = $url_var['pg'];
                return $this->totalPages;

                break;
            }
            
        }
    }
    
    function saveData( $data )
    {
        if( empty($data) ) 
        {
            return;
        }
        
        $datasw = $data;
        unset($datasw['photos']);
        
        $i=0;
        foreach( $data['photos'] AS $photo )
        {
            $datasw['photo'.($i+1)] = $photo;
            $i++;
        }

        if( $this->isOnline() )
        {
                scraperwiki::save_sqlite(array('id'), $datasw); 
        }
        
        $this->printMsg( 'Saving "'.$data['title'].'"... done.' );
    }
    
    function crawlAll( $max_listings=0 )
    {
        if( $this->totalPages <= 0 )
        {
            $this->getTotalPages();
        }
        
        $crawled = 0;
        
        for( $page=1; $page <= $this->totalPages; $page ++ )
        {
            $url = 'http://www.oto.my/cars-for-sale/?&pg=' . $page;
            $this->printMsg( 'Crawling page ' . $page . ' at ' . $url );

            $listing_urls = $this->crawlListingURLs( $url );
            
            foreach( $listing_urls AS $listing_url )
            {
                $data = $this->crawlListing( $listing_url );
                $this->saveData( $data );
                $crawled++;
                
                if( $max_listings > 0 && $crawled >= $max_listings )
                {
                    break 2;
                }
            }
            
        }
    }
    
    function crawlListingURLs( $url )
    {
        $results = array();
        
        if( !empty($url) )
        {
            $this->setURL($url);
            $this->loadHTML();
        }

        if( empty($this->html) )
        {
            $this->loadHTML();
        }
        
        $listings = $this->dom->find( 'div[@class="span12 search-result-holder"]/a' );
        
        if( !empty($listings) )
        {
            foreach( $listings AS $listing )
            {
                $results[] = $listing->getAttribute('href');
            }
        }
        
        $this->printMsg( 'Found ' . count($results) . ' listings.' );
        return $results;
    }
    
    function crawlListing( $url )
    {

        if( !empty($url) )
        {
            $this->setURL($url);
            $this->loadHTML();
        }

        if( empty($this->html) )
        {
            $this->loadHTML();
        }

        $this->printMsg( 'Crawling listing page ' . $url );
        
        // Get listing's specification
        $results = $this->dom->find( 'div[@class="span2"]/small' );
        if( empty($results) || is_null($results) )
        {
            $this->printMsg( 'This is not a listing page.' );
            return array();
        }
        

        $captions = array('Car Make', 'Car Model', 'Car Variant', 'Year', 'Condition', 'Mileage', 'Transmission', 'Engine Capacity', 'Body Type', 'Location', 'Time Posted', 'Last Updated');
        $data = array();
        $i = 0;
        foreach( $results AS $result )
        {
            $arrResults[] = $result->text();
            $i++;
        }

        $i=0;
        foreach( $arrResults AS $result )
        {
            if( $key = array_search($result,$captions) )
            {
                $data[str_replace(' ', '_', strtolower($captions[$key]))] = $arrResults[$i+1];
            }
            $i++;
        }
        
        // Get price
        $price = $this->dom->find( 'input[@id="loan-total"]' );
        if( is_object($price[0]) )
        {
            $data['price'] = $price[0]->getAttribute('value');
        }
        else
        {
            $this->printMsg( 'Can not retrieve price.' );
        }

        // Get listing description
        $description = $this->dom->find( 'div[@id="description-content"]/small' );
        if( isset($description[0]) && is_object($description[0]) )
        {
            $data['description'] = $description[1]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve description.' );
        }

        // Get photos
        $photos_small = $this->dom->find( 'div[@class="thumbnail-image"]/a/img' );
        $photos_medium = $this->dom->find( 'div[@class="listing-big-image-inner-holder"]/a/img' );
        $photos_large = $this->dom->find( 'div[@class="thumbnail-image"]/a' );
        
        $photos = array();
        $i=0;
        foreach( $photos_small AS $photo )
        {
            // echo '<br />';
            // echo 'Thumbnail: ';
            // echo $photo->getAttribute('src');
            // echo '<br />';
            // echo 'Medium: ';
            // echo $photos_medium[$i]->getAttribute('src');
            // echo '<br />';
            // echo 'Large: ';
            // echo $photos_large[$i]->getAttribute('href');
            $photos[] = $photos_large[$i]->getAttribute('href');
            $i++;
        }
        $data['photos'] = $photos;
        
        // Get listing title
        $data['title'] = $photos_large[0]->getAttribute('title');
        
        // Get listing URL
        $listing_id = $this->dom->find( 'link[@rel="canonical"]' );
        $data['url'] = $listing_id[0]->getAttribute( 'href' );
        
        // Get listing ID
        $data['id'] = basename(dirname($data['url']));
        
        // Get seller type
        $seller_type['company'] = $this->dom->find( 'span[@class="label label-info listing-badge-style company-account-badge"]' );
        $seller_type['individual'] = $this->dom->find( 'span[@class="label label-info listing-badge-style individual-account-badge"]' );
        $seller_type['sales_agent'] = $this->dom->find( 'span[@class="label label-info listing-badge-style sales-agent-account-badge"]' );

        if( !empty($seller_type['individual']) )
        {
            $data['seller_type'] = 'individual';
        }
        elseif( !empty($seller_type['company']) )
        {
            $data['seller_type'] = 'company';
        }
        elseif( !empty($seller_type['sales_agent']) )
        {
            $data['seller_type'] = 'sales_agent';
        }
        
        // Get seller name
        $seller_name = $this->dom->find( 'small[@class="pull-left listing-posted-by-name"]' );
        $data['seller_name'] = '';
        if( !is_null($seller_name[0]) && is_object($seller_name[0]) )
        {
            $data['seller_name'] = $seller_name[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve seller name.' );
        }
        
        // Get seller details
        $seller_details = $this->dom->find( 'div[@class="seller-detail-info-right"]' );

        switch( $data['seller_type'] )
        {
            case 'company':
                $data['seller_address'] = trim($seller_details[1]->text());
                break;
            case 'sales_agent':
                $data['seller_address'] = trim($seller_details[2]->text());
                break;
            case 'individual':
                $data['seller_address'] = '';
                break;
            
        }

        return $data;
        
    }
    
    function printMsg( $msg )
    {
        if( $this->verbose )
        {
            echo $msg;
        }
    }
}

$parser = new autoParser();

$parser->setURL( $url );
$parser->loadHTML();
$parser->crawlAll();

// $url        = "http://localhost/scraperwiki/source/oto.my.html";
// $parser->crawlListingURLs( $url );

// $data = $parser->crawlListing( $url_listing );
// $parser->saveData( $data );

$parser->printMsg( 'Crawl Completed!' );
?>