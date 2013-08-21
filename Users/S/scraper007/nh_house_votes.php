<?php
    $sourcescraper = 'nh_gencourt_votes';
    scraperwiki::attach('nh_gencourt_votes');
    $data = scraperwiki::select(
        "* from nh_gencourt_votes.bill_votes 
         order by 
             substr(date_of_vote, 7) || substr(date_of_vote, 1, 2) || substr(date_of_vote, 4, 2) desc, 
             cast(vote_num as int) desc
        "
    );
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- http://twitter.github.com/bootstrap/base-css.html -->
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/js/bootstrap.min.js"></script>
    <style>
        th {
            white-space: nowrap;
        }
    </style>
</head>
<body>
    <div class="container">
    <div class="page-header"><h1>NH House Bills</h1></div>
    <div class="row">
        <div class="span12">
            <table class="table table-striped table-bordered table-hover table-condensed">
                <tr>
                    <th>Date of Vote</th>
                    <th>Vote #</th>
                    <th>Bill #</th>
                    <th>Bill Title</th>
                    <th>Question/Motion</th>
                    <th>Yeas</th>
                    <th>Nays</th>
                </tr>
                <?php
                    foreach ($data as $d) {
                        print '<tr>';
                        print '<td>' . $d['date_of_vote'] . '</td>';
                        print '<td>' . $d['vote_num'] . '</td>';
                        print '<td>' . $d['bill_num'] . '</td>';
                        print '<td>' . $d['bill_title'] . '</td>';
                        print '<td>' . $d['question_or_motion'] . '</td>';
                        print '<td>' . $d['yeas'] . '</td>';
                        print '<td>' . $d['nays'] . '</td>';
                        print '</tr>';
                    }
                ?>
            </table>
        </div>
    </div>
    </div>
</body>
</html>