<?php
# Blank PHP
$sourcescraper = 'nhschoicesorgscraper';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from ".$sourcescraper.".swdata 
    order by title desc limit 100"
);
foreach($data as $gp){ ?>
    <div class="table">
        <h2><?php echo($gp["title"]); ?></h2>
        <p class="address"><?php echo($gp["address"]); ?></p>
        <?php if($gp["ratings"] !== "No data available"){ ?>
        <p class="rating"><?php echo($gp["percentwouldrecommend"]); ?>% of patients would recommend (based on <?php echo($gp["ratings"]); ?> ratings)</p>
<?php } ?>
    </div>
<?php }
?><?php
# Blank PHP
$sourcescraper = 'nhschoicesorgscraper';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from ".$sourcescraper.".swdata 
    order by title desc limit 100"
);
foreach($data as $gp){ ?>
    <div class="table">
        <h2><?php echo($gp["title"]); ?></h2>
        <p class="address"><?php echo($gp["address"]); ?></p>
        <?php if($gp["ratings"] !== "No data available"){ ?>
        <p class="rating"><?php echo($gp["percentwouldrecommend"]); ?>% of patients would recommend (based on <?php echo($gp["ratings"]); ?> ratings)</p>
<?php } ?>
    </div>
<?php }
?>