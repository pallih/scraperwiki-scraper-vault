<?php
require 'scraperwiki/simple_html_dom.php';           

    function scrapeSmellsCategories($categoryUrl){

        $html = scraperWiki::scrape($categoryUrl);
        $dom = new simple_html_dom();
        $dom->load($html);

        $cells = $dom->find('div.column h3 a');
        foreach($cells as $cell){
            $url = html_entity_decode( $cell->href);
            $name = $cell->plaintext;
            
            echo $url . "\r\n";
            scrapeSmellsCategory($url);
            
            //break;
        }

    }

    function scrapeSmellsCategory($url){
        $html = scraperWiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);
        $products = $dom->find('div.product');
        foreach($products as $product){
            $brand = $product->find('h3 > a',0);                        
                    

            $productName = $product->find('p.productName > a',0);
            echo $productName->innertext;

            $prices = $product->find('p.productPrice',0);
            $rrp = $prices->find('a',0);
            $ourPrice = $prices->find('a.ourPrice',0);

            $productDesc = $product->find('p.productDesc a',0);
            

            $fixedRrp = substr($rrp->innertext,10); 
            $fixedPrice = substr($ourPrice->innertext,16);

                        

            $data = array(
                        'brand'=> $brand->innertext,
                        'product' => $productName->innertext,
                        'rrp' => $fixedRrp ,
                        'price' => $fixedPrice,
                        'desc' => $productDesc->innertext,
                        'url' => $url );
                    
            scraperWiki::save_sqlite(array('brand', 'product','rrp','price','desc','url'), $data);
        }

        
        
    }

    scrapeSmellsCategories('http://www.cheapsmells.com/productListing.php?category=1');


    

    

?>
<?php
require 'scraperwiki/simple_html_dom.php';           

    function scrapeSmellsCategories($categoryUrl){

        $html = scraperWiki::scrape($categoryUrl);
        $dom = new simple_html_dom();
        $dom->load($html);

        $cells = $dom->find('div.column h3 a');
        foreach($cells as $cell){
            $url = html_entity_decode( $cell->href);
            $name = $cell->plaintext;
            
            echo $url . "\r\n";
            scrapeSmellsCategory($url);
            
            //break;
        }

    }

    function scrapeSmellsCategory($url){
        $html = scraperWiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);
        $products = $dom->find('div.product');
        foreach($products as $product){
            $brand = $product->find('h3 > a',0);                        
                    

            $productName = $product->find('p.productName > a',0);
            echo $productName->innertext;

            $prices = $product->find('p.productPrice',0);
            $rrp = $prices->find('a',0);
            $ourPrice = $prices->find('a.ourPrice',0);

            $productDesc = $product->find('p.productDesc a',0);
            

            $fixedRrp = substr($rrp->innertext,10); 
            $fixedPrice = substr($ourPrice->innertext,16);

                        

            $data = array(
                        'brand'=> $brand->innertext,
                        'product' => $productName->innertext,
                        'rrp' => $fixedRrp ,
                        'price' => $fixedPrice,
                        'desc' => $productDesc->innertext,
                        'url' => $url );
                    
            scraperWiki::save_sqlite(array('brand', 'product','rrp','price','desc','url'), $data);
        }

        
        
    }

    scrapeSmellsCategories('http://www.cheapsmells.com/productListing.php?category=1');


    

    

?>
