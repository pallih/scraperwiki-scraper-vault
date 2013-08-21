<?php
require 'scraperwiki/simple_html_dom.php';

$url = 'http://www.cinema.com.my/cinemas/cinemalist.aspx';
$html = str_get_html(scraperwiki::scrape($url));

$id = 0;

foreach ($html->find("div.contents table tbody tr.row1 td a") as $data)
{
    save_sqlite(++$id, $data);
}

foreach ($html->find("div.contents table tbody tr.row2 td a") as $data)
{
    save_sqlite(++$id, $data);
}


function save_sqlite($id, $data)
{
    $table_name = 'cinema_list';
    $unique_keys = 'id'; // table primary key
    $column1 = 'cinema_name';
    $column2 = 'cinema_id';

    $parsed_url = parse_url($data->href);
    $query = $parsed_url['query'];

    $start_with= "cid=C";
    $position= strpos($query, $start_with);
    $first_removed = substr($query, $position + strlen($start_with));
    $cinema_id = substr($first_removed, 0, strpos($first_removed, "&"));

    scraperwiki::save_sqlite(
                    array($unique_keys),
                    array($unique_keys => $id,
                        $column1 => $data->plaintext,
                        $column2 => $cinema_id),
                    $table_name);
    }

$html->__destruct();
