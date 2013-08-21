<?php

function curl( $options )
{
    $ch = curl_init();
    
    curl_setopt ( $ch, CURLOPT_URL, $options["url"] );
    curl_setopt ( $ch, CURLOPT_SSL_VERIFYPEER, FALSE );
    curl_setopt ( $ch, CURLOPT_USERAGENT, "Medic Cabinet Mapper v 1.0 /  Non-Commercial purposes only / Running for a limited amount of time (few days) / ~8 second delay between most requests / Text only" );
    
    if ( isset( $options["timeout"] ) )
    {
        curl_setopt ( $ch, CURLOPT_TIMEOUT, $options["timeout"] );
    }
    
    if ( isset( $options["connectionTimeout"] ) )
    {
        curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, $options["connectionTimeout"] );
    }
    
    if ( isset( $options["allowRedirect"] ) )
    {
        curl_setopt ( $ch, CURLOPT_FOLLOWLOCATION, $options["allowRedirect"] );
    }
    
    if( isset( $options["cookieSetFile"] ) )
    {
        curl_setopt ( $ch, CURLOPT_COOKIEJAR, $options["cookieSetFile"] );
    }
    
    if( isset( $options["cookieGetFile"] ) )
    {
        curl_setopt ( $ch, CURLOPT_COOKIEFILE, $options["cookieGetFile"] );
    }
    
    if( isset( $options["binaryTransfer"] ) )
    {
        curl_setopt ( $ch, CURLOPT_BINARYTRANSFER, 1 );
    }
    
    if( isset( $options["referer"] ) )
    {
        curl_setopt ( $ch, CURLOPT_REFERER, $options["referer"] );
    }
    
    curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, 1 );
    
    curl_setopt ( $ch, CURLOPT_HEADER, ( isset( $options["includeHeaders"] ) ) ? $options["includeHeaders"] : false );

    
    if( isset( $options["postData"] ) )
    {
        curl_setopt ( $ch, CURLOPT_POSTFIELDS, $options["postData"] );
        curl_setopt ( $ch, CURLOPT_POST, 1 );
    }

    if ( isset( $options["headers"] ) )
    {
        curl_setopt ( $ch, CURLOPT_HTTPHEADER, $options["headers"] );
    }
    
    $data = curl_exec ( $ch );
    $info = curl_getinfo( $ch );
    
    curl_close( $ch );
    
    return array( "info" => $info, "content" => $data );
}

// Accepts keywords and page
function fetchQueryResult( $keywords, $page )
{
    $keywords = rawurlencode( $keywords );
    $address = "http://www.paginegialle.it/pgol/4-$keywords/p-$page?mr=50";

    $response = curl( array(
        "url" => $address
    ) );
    
    $content = $response["content"];
    if ( isset( $content ) && ( strlen( $content ) > 0 ) )
    {
        $doc = new DOMDocument();
        @$doc->loadHTML( $content );
        
        $finder = new DomXPath( $doc );
        
        $resultNodes = $finder->query( "//div[not(@*)]/div[contains(@class,'item')]" );
        if ( isset( $resultNodes ) )
        {
            foreach( $resultNodes as $node )
            {
                $pageType = 0;
                
                // Type 1
                if ( $node->hasAttribute( "id" ) )
                {
                    $pageType = 1;
                }
                else
                {
                    if ( $node->hasAttribute( "class" ) )
                    {
                        $nodeClass = $node->getAttribute( "class" );
                        if ( isset( $nodeClass ) )
                        {
                            if ( strstr( $nodeClass, "contextuallight" ) )
                            {
                                $pageType = 3;                            
                            }
                        }
                    }                
                }
                
                $nameURLNode = $finder->query( ".//a[@href][1]", $node );
                if ( $resultURL = $nameURLNode->item( 0 ) )
                {
                    $resultURL = $resultURL->getAttribute( "href" );
                    $resultURL = preg_replace( "#((%7E)[/]*)#", "", $resultURL );
                    
                    // Fetch page
                    $entryPageContent = fetchEntryPage( $resultURL );
                    if ( strlen( $entryPageContent ) <= 0 )
                    {
                        print( "Timeout for sub-cabinet $resultURL. Skipping..." );
                        continue;
                    }
                    
                    if ( $pageType == 1 )
                    {
                        $entryContactContent = "";

                        //$nodesContact = $finder->query( "//div[@class='web-contatti']/a[@turl and text()[contains(.,'email')]]" );
                        //if ( $contactNode = $nodesContact->item( 0 ) )

                        if ( strstr( $entryPageContent, "email" ) )
                        {
                            $entryContactContent = fetchEntryContactPage( $resultURL );
                            print( "Also fetching contact info for $resultURL" );
                        }
                        
                        scraperwiki::save_sqlite( array( "url" ), array( "url" => $resultURL, "type" => $pageType, "parent_page_content" => $entryPageContent, "contact_page_content" => $entryContactContent ) );   
                    }
                    else
                    {
                        if ( $pageType == 3 )
                        {
                            $maxPage = 1;
                            $storesContentList = array();
                            
                            for ( $j = 0; $j < $maxPage; $j++ )
                            {
                                $storePageContent = fetchStorePage( $resultURL, $j );
                                if ( isset( $storePageContent ) )
                                {
                                    if ( preg_match( "#(?<=(\"total_pages\":))([0-9]+)#", $storePageContent, $matches ) )
                                    {
                                        $maxPage = intval( $matches[0] );
                                    }
                                    
                                    $storesContentList["store_$j"] = $storePageContent;
                                }
                            }
                            
                            scraperwiki::save_sqlite( array( "url" ), array_merge( array( "url" => $resultURL, "type" => $pageType, "parent_page_content" => $entryPageContent, "page_store_count" => count( $storesContentList ) ), $storesContentList ) );   
                        }                    
                    }
                }

                sleep( 2.5 );
            }
        }
    }
    else
    {
        print( "Timeout on $page for $keywords" );
    }
}    

register_shutdown_function( 'handleShutdown' );

$currentPage = 1;
$myVar = getVariable( "currentPage" );
if ( isset( $myVar ) )
{
    $currentPage = getVariable( "currentPage" );
}

function handleShutdown()
{
    global $currentPage;

    $error = error_get_last();
    if( $error !== NULL )
    {
        setVariable( "currentPage", $currentPage + 1 );
    }
}

function getVariable( $key )
{
    try
    {
        return scraperwiki::get_var( $key );
    }
    catch( Exception $e )
    {
        return;
    }
}

function setVariable( $key, $value )
{
    scraperwiki::save_var( $key, $value );
}

// Root page
function fetchEntryPage( $address )
{
    $response = curl( array(
        "url" => $address,
        "connectionTimeout" => 8
    ) );
    
    return $response["content"];
}

// Accepts root address and store page
function fetchStorePage( $address, $page )
{
    if ( $uri = parse_url( $address ) )
    {
        if ( array_key_exists( "path", $uri ) )
        {
            $path = $uri["path"];
            
            if ( preg_match( "/[\w]+/", $path, $matches ) )
            {        
                if ( isset( $matches[0] ) )
                {
                    $address = "http://pgmultilocator.paginegialle.it/search_bnc.php?lat=41.89488&lon=12.49360&radius=none&bnc_lnk=$matches[0]&n_page=$page";
                    
                    $response = curl( array(
                        "url" => $address,
                        "connectionTimeout" => 8
                    ) );
                    
                    return $response["content"];
                }
            }
        }
    }
}

// Accepts root address
function fetchEntryContactPage( $address )
{
    $address = "$address/contatto?lt=frag";
    
    $response = curl( array(
        "url" => $address,
        "connectionTimeout" => 8
    ) );
    
    return $response["content"];
}


//------------------------------ OPTIONS ---------------------------------//

//setVariable( "currentPage", 34 ); // You can set a starting page by uncommenting these two lines here, setting the number (where 15 is now)
//$currentPage = getVariable( "currentPage" ); // then starting the bot; afterward, you need to comment the lines, if you don't want your bot to keep starting 

$endPage = 360; // Change the maximum page of the search keywords page (50 entries per page)
$keywords = "centro benessere"; // Change keywords here

//-----------------------------------------------------------------------//

$startPage = $currentPage;

for ( $i = $startPage; $i < $endPage; $i++ )
{
    $currentPage = $i;
    print( "Processing $currentPage" );

    try
    {
        fetchQueryResult( $keywords, $i );
    }
    catch( Exception $e )
    {
        print( "Exception for results page $i..." );
    }
    setVariable( "currentPage", $currentPage + 1 );
}


?>