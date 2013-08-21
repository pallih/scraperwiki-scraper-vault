<?php
/*/
 *
 * Copyright 2013 David Shumway
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * Contact: davidshumway@gmail.com
 * 
/*/

// max execution time 60 seconds
//set_time_limit(60);

//scraperwiki::sqliteexecute(
//    "DROP TABLE last_update"
//);
//scraperwiki::sqlitecommit();


// default SQLite table
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY ASC,
        title string,
        requester_id string,
        requester_name string,
        HITs_available int,
        time_posted int,
        time_last_update int,
        job_exists int,
        id_duplicate_jobs int NOT NULL DEFAULT 0,
        on_page_number int
    )"
);

// last updates (by time())
scraperwiki::sqliteexecute(
    "CREATE TABLE IF NOT EXISTS last_update (
        id INTEGER PRIMARY KEY ASC,
        HITs_available int,
        jobs int
    )"
);

//echo scraperwiki::busyTimeout(120000); exit;

//scraperwiki::sqliteexecute(
//    'ALTER TABLE jobs
//    ADD COLUMN on_page_number INT NOT NULL DEFAULT 1'
//);

//scraperwiki::sqliteexecute(
//    'ALTER TABLE jobs
//    ADD COLUMN id_duplicate_jobs INT NOT NULL DEFAULT 0'
//);

//scraperwiki::sqliteexecute(
//    'UPDATE jobs
//    SET
//        id_duplicate_jobs = 1'
//);
                    
//scraperwiki::sqliteexecute(
//    'INSERT INTO last_update (id, jobs, HITs_available)
//        VALUES (1, 0, 0)'
//);

// execute
scraperwiki::sqlitecommit();// exit;
    
// Example URLs to load (pages 2, 3)
//searchWords=&selectedSearchType=hitgroups&sortType=NumHITs%3A1&pageNumber=2&searchSpec=HITGroupSearch%23T%231%2310%23-1%23T%23%21%23%21NumHITs%211%21%23%21
//searchWords=&selectedSearchType=hitgroups&sortType=NumHITs%3A1&pageNumber=3&searchSpec=HITGroupSearch%23T%232%2310%23-1%23T%23%21%23%21NumHITs%211%21%23%21

// Search page 1 url to load
$url_string = 'https://www.mturk.com/mturk/viewhits?searchWords=&selectedSearchType=hitgroups&sortType=NumHITs%3A1&pageNumber=1&searchSpec=HITGroupSearch%23T%232%2310%23-1%23T%23%21%23%21NumHITs%211%21%23%21';

// NOT USING--database_ids_array: array of database ids to not delete from database
//$database_ids_array = new Array();

// number pages to scrape (depth)
$np = 14;

// debug
$last__ = '';

//
$runs = 800;

//
$countrn = 0;

// variable whether any jobs have changed since last run
$jobs_are_modified = true;

// number completed pages
$count_pages_complete = 0;
    
while ($countrn < $runs) {
    
    // TODO: is a run required?/continue
    
    // set all jobs to non-existent
    if ($jobs_are_modified && $count_pages_complete == $np) {
        scraperwiki::sqliteexecute(
            'UPDATE jobs
            SET
                job_exists = 0'
        );
        scraperwiki::sqlitecommit();
        
        // reset this
        $jobs_are_modified = false;
    }
    
    // number completed pages (reset)
    $count_pages_complete = 0;
    
    // duplicate jobs array
    $duplicate_jobs_array = array();

    // loop through the search pages
    for ($i = 1; $i <= $np; $i++) {
        
        // change url string to next page
        $url_string = preg_replace('/pageNumber=\d+/', 'pageNumber='.$i, $url_string);
        
        // download page
        $html_content = scraperwiki::scrape($url_string);
        //if ($html_content == $last__) {
        //    echo 'x'; exit;
        //} else $last__ = $html_content;
        
        $html_content = str_replace("\n", "", $html_content);
        
        //>using regex - DOM is commented out below
        
        // preg string
        $preg = '/<a class="capsulelink" href="#" id="capsule(?:.+?)">(.+?)<\/a>(?:.+?)<a href="\/mturk\/searchbar\?selectedSearchType=hitgroups&amp;requesterId=([^&"]+)[^"]{0,}">(.+?)<\/a>(?:.+?)number_of_hits(?:.+?)(\d{2,8})/';
        
        // match all
        preg_match_all($preg, $html_content, $matches);
        
        // HIT title
        // Requester ID
        // Requester Name
        // HITs available (8 digits max for HITs available, i.e. 99,999,999)
        
        // ..
        $m = $matches;
        
        // count
        $c = 0;
        
        //
        if (isset($m) && count($m[1]) == 10) {
            
        //!    duplicate title, requester id/name (w/ no groupid) (ie 6 dups == 114 rather than 120 results)
        //!    TODO: duplicate jobs do not add/delete properly (by time posted). i.e. id_duplicate_jobs is interchangeable between duplicate jobs.
            
            foreach ($m[1] as $k => $title) {
                
                $t        = trim($title);    // title
                $rid    = $m[2][$c];    // requester id
                $rn        = $m[3][$c];    // requester name
                $h        = $m[4][$c];    // number of HITs [digit(s)]
                
                $key = $t.$rid.$rn.'';
                
                if (isset($duplicate_jobs_array[$key])) { // #misses "NULL"
                //if (array_key_exists($key, $duplicate_jobs_array)) { // higher cpu load
                    
                    $duplicate_jobs_array[$key]++;
                } else
                    $duplicate_jobs_array[$key] = 0;
                
                // is job in database?
                $res = scraperwiki::select('id FROM jobs
                        WHERE
                            title                = "'.sqlite_escape_string($t).'" AND
                            requester_id        = "'.sqlite_escape_string($rid).'" AND
                            requester_name        = "'.sqlite_escape_string($rn).'" AND
                            id_duplicate_jobs    = '.sqlite_escape_string($duplicate_jobs_array[$key]).'
                        LIMIT 1
                ');
                
                // job is in database
                if (count($res) > 0) {
                    
                    // update job's HITs_available
                    scraperwiki::sqliteexecute(
                        'UPDATE jobs
                        SET
                            HITs_available        = '.$h.',
                            time_last_update    = '.time().',
                            job_exists            = 1,
                            on_page_number        = '.$i.'
                        WHERE
                            id = '.$res[0]['id']
                    );
                    //overwrites
                    /*scraperwiki::save_sqlite(
                            array(),
                            array(
                                "id"                => ,
                                "HITs_available"     => $h,
                                "exists"            => 1
                            ),
                            'm'
                    );*/
                }
                // else job is not in database
                else
                {
                    
                    // update jobs are modified
                    $jobs_are_modified = true;
                    
                    // insert new job
                    scraperwiki::sqliteexecute('
                        INSERT INTO jobs (title, requester_id, requester_name, HITs_available, time_posted, time_last_update, job_exists, id_duplicate_jobs, on_page_number)
                        VALUES (
                            "'.sqlite_escape_string($t).'",
                            "'.sqlite_escape_string($rid).'",
                            "'.sqlite_escape_string($rn).'",
                            '.$h.',
                            '.time().',
                            '.time().',
                            1,
                            '.sqlite_escape_string($duplicate_jobs_array[$key]).',
                            '.$i.'
                        )
                        
                    ');
                    /*scraperwiki::save_sqlite(
                            array(),
                            array(
                                "title"                => sqlite_escape_string($t),
                                "requester_id"        => sqlite_escape_string($rid),
                                "requester_name"    => sqlite_escape_string($rn),
                                "HITs_available"    => $h,
                                "time_posted"        => time(),
                                "time_last_update"    => time(),
                                "job_exists"        => 1
                            ),
                            'jobs'
                    );*/
                }
                
                // increment preg count
                $c++;
            }
            
            // increment pages complete
            // pages complete++ occurs when a page has
            // 10 matches
                
            $count_pages_complete++;
        }
        // sleep 1 second and continue
        //sleep(1);
    }
    
    // End of looped pages.
    // Commit now only if jobs are modified, this will update job_exists fields before purge.
    
    if ($jobs_are_modified) {
        
        // update last_update table (2 fields)
        scraperwiki::sqliteexecute(
            'UPDATE last_update
            SET
                HITs_available        = '.time().',
                jobs                = '.time().'
            WHERE
                id = 1'
        );
    }
    // else update HITs_available
    else
    {
        
        // update last_update table (1 field)
        scraperwiki::sqliteexecute(
            'UPDATE last_update
            SET
                HITs_available        = '.time().'
            WHERE
                id = 1'
        );
    }
    
    // execute
    scraperwiki::sqlitecommit();
        
    // wait some to finish SQL above. Wait xx1 minutexx 2 minutes.
    sleep(100);
        
    // delete old
    // only when completed pages is max (all complete)
    
    if ($jobs_are_modified && $count_pages_complete == $np) {
        
        // delete old jobs
        scraperwiki::sqliteexecute(
            'DELETE FROM jobs
            WHERE
                job_exists = 0'
        );
        
        // save above
        scraperwiki::sqlitecommit();
    }
    
    // increment
    $countrn++;
    
    // debug
    //echo $jobs_are_modified."\r\n";
    //echo $count_pages_complete."\r\n";
    //echo $np."\r\n";
    //echo time()."\r\n";
    
    // sleep 1 more minute
    sleep(20);
}

//https://scraperwiki.com/scrapers/toronto_-_call_docs_-_purchasers
function sqlite_escape_string($a) {
    $a = preg_replace("/'/","''",$a);
    return $a;
}
?>