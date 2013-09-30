<?php

require 'scraperwiki/simple_html_dom.php';
/* This scraper might work for other areas with pages in the same format */           
$html_content = scraperwiki::scrape("http://tmwa.com/water_system/quality/lookup/central.html");
$html = str_get_html($html_content);

$output = array( 
    'area' => 'central'
);
$save_keys = array( 'area' );

$sample_span = $html->find( '.sample_date' );
$sample_date = ( !empty( $sample_span ) ? str_replace( 'Sample Date:&nbsp;&nbsp;', '', $sample_span[0]->innertext ) : '' );
if ( empty( $sample_date ) )
    exit;

$time = strtotime( $sample_date );
$output['sample_date'] = date( 'Y-m', $time );
$save_keys[] = 'sample_date';

$data_rows = $html->find( '#main_content table tr' );
if ( empty( $data_rows ) ) 
    exit;

$expected_rows = array(
    2 => 'turbidity',
    3 => 'pH',
    4 => 'chlorine',
    5 => 'hardness',
    6 => 'arsenic',
);

$save_record = $output;

foreach( $expected_rows as $row_index => $data_key ) {
    if ( !empty( $data_rows[$row_index] ) ) {
        $cell = $data_rows[$row_index]->find( 'td', 2 );
        if ( $cell ) {
            $unit_link = $cell->find( 'a', 0 );
            $save_record[$data_key] = floatval( array_pop( explode( ' or ', $cell->plaintext ) ) );
            $output[$data_key] = array(
                'value' => floatval( array_pop( explode( ' or ', $cell->plaintext ) ) ),
                'units' => ( $unit_link ? $unit_link->plaintext : '' ),
            );
        }
    }
}

scraperwiki::save( $save_keys, $save_record );
?>
<?php

require 'scraperwiki/simple_html_dom.php';
/* This scraper might work for other areas with pages in the same format */           
$html_content = scraperwiki::scrape("http://tmwa.com/water_system/quality/lookup/central.html");
$html = str_get_html($html_content);

$output = array( 
    'area' => 'central'
);
$save_keys = array( 'area' );

$sample_span = $html->find( '.sample_date' );
$sample_date = ( !empty( $sample_span ) ? str_replace( 'Sample Date:&nbsp;&nbsp;', '', $sample_span[0]->innertext ) : '' );
if ( empty( $sample_date ) )
    exit;

$time = strtotime( $sample_date );
$output['sample_date'] = date( 'Y-m', $time );
$save_keys[] = 'sample_date';

$data_rows = $html->find( '#main_content table tr' );
if ( empty( $data_rows ) ) 
    exit;

$expected_rows = array(
    2 => 'turbidity',
    3 => 'pH',
    4 => 'chlorine',
    5 => 'hardness',
    6 => 'arsenic',
);

$save_record = $output;

foreach( $expected_rows as $row_index => $data_key ) {
    if ( !empty( $data_rows[$row_index] ) ) {
        $cell = $data_rows[$row_index]->find( 'td', 2 );
        if ( $cell ) {
            $unit_link = $cell->find( 'a', 0 );
            $save_record[$data_key] = floatval( array_pop( explode( ' or ', $cell->plaintext ) ) );
            $output[$data_key] = array(
                'value' => floatval( array_pop( explode( ' or ', $cell->plaintext ) ) ),
                'units' => ( $unit_link ? $unit_link->plaintext : '' ),
            );
        }
    }
}

scraperwiki::save( $save_keys, $save_record );
?>
