<?php

error_reporting(-1);

$whitelist = array('localhost', '127.0.0.1');

if( isset($_SERVER['HTTP_HOST']) && in_array($_SERVER['HTTP_HOST'], $whitelist) )
{
    // script is on localhost
    require 'scraperwiki/scraperwiki.php';
    require 'scraperwiki/simple_html_dom.php';

    $url        = "http://localhost/scraperwiki/source/sothebysrealty.html";
    $url_listing    = "http://localhost/scraperwiki/source/sothebysrealty.listing.html";
    $url_listing_gallery    = "http://localhost/scraperwiki/source/sothebysrealty.listing.gallery.html";

    // $url        = "http://www.sothebysrealty.com/eng/sales/int";
    // $url_listing    = "http://www.sothebysrealty.com/eng/sales/detail/180-l-1182-0018078/brilliant-barbizon-pw-terraced-condo-upper-east-side-new-york-ny-10065";

}
else
{
    // script is online
    require 'scraperwiki/simple_html_dom.php';
    
    $url        = "http://www.sothebysrealty.com/eng/sales/int";
    $url_listing    = "http://www.sothebysrealty.com/eng/sales/detail/180-l-1182-0018078/brilliant-barbizon-pw-terraced-condo-upper-east-side-new-york-ny-10065";
}

$verbose    = true;

class autoParser
{
    var $totalPages    = 0;
    var $html    = null;
    var $dom    = null;
    var $url    = null;
    var $verbose    = true;
    var $data    = null;
    
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
        // $this->html = scraperWiki::scrape($this->url);
        $this->html = $this->scrape($this->url);
        $this->dom->load($this->html);
    }

    function getTotalPages()
    {
        // $this->totalPages = 5;
        // return $this->totalPages;
        
        if( empty($this->html) )
        {
            $this->loadHTML();
        }

        $results = $this->dom->find( 'span[@class="index"]' );

        $max_page = intval(str_replace(array('of ',','),'', trim($results[0]->text())));

        $this->totalPages = $max_page;

        return $this->totalPages;
    }
    
    function saveData( $data )
    {
        if( empty($data) ) 
        {
            return;
        }
        
        $datasw = $data;
        
        // Implode photos[] in to multiple columns
        unset($datasw['photos']);
        $i=0;
        foreach( $data['photos'] AS $photo )
        {
            $datasw['photo'.($i+1)] = $photo;
            $i++;
        }
        
        // Implode amenities into text
        unset($datasw['amenities']);
        $datasw['amenities'] = implode(', ',$data['amenities']);

        // Save data
            scraperwiki::save_sqlite(array('id'), $datasw); 

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
            $url = 'http://www.sothebysrealty.com/eng/sales/int/'.$page.'-pg';
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
        
        $listings = $this->dom->find( 'div[@class="description"]/a' );
        // $listings = $this->dom->find( 'h2[@class="item street-address"]/a' );
        // $listings = $this->dom->find( 'div[@class="header adr"]//a' );
        
        $url_components = parse_url($this->url);
        $hostname = $url_components['host'];
        $scheme = $url_components['scheme'];
        
        $this->printMsg( 'Start crawlListingURLs('.$url.')' );
        $this->printMsg( 'count: ' . count($listings) );
        // echo '<pre>';
        // var_dump($listings);
        if( !empty($listings) )
        {
            $this->printMsg( 'Found nodes.' );
            foreach( $listings AS $listing )
            {
                // $this->printMsg( ' - listing' );
                $result = $listing->getAttribute('href');
                if( $result == '#' ) { continue; }
                $this->printMsg( ' - ' . $result );
                
                // Prepend URLs with host name if none is found.
                $parsed_url = parse_url($result);
                if( empty($parsed_url['host']) ) 
                {
                    $result = $scheme . '://' . $hostname . $result;
                }
                
                $results[] = $result;
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
        $spec_properties = $this->dom->find( 'div[@class="omega summary"]/dl/dt' );
        $spec_values = $this->dom->find( 'div[@class="omega summary"]/dl/dd' );
        
        if( empty($spec_properties) || is_null($spec_properties) )
        {
            $this->printMsg( 'This is not a listing page.' );
            return array();
        }
        
        $spec = array();
        $i = 0;
        
        foreach( $spec_properties AS $spec_property )
        {
            $key = strtolower(str_replace(array(':',' '), array('', '_'), trim($spec_property->text())));
            $spec[$key] = trim(preg_replace("/( )\\1+/", "$1", $spec_values[$i]->text()));
            $i++;
        }

        // Get address
        $address_parts = array('city', 'state', 'zip');
        foreach( $address_parts AS $address_part )
        {
            $tmp = $this->dom->find( 'meta[@name="T.z_prop_'.$address_part.'"]' );
            $data[$address_part] = $tmp[0]->getAttribute('content');
        }
        
        
        // Get price
        $price = $this->dom->find( 'ul[@class="price"]/li' );
        $data_price = preg_replace ( '/[^0-9]/', '', $price[0]->text() );
        $data['price'] = '';

        if( is_numeric($data_price) )
        {
            $data['price'] = $data_price;

            // Get currency
            $currency = $this->dom->find( 'ul[@class="price"]/li/em' );
            $data['currency'] = $currency[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve price.' );
        }
        
        // Get listing description
        $data['description'] = '';
        $description = $this->dom->find( 'div[@class="description"]/p' );
        if( isset($description[0]) && is_object($description[0]) )
        {
            $data['description'] .= $description[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve description.' );
        }

        // Get amenities
        $amenities = $this->dom->find( 'dl[@class="amenities group"]/dd' );
        $data['amenities'] = array();
        foreach( $amenities AS $amenity )
        {
            $data['amenities'][] = $amenity->text();
            
        }
        
        // Get photos
        $data['photos'] = $this->getListingPhotos( $this->url . '/photos' );

        // Get listing title
        $title = $this->dom->find( 'h1[@class="item adr"]/span[@class="fn"]' );
        $data['title'] = $title[0]->text();
        
        // Get listing URL
        $data['url'] = $url;
        
        // Get listing ID
        $listing_id = $this->dom->find( 'meta[@name="T.z_prop_id"]' );
        $data['id'] = $listing_id[0]->getAttribute('content');
        
        $listing_id = $this->dom->find( 'input[@id="CallString"]' );
        $data['id2'] = $listing_id[0]->getAttribute('value');

        // Get seller name
        $seller_name = $this->dom->find( 'div[@class="vcard lister group"]//a' );
        $data['seller_name'] = '';
        if( !is_null($seller_name[0]) && is_object($seller_name[0]) )
        {
            $data['seller_name'] = $seller_name[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve seller name.' );
        }

        // Seller phone
        $seller_phone = $this->dom->find( 'span[@class="phone_block phone-num-1"]' );
        $data['seller_phone'] = '';
        if( !is_null($seller_name[0]) && is_object($seller_name[0]) )
        {
            $data['seller_phone'] = $seller_phone[0]->text();
        }
        else
        {
            $this->printMsg( 'Can not retrieve seller phone.' );
        }

        return $data;
    }
    
    function getListingPhotos( $url )
    {
        // $html = scraperWiki::scrape($url);
        $html = $this->scrape($url);

        $dom = new simple_html_dom();
        $dom->load( $html );
        
        $photos = array();
        
        $gallery_photos = $dom->find( 'div[@id="photo_gallery"]/img' );

        foreach( $gallery_photos AS $gallery_photo )
        {
            $src = $gallery_photo->getAttribute('src');
            parse_str($src, $query);
            $photos[] = $query['amp;ImageURL'];
        }
        
        return $photos;
    }
    
    function printMsg( $msg )
    {
        if( $this->verbose )
        {
            if( $this->isOnline() )
            {
                echo $msg;
            }
            else
            {
                echo '<br />'.$msg;
            }
        }
    }
    
    function scrape($url)
       {
          $curl = curl_init($url);
          curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
          curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
          curl_setopt($curl, CURLOPT_MAXREDIRS, 10);

          // Added by CY to circumvent sothebysrealty.com
          curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows; Intel Mac OS X 10_7_5) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11');
          // disable SSL checking to match behaviour in Python/Ruby.
          // ideally would be fixed by configuring curl to use a proper 
          // reverse SSL proxy, and making our http proxy support that.
          curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
          $res = curl_exec($curl);
          curl_close($curl);
          return $res;
       }
}

$parser = new autoParser();

// *** ACTUAL CRAWL
$parser->setURL( $url );
$parser->loadHTML();
$parser->crawlAll();
// 
// echo '<pre>';
// var_dump($parser->data);
// echo '</pre>';

// *** Construct Total pages
// $parser->setURL( $url );
// $parser->getTotalPages();

// *** Construct Listing URLs
// $parser->crawlListingURLs( $url );

// *** Construct Listing crawl
// $data = $parser->crawlListing( $url_listing );

// *** Construct Listing's gallery photo crawl
// $data = $parser->getListingPhotos( $url_listing_gallery );
// var_dump($data);

// $parser->saveData( $data );

$parser->printMsg( 'Crawl Completed!' );
?>