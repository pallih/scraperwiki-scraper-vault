<?php
require 'scraperwiki/simple_html_dom.php'; 

define( "SOURCE", "www.theage.com.au" );
define( "YEAR", date( 'Y' ) );

$html = scraperwiki::scrape( "http://www.theage.com.au/afl/tipping" );
$dom = new simple_html_dom();
$dom->load( $html );

// This is here because if I call get_var without calling set_var first, then it busts,
// so the first time I run this I'll need to uncomment this line, then recomment for 
// further runs...
// scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", 0 );

// Find out which round we are tipping for currently...
$title = $dom->find( "#title" );
$round = 0;
if ( is_array( $title ) && count( $title ) > 0 ) {
  $titleText = $title[0]->plaintext;
  $i = strpos( $titleText, "Round " );
  $round = (int)substr( $titleText, $i + 6 /* 6 == strlen( "Round " ) */ );
}

// If we can't find out the round number, then 
if ( $round <= 0 ) {
  echo "Cannot find round number, bailing...\n";
  exit;
} else if ( $round == scraperwiki::get_var( SOURCE . "-" . YEAR . "-lastRound" ) ) {
  echo "Already have data for this round, bailing...\n";
  exit;
}

// REMOVED: Just save them all in a big flat table...
// echo "Saving round " . $round . " from " . SOURCE . "\n";
// $roundData = array( 'round' => $round, 'source' => SOURCE, 'year' => YEAR );
// scraperwiki::save_sqlite( array( "source", "round" ), $roundData, "round" );

// Find each expert and their respective tips...
foreach( $dom->find( "ul.expert li" ) as $li ) {
  $nameNode = $li->find( 'h4' );
  if ( is_array( $nameNode ) && count( $nameNode ) > 0 ) {
    
    $expertName = $nameNode[0]->plaintext;
    
    // REMOVED: Just save them all in a big flat table...
    // Save expert to database...
    // $expert = array( 'name' => $expertName, 'source' => SOURCE );
    // scraperwiki::save_sqlite( array( "name" ), $expert, "expert" );

    // What is their current score as of the start of this round?
    $currentScore = $li->find( 'cite' );
    if ( is_array( $currentScore ) && count( $currentScore ) > 0 ) {
      $currentScore = $currentScore[0]->plaintext;
      $start = strpos( $currentScore, "(" );
      $end = strpos( $currentScore, ")" );
      $str = substr( $currentScore, $start + 1, -( strlen( $currentScore ) - $end ) );
      $parts = explode( "/", $str );

      if ( count( $parts ) != 2 ) {
        echo "Couldn't find score for " . $expertName . " (tried to parse '" . $currentScore . "), bailing...\n";
        exit;
      }

      $correct = (int)$parts[ 0 ];
      $total = (int)$parts[ 1 ];
      $score = $correct / $total * 100; 
      $scoreRow = array( 
        'expert' => $expertName,
        'round' => $round,
        'year' => YEAR,
        'source' => SOURCE,
        'score' => $score,
        'correct' => $correct,
        'total' => $total
      );
      echo "Saving current results for " . $expertName . " - " . number_format( $score, 2 ) . "% (" . $correct . "/" . $total . ")\n";
      scraperwiki::save_sqlite( array( "expert", "round", "year", "score", "correct", "total", "source" ), $scoreRow, "results" );
    }

    // Then find out what tips they have submitted...
    $tipsList = $li->find( "ul li" );
    echo "Tips for " . $expertName . ":\n";
    $gameNum = 1;
    foreach( $tipsList as $tipLi ) {

      echo " - " . $tipLi->plaintext . "\n";
      $tipRow = array(
        "expert" => $expertName,
        "round" => $round,
        "year" => YEAR,
        "gameNum" => $gameNum ++,
        "tip" => $tipLi->plaintext,
        "source" => SOURCE
      );
      scraperwiki::save_sqlite( array( "expert", "round", "source", "year", "gameNum" ), $tipRow, "tips" );

    }
  }
}

scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", $round );
<?php
require 'scraperwiki/simple_html_dom.php'; 

define( "SOURCE", "www.theage.com.au" );
define( "YEAR", date( 'Y' ) );

$html = scraperwiki::scrape( "http://www.theage.com.au/afl/tipping" );
$dom = new simple_html_dom();
$dom->load( $html );

// This is here because if I call get_var without calling set_var first, then it busts,
// so the first time I run this I'll need to uncomment this line, then recomment for 
// further runs...
// scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", 0 );

// Find out which round we are tipping for currently...
$title = $dom->find( "#title" );
$round = 0;
if ( is_array( $title ) && count( $title ) > 0 ) {
  $titleText = $title[0]->plaintext;
  $i = strpos( $titleText, "Round " );
  $round = (int)substr( $titleText, $i + 6 /* 6 == strlen( "Round " ) */ );
}

// If we can't find out the round number, then 
if ( $round <= 0 ) {
  echo "Cannot find round number, bailing...\n";
  exit;
} else if ( $round == scraperwiki::get_var( SOURCE . "-" . YEAR . "-lastRound" ) ) {
  echo "Already have data for this round, bailing...\n";
  exit;
}

// REMOVED: Just save them all in a big flat table...
// echo "Saving round " . $round . " from " . SOURCE . "\n";
// $roundData = array( 'round' => $round, 'source' => SOURCE, 'year' => YEAR );
// scraperwiki::save_sqlite( array( "source", "round" ), $roundData, "round" );

// Find each expert and their respective tips...
foreach( $dom->find( "ul.expert li" ) as $li ) {
  $nameNode = $li->find( 'h4' );
  if ( is_array( $nameNode ) && count( $nameNode ) > 0 ) {
    
    $expertName = $nameNode[0]->plaintext;
    
    // REMOVED: Just save them all in a big flat table...
    // Save expert to database...
    // $expert = array( 'name' => $expertName, 'source' => SOURCE );
    // scraperwiki::save_sqlite( array( "name" ), $expert, "expert" );

    // What is their current score as of the start of this round?
    $currentScore = $li->find( 'cite' );
    if ( is_array( $currentScore ) && count( $currentScore ) > 0 ) {
      $currentScore = $currentScore[0]->plaintext;
      $start = strpos( $currentScore, "(" );
      $end = strpos( $currentScore, ")" );
      $str = substr( $currentScore, $start + 1, -( strlen( $currentScore ) - $end ) );
      $parts = explode( "/", $str );

      if ( count( $parts ) != 2 ) {
        echo "Couldn't find score for " . $expertName . " (tried to parse '" . $currentScore . "), bailing...\n";
        exit;
      }

      $correct = (int)$parts[ 0 ];
      $total = (int)$parts[ 1 ];
      $score = $correct / $total * 100; 
      $scoreRow = array( 
        'expert' => $expertName,
        'round' => $round,
        'year' => YEAR,
        'source' => SOURCE,
        'score' => $score,
        'correct' => $correct,
        'total' => $total
      );
      echo "Saving current results for " . $expertName . " - " . number_format( $score, 2 ) . "% (" . $correct . "/" . $total . ")\n";
      scraperwiki::save_sqlite( array( "expert", "round", "year", "score", "correct", "total", "source" ), $scoreRow, "results" );
    }

    // Then find out what tips they have submitted...
    $tipsList = $li->find( "ul li" );
    echo "Tips for " . $expertName . ":\n";
    $gameNum = 1;
    foreach( $tipsList as $tipLi ) {

      echo " - " . $tipLi->plaintext . "\n";
      $tipRow = array(
        "expert" => $expertName,
        "round" => $round,
        "year" => YEAR,
        "gameNum" => $gameNum ++,
        "tip" => $tipLi->plaintext,
        "source" => SOURCE
      );
      scraperwiki::save_sqlite( array( "expert", "round", "source", "year", "gameNum" ), $tipRow, "tips" );

    }
  }
}

scraperwiki::save_var( SOURCE . "-" . YEAR . "-lastRound", $round );
