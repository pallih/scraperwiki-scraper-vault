<?php
require 'scraperwiki/simple_html_dom.php';     
$base_url = "http://www.icarros.com.br/catalogo/index.jsp";

//$brands = getBrands($base_url);
$versions = getModelsYears("/volkswagen/gol/");

function getBrands($base_url) {
    $html = scraperWiki::scrape($base_url);     
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("table.diretorio tr");

    foreach ($rows as $row) {
        $columns = $row->find("td a");
        foreach ($columns as $column) {
            $brand_name = $column->plaintext;
            $brand_url = $column->href;
            $brands[$brand_name] =  getModels($brand_url);
        }
    }
    return $brands;
}

function getModels($brand_url) {
    $url = "http://www.icarros.com.br" . $brand_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("li.modelo h1 a");

    foreach($rows as $row) {
        $model_name = $row->plaintext;
        $url = $row->href;
        $models[$model_name] = getVersions($url);
    }
    return $models;
}

function getModelsYears($model_url) {
    $url = "http://www.icarros.com.br" . $model_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("div.outrosanosmodelo tbody tr");

    $count = 0;
    foreach ($rows as $row) {
        if ($count > 0) {
            $year = $row->find("td", 0)->plaintext;
            $year_url = $row->find("td a", 0)->href;
            $versions[$year] = getYears($year_url);
        }
        $count++;
    }
}

function getYears($year_url) {
    $url = "http://www.icarros.com.br" . $year_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);    
    
    $rows = $dom->find("table.listaversoesofertas tbody tr");

    $count = 0;
    foreach($rows as $row) {
        if ($count > 0) {
            $version_url = $row->find("td a", 0)->href;
            print $version_url . "\n";
        }
        $count++;
    }
}<?php
require 'scraperwiki/simple_html_dom.php';     
$base_url = "http://www.icarros.com.br/catalogo/index.jsp";

//$brands = getBrands($base_url);
$versions = getModelsYears("/volkswagen/gol/");

function getBrands($base_url) {
    $html = scraperWiki::scrape($base_url);     
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("table.diretorio tr");

    foreach ($rows as $row) {
        $columns = $row->find("td a");
        foreach ($columns as $column) {
            $brand_name = $column->plaintext;
            $brand_url = $column->href;
            $brands[$brand_name] =  getModels($brand_url);
        }
    }
    return $brands;
}

function getModels($brand_url) {
    $url = "http://www.icarros.com.br" . $brand_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("li.modelo h1 a");

    foreach($rows as $row) {
        $model_name = $row->plaintext;
        $url = $row->href;
        $models[$model_name] = getVersions($url);
    }
    return $models;
}

function getModelsYears($model_url) {
    $url = "http://www.icarros.com.br" . $model_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $rows = $dom->find("div.outrosanosmodelo tbody tr");

    $count = 0;
    foreach ($rows as $row) {
        if ($count > 0) {
            $year = $row->find("td", 0)->plaintext;
            $year_url = $row->find("td a", 0)->href;
            $versions[$year] = getYears($year_url);
        }
        $count++;
    }
}

function getYears($year_url) {
    $url = "http://www.icarros.com.br" . $year_url;
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);    
    
    $rows = $dom->find("table.listaversoesofertas tbody tr");

    $count = 0;
    foreach($rows as $row) {
        if ($count > 0) {
            $version_url = $row->find("td a", 0)->href;
            print $version_url . "\n";
        }
        $count++;
    }
}