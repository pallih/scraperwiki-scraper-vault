<?php

require 'scraperwiki/simple_html_dom.php';

class site{

    public $dom;
    public $html;
    public $url;
    public $exp;
    public $pages = array();
    public $get_pages = false;
    public $subpages;
    public $loaded_pages = array();

    function __construct(){
        
    }

    function scrape(){
        $this->html = scraperWiki::scrape($this->url);
        $this->dom = new simple_html_dom();
        $this->dom->load($this->html);
    }
    
    function parse($html){
        return $this->dom->find($html);
    }

    function loadProducts(){
        $dds = $this->dom->find($this->exp->products->holders);
        foreach($dds as $dd){
            $name = $dd->find($this->exp->products->title);
        }
    }

    function loadPages(){
        $this->loaded_pages = scraperwiki::sqliteexecute('select * from pc_garage_pages');
        if(count($this->loaded_pages)>0) return;
        $links = $this->parse($this->exp->pages->link);
        foreach($links as $link){
            $this->pages[] = array('id'=>count($this->pages),'url'=>$link->href,'title'=>$link->plaintext);
        }
    }

    function save_data(){
        // save pages
        if($this->get_pages){
            foreach($this->pages as $page){
                scraperwiki::save_sqlite(array('id','url'), $page, "pc_garage_pages");
            }
        }
    }

}


class pcgarage extends site{
    
    public $url = "http://www.pcgarage.ro/";

    function __construct(){
        $product;
        $product->holders = "dd.product_table_holder";
        $product->title = "dd.product_name";
        $this->exp->products = $product;

        $page;
        $page->holder = "li.second_left_category";
        $page->link = "li.second_left_category li a";
        $this->exp->pages = $page;
    }

}

$x = new pcgarage();
$x->scrape();
$x->loadPages();
$x->parse_page();
$x->save_data();
$x->loadProducts();

?>