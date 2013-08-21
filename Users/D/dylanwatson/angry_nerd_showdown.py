import scraperwiki

sourcescraper = 'angry_nerd_tally'
scraperwiki.sqlite.attach(sourcescraper)

totalQuery = "select total from " + sourcescraper + ".team_members"
lukeTotalQuery = "select total from " + sourcescraper + ".team_members where LOWER(name) LIKE '%luke%'"
dylanTotalQuery = "select total from " + sourcescraper + ".team_members where LOWER(name) LIKE '%dylan%'"

# Includes Exceptions for poorly formed heals
dylanHealQuery = "select amount, message from " + sourcescraper + ".donations where LOWER(message) LIKE '%heal%' AND LOWER(message) LIKE '%dylan%' OR name LIKE '%Dag%'"
lukeHealQuery = "select amount, message from " + sourcescraper + ".donations where LOWER(message) LIKE '%heal%' AND LOWER(message) LIKE '%luke%'"

def calculateTotal(query):
    total = 0
    heals  = scraperwiki.sqlite.execute(query)['data']
    for heal in heals:
        total += float(heal[0])
    return total

lukeHeals = calculateTotal(lukeHealQuery)
dylanHeals = calculateTotal(dylanHealQuery)
lukeTotal = calculateTotal(lukeTotalQuery)
dylanTotal = calculateTotal(dylanTotalQuery)
teamTotal = calculateTotal(totalQuery)

lukeHurt = lukeTotal - lukeHeals
dylanHurt = dylanTotal - dylanHeals

print '''
<html>
<head>
<title>Angry Nerd 'Hurt or Heal' Showdown</title>
<meta http-equiv="x-ua-compatible" content="IE=7,chrome=1">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

<script>'''
print 'var dylanHurt = ' + str(dylanHurt) + ';'
print 'var dylanHeal = ' + str(dylanHeals) + ';'

print 'var lukeHurt = ' + str(lukeHurt) + ';'
print 'var lukeHeal = ' + str(lukeHeals) + ';'

print 'var total = ' + str(teamTotal) + ';'

print '''
var dylanNet = dylanHeal - dylanHurt;
var lukeNet = lukeHeal - lukeHurt;


$(document).ready(function() {
    doResize();
    setupTooltips();
});

$(window).resize(function() {
    doResize();
});

function doResize() {
    
    var dylanHurtHeight = getDistance(dylanHurt, total);
    var lukeHurtHeight = getDistance(lukeHurt, total);
    
    var dylanHealHeight = getDistance(dylanHeal, total);
    var lukeHealHeight = getDistance(lukeHeal, total);
    
    var dylanNetHeight = getDistance(dylanNet, total);
    var lukeNetHeight = getDistance(lukeNet, total);
    
    var delay = 500;
    var duration = 1000;
    
    $('.dylan.green').delay(delay).animate({ height: dylanHealHeight + 'px'}, { duration : duration, queue: true });
    $('.luke.green').delay(delay).animate({ height: lukeHealHeight + 'px'}, { duration : duration, queue: true });
    
    $('.dylan.red').delay(delay).animate({ height: dylanHurtHeight + 'px'}, { duration : duration, queue: true });
    $('.luke.red').delay(delay).animate({ height: lukeHurtHeight + 'px'}, { duration : duration, queue: true });
    
    $('.dylan.white').delay(delay).animate({ bottom: dylanNetHeight + 'px'}, { duration : duration, queue: true });
    $('.luke.white').delay(delay).animate({ bottom: lukeNetHeight + 'px'}, { duration : duration, queue: true });
        
    $('.dylan.images').delay(delay).animate({ bottom: dylanNetHeight + 'px'}, { duration : duration, queue: true });
    $('.luke.images').delay(delay).animate({ bottom: lukeNetHeight + 'px'}, { duration : duration, queue: true });
    
    $('.dylan.text').delay(delay).animate({ bottom: dylanNetHeight + 'px'}, { duration : duration, queue: true });
    $('.luke.text').delay(delay).animate({ bottom: lukeNetHeight + 'px'}, { duration : duration, queue: true });

    var textIncrementer = function() {
        $(this).data('count', parseInt($(this).html().replace('$', ''), 0));
        $(this).html('$0');
        countUp(5, '$', $(this));
    }
    
    var totaller = function() {
        $(this).data('count', parseInt($(this).html().replace('Total: $', ''), 0));
        $(this).html('Total: $0');
        countUp(1, 'Total: $', $(this));
    }    
    
    var textDecrementer = function() {
        $(this).data('count', parseInt($(this).html().replace('$', ''), 0));
        $(this).html('$0');
        countDown(5, '$', $(this));
    }
    
    $('.dylan.text').text(dylanNet + ' pts');
    var dylFunc = dylanNet <= 0 ? textDecrementer : textIncrementer;
    $('.dylan.text').each(dylFunc);
    
    $('.luke.text').text(lukeNet + ' pts');
    var lukeFunc = lukeNet <  0 ? textDecrementer : textIncrementer;
    $('.luke.text').each(lukeFunc);
    
    $('#total').text('Total: $' + total);
    $('#total').each(totaller);
}

function countUp(timeout, prefix, $this){
    var val = $this.html().replace(prefix, '');
    var current = parseInt(val, 0);
    if(current < parseInt($this.data('count'))) {
        $this.html(prefix + ++current);
    
        setTimeout(function(){countUp(timeout, prefix, $this);}, timeout);
    }
}

function countDown(timeout, prefix, $this){
    var val = $this.html().replace(prefix, '');
    var current = parseInt(val, 0);
    if(current > parseInt($this.data('count'))) {
        $this.html(prefix + --current);
        setTimeout(function(){countDown(timeout, prefix, $this);}, timeout);
    }
}

function calcHeight() {
    var body = document.body,
        html = document.documentElement;
    var height = Math.max( body.scrollHeight, body.offsetHeight, 
                           html.clientHeight, html.scrollHeight, html.offsetHeight );
    return height;
}

function getDistance(player, total) {
    var ratio = ( player / total );
    var totalHeight = calcHeight();
    var usableHeight = totalHeight - (totalHeight * 0);
    
    var distance =  usableHeight * ratio;
    return distance;    
}

function setupTooltips(){
    $('.dylan.green').attr('title', 'Healed: $' + dylanHeal);
    $('.luke.green').attr('title', 'Healed: $' + lukeHeal);
    
    $('.dylan.red').attr('title', 'Hurt: $' + dylanHurt);
    $('.luke.red').attr('title', 'Hurt: $' + lukeHurt);
    
    if(dylanNet == lukeNet) {
        $('#dylanholder .images').attr('title', "It's currently a tie! Perhaps they'll both don the tutu?");
        $('#lukeholder .images').attr('title', "It's currently a tie! Perhaps they'll both don the tutu?");
        $('#dylanholder .tiara').show();
        $('#lukeholder .tiara').show();
    } else if (dylanNet < lukeNet) {
        $('#dylanholder .images').attr('title', 'Dylan is currently the princess!');
        $('#lukeholder .images').attr('title', 'Donate "Hurt Luke" to make sure HE wears the tutu for Tough Mudder!');
        $('#dylanholder .tiara').show();
        $('#lukeholder .tiara').hide();
    } else {
        $('#dylanholder .images').attr('title', 'Donate "Hurt Dylan" to make sure HE wears the tutu for Tough Mudder!');
        $('#lukeholder .images').attr('title', 'Luke is currently the princess!');    
        $('#dylanholder .tiara').hide();
        $('#lukeholder .tiara').show();
    }
    //$(document).tooltip();
    
    var targets = $( '[title]' ),
        target  = false,
        tooltip = false;
 
            targets.bind( 'mouseenter', function()
            {
                target    = $( this );
                tip        = target.attr( 'title' );
                tooltip    = $( '<div id="tooltip"></div>' );

                if( !tip || tip == '' )
                    return false;

                target.removeAttr( 'title' );
                tooltip.css( 'opacity', 0 )
                       .html( tip )
                       .appendTo( 'body' );

                var init_tooltip = function()
                {
                    if( $( window ).width() < tooltip.outerWidth() * 1.5 )
                        tooltip.css( 'max-width', $( window ).width() / 2 );
                    else
                        tooltip.css( 'max-width', 340 );

                    var pos_left = target.offset().left + ( target.outerWidth() / 2 ) - ( tooltip.outerWidth() / 2 ),
                        pos_top     = target.offset().top - tooltip.outerHeight() - 20;

                    if( pos_left < 0 )
                    {
                        pos_left = target.offset().left + target.outerWidth() / 2 - 20;
                        tooltip.addClass( 'left' );
                    }
                    else
                        tooltip.removeClass( 'left' );

                    if( pos_left + tooltip.outerWidth() > $( window ).width() )
                    {
                        pos_left = target.offset().left - tooltip.outerWidth() + target.outerWidth() / 2 + 20;
                        tooltip.addClass( 'right' );
                    }
                    else
                        tooltip.removeClass( 'right' );

                    if( pos_top < 0 )
                    {
                        var pos_top     = target.offset().top + target.outerHeight();
                        tooltip.addClass( 'top' );
                    }
                    else
                        tooltip.removeClass( 'top' );

                    tooltip.css( { left: pos_left, top: pos_top } )
                           .animate( { top: '+=10', opacity: 1 }, 50 );
                };

                init_tooltip();
                $( window ).resize( init_tooltip );

                var remove_tooltip = function()
                {
                    tooltip.animate( { top: '-=10', opacity: 0 }, 50, function()
                    {
                        $( this ).remove();
                    });

                    target.attr( 'title', tip );
                };

                target.bind( 'mouseleave', remove_tooltip );
                tooltip.bind( 'click', remove_tooltip );
            });
}
</script>
<style>
/* $$$$$$$$$$$$$$ Pre Existing ##############*/
.fullscreen {
    left: 0;
    bottom: 0;
    width:100%;
    margin: 0px;
    background: #04647f url('http://farm4.staticflickr.com/3758/9140420907_583f8032e2_o_d.png') repeat-x;
    background-position: 0% 100%;
    background-size: 100% auto;
}

.centre {
  margin-left: auto;
  margin-right: auto;
}

.red {
background: #cc0000; /* Old browsers */
background: -moz-linear-gradient(left,  #cc0000 0%, #680600 100%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, right top, color-stop(0%,#cc0000), color-stop(100%,#680600)); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(left,  #cc0000 0%,#680600 100%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(left,  #cc0000 0%,#680600 100%); /* Opera 11.10+ */
background: -ms-linear-gradient(left,  #cc0000 0%,#680600 100%); /* IE10+ */
background: linear-gradient(to right,  #cc0000 0%,#680600 100%); /* W3C */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#cc0000', endColorstr='#680600',GradientType=1 ); /* IE6-9 */

}

.black {
background: #7d7e7d; /* Old browsers */
background: -moz-linear-gradient(left,  #7d7e7d 0%, #0e0e0e 100%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, right top, color-stop(0%,#7d7e7d), color-stop(100%,#0e0e0e)); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(left,  #7d7e7d 0%,#0e0e0e 100%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(left,  #7d7e7d 0%,#0e0e0e 100%); /* Opera 11.10+ */
background: -ms-linear-gradient(left,  #7d7e7d 0%,#0e0e0e 100%); /* IE10+ */
background: linear-gradient(to right,  #7d7e7d 0%,#0e0e0e 100%); /* W3C */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#7d7e7d', endColorstr='#0e0e0e',GradientType=1 ); /* IE6-9 */
}

.green {
background: rgb(2,165,0); /* Old browsers */
background: -moz-linear-gradient(left,  rgba(2,165,0,1) 0%, rgba(0,110,46,1) 100%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, right top, color-stop(0%,rgba(2,165,0,1)), color-stop(100%,rgba(0,110,46,1))); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(left,  rgba(2,165,0,1) 0%,rgba(0,110,46,1) 100%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(left,  rgba(2,165,0,1) 0%,rgba(0,110,46,1) 100%); /* Opera 11.10+ */
background: -ms-linear-gradient(left,  rgba(2,165,0,1) 0%,rgba(0,110,46,1) 100%); /* IE10+ */
background: linear-gradient(to right,  rgba(2,165,0,1) 0%,rgba(0,110,46,1) 100%); /* W3C */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#02a500', endColorstr='#006e2e',GradientType=1 ); /* IE6-9 */
}

.white {
background: #f5f6f6; /* Old browsers */
background: -moz-linear-gradient(top,  #f5f6f6 0%, #dbdce2 21%, #b8bac6 49%, #dddfe3 80%, #f5f6f6 100%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#f5f6f6), color-stop(21%,#dbdce2), color-stop(49%,#b8bac6), color-stop(80%,#dddfe3), color-stop(100%,#f5f6f6)); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(top,  #f5f6f6 0%,#dbdce2 21%,#b8bac6 49%,#dddfe3 80%,#f5f6f6 100%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(top,  #f5f6f6 0%,#dbdce2 21%,#b8bac6 49%,#dddfe3 80%,#f5f6f6 100%); /* Opera 11.10+ */
background: -ms-linear-gradient(top,  #f5f6f6 0%,#dbdce2 21%,#b8bac6 49%,#dddfe3 80%,#f5f6f6 100%); /* IE10+ */
background: linear-gradient(to bottom,  #f5f6f6 0%,#dbdce2 21%,#b8bac6 49%,#dddfe3 80%,#f5f6f6 100%); /* W3C */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#f5f6f6', endColorstr='#f5f6f6',GradientType=0 ); /* IE6-9 */
}

/*
    TOOLTIP
*/

#tooltip
{
    font-family: Ubuntu, sans-serif;
    font-size: 0.875em;
    text-align: center;
    text-shadow: 0 1px rgba( 0, 0, 0, .5 );
    line-height: 1.5;
    color: #fff;
    background: #333;
    background: -webkit-gradient( linear, left top, left bottom, from( rgba( 0, 0, 0, .6 ) ), to( rgba( 0, 0, 0, .8 ) ) );
    background: -webkit-linear-gradient( top, rgba( 0, 0, 0, .6 ), rgba( 0, 0, 0, .8 ) );
    background: -moz-linear-gradient( top, rgba( 0, 0, 0, .6 ), rgba( 0, 0, 0, .8 ) );
    background: -ms-radial-gradient( top, rgba( 0, 0, 0, .6 ), rgba( 0, 0, 0, .8 ) );
    background: -o-linear-gradient( top, rgba( 0, 0, 0, .6 ), rgba( 0, 0, 0, .8 ) );
    background: linear-gradient( top, rgba( 0, 0, 0, .6 ), rgba( 0, 0, 0, .8 ) );
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    border-top: 1px solid #fff;
    -webkit-box-shadow: 0 3px 5px rgba( 0, 0, 0, .3 );
    -moz-box-shadow: 0 3px 5px rgba( 0, 0, 0, .3 );
    box-shadow: 0 3px 5px rgba( 0, 0, 0, .3 );
    position: absolute;
    z-index: 100;
    padding: 15px;
}
#tooltip:after
{
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 10px solid #333;
    border-top-color: rgba( 0, 0, 0, .7 );
    content: '';
    position: absolute;
    left: 50%;
    bottom: -10px;
    margin-left: -10px;
}
#tooltip.top:after
{
    border-top-color: transparent;
    border-bottom: 10px solid #333;
    border-bottom-color: rgba( 0, 0, 0, .6 );
    top: -20px;
    bottom: auto;
}
#tooltip.left:after
{
    left: 10px;
    margin: 0;
}
#tooltip.right:after
{
    right: 10px;
    left: auto;
    margin: 0;
}

/* $$$$$$$$$$$$$$ New ##############*/

#title {
    width: 100%;
    height: 20%;
    position:fixed;
}

#top {
    width: 100%;
    height: 50%;
    position:relative;
}

#bottom {
    width: 100%;
    height: 50%;
    position:relative;
}

.text {
    color: white;
    font-size: 150%;
    font-weight: bold;
    text-shadow: 2px 2px 1px #151515;
}
</style>

<body class="fullscreen">
    <img title="Nedlands Angry Nerds ~ Hurt and Heal" style=" position:fixed; max-height:17%; max-width: 60%; top:2%; left:2%;" src="http://farm8.staticflickr.com/7386/9142654722_5808ac17ef_o_d.png" />
    <div id="top">
        <div id="dylanholder" style="height:100%; width: 10%; bottom: 0px; position:absolute; left: 52%;">
          <div class="dylan green" style="height: 1px; width: 50%; bottom: 0px; position:absolute; left: 0;"></div>
          <div class="dylan white" style="height: 2px; width: 50%; position:absolute; bottom: 0px; right: 0;"></div>
          <div class="dylan images" style="width: 60%; position: absolute; right: -50%; z-index: 50; bottom: 1px;">
                <img class="tiara" src="http://farm8.staticflickr.com/7403/9142487409_96e70c767e_o_d.png" style="position: absolute; max-width: 100px; width: 50%; right: 0%; top: -10%; display: none;">
                <img class="avatar" src="http://farm8.staticflickr.com/7409/9140407581_77cafa5ce2_o_d.png" style="width: 100%;">
          </div>
          <div class="dylan text" style="position: absolute; bottom: 0; right: 0; z-index: 100;"></div>
        </div>
        <div id="lukeholder" style="height:100%; width: 10%; bottom: 0px; position:absolute; right: 52%;">
          <div class="luke green" style="height: 1px; width: 50%; bottom: 0px; position: absolute; right: 0;"></div>
          <div class="luke white" style="height: 2px; width: 50%; position: absolute; bottom: 1px; left: 0;"></div>
          <div class="luke images" style="width: 60%; position: absolute; left: -50%; z-index: 50; bottom: 1px;">
                <img class="tiara" src="http://farm8.staticflickr.com/7403/9142487409_96e70c767e_o_d.png" style="position: absolute; max-width: 100px; width: 50%; right: 12%; top: -12%;">
                <img class="avatar" src="http://farm3.staticflickr.com/2843/9142640522_15b2d6e42e_o_d.png" style="width: 100%;">
          </div>
          <div class="luke text" style="position: absolute; bottom: 0; z-index: 100;"></div>
        </div>
    </div>
    
    <div id="bottom">
          <div class="dylan red" style="height:1px; width: 5%; top: 0px; position:absolute; left: 52%;"></div>
          <div class="luke red" style="height:1px; width: 5%; top: 0px; position: absolute; right: 52%;"></div>
    </div>
    <div style="position:fixed; width:30%; left: 10; bottom: 2%; color:white;">
        <h3 style="text-shadow: 2px 2px 1px #151515;">Who will don the tutu for Tough Mudder? You decide!</h3>
        <a href="http://www.legacyfundraising.com.au/nedlands_angry_nerds" style="display: inline; " ><h2>Donate Now!</h2></a>
        <img title="In October 2013, a ragtag bunch of Nerds will be gearing up to compete in Tough Mudder, 'Probably the toughest event on the planet'. Our Co-Captains, Luke and Dylan are battling it out raising money for Legacy. Ultimately the loser will be crowned the princess and don a pretty pink tutu for Tough Mudder! Support a nerd now! When donating, state whether you wish to 'Hurt' or 'Heal' and your nerds name. Each dollar you donate will either hurt or heal your nerd for 1 point. As well as helping Legacy and having a laugh, your money will help us decide WHO WILL WEAR THE TUTU!" style="display: inline; width:2em;" src="http://media.cleveland.com/strongsville/photo/question-mark-cd7c056662278be7.png" />
    </div>
    <h2 id="total" style="text-shadow: 2px 2px 1px #151515; position:fixed; bottom: 10px; right: 10px; color:white;"></h2>    
</body>
</html>
'''