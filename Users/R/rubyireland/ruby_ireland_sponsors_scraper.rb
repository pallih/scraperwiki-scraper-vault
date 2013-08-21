require 'scraperwiki'
require 'active_support'
require 'nokogiri'

# Okay, from some reason, we don't seem to receive the div's we are interested in.
# Not sure why, so we use the example input below, which is also useful to test the code

def get_doc_from_example_input
  example_input = %^

<ul class="dividedList">

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="http://www.sageone.com" target="_blank"><img src="http://photos1.meetupstatic.com/photos/sponsor/c/8/e/8/iab120x90_1731432.jpeg"></a>

</div>

<h5>

<a href="http://www.sageone.com" target="_blank">Sage One</a>

</h5>

<p>Ruby Ireland meetup host and meetup sponsor</p>

</li>

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="http://engineyard.com" target="_blank"><img src="http://photos4.meetupstatic.com/photos/sponsor/e/7/7/4/iab120x90_1379252.jpeg"></a>

</div>

<h5>

<a href="http://engineyard.com" target="_blank">Engine Yard</a>

</h5>

<p>A welcoming host for Ruby Ireland meetups over craft beers at our HQ</p>

</li>

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="https://www.intercom.io/" target="_blank"><img src="http://photos3.meetupstatic.com/photos/sponsor/8/5/c/2/iab120x90_1534242.jpeg"></a>

</div>

<h5>

<a href="https://www.intercom.io/" target="_blank">Intercom</a>

</h5>

<p>We're delighted to sponsor Ruby Ireland at meetup.com &amp; host meetups</p>

</li>

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="http://www.sumup.ie/" target="_blank"><img src="http://photos2.meetupstatic.com/photos/sponsor/3/8/6/iab120x90_1620902.jpeg"></a>

</div>

<h5>

<a href="http://www.sumup.ie/" target="_blank">SumUp</a>

</h5>

<p>Ruby Ireland meetup host and food/drinks sponsor.</p>

</li>

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="http://www.zendesk.com" target="_blank"><img src="http://photos4.meetupstatic.com/photos/sponsor/d/3/7/e/iab120x90_1494142.jpeg"></a>

</div>

<h5>

<a href="http://www.zendesk.com" target="_blank">Zendesk</a>

</h5>

<p>Sponsor of Ruby Ireland meetups</p>

</li>

<li class="wrapNice">

<div class="D_sponsorImage rounded-all">

<a href="http://www.jetbrains.com/" target="_blank"><img src="http://photos4.meetupstatic.com/photos/sponsor/1/5/5/6/iab120x90_1565462.jpeg"></a>

</div>

<h5>

<a href="http://www.jetbrains.com/" target="_blank">JetBrains</a>

</h5>

<p>Cross-platform Rails IDE with smart Ruby code completion and refactoring</p>

</li>

</ul>
^
  Nokogiri::HTML(example_input)
end




=begin
def get_doc_from_example_input
  example_input = %^
<div id="module_73710552" class="module_slot sponsors">
<div id="modbox_73710552" class="D_box newBox D_sponsors M_sponsorship_badge">
<div class="D_boxhead">
<h2 class="D_dropdown">
<button id="settingsCog-73710552" class="cog settings-cog D_dropdownToggler D_dropdownParent"><span></span></button>
<ul class="D_dropdownContent jsStartHidden cog-menu D_dropdownRight" id="settingsBg-73710552">
<li>
<a href="http://www.meetup.com/rubyireland/sponsors/" class="sprite sprite_action pencil_icon">Edit Sponsors/settings</a>
</li>
<li>
<a href="http://www.meetup.com/rubyireland/manage/settings/sponsors/add/" class="sprite sprite_action add_icon">Add Sponsors</a>
</li>
</ul>   
<a href="http://www.meetup.com/rubyireland/sponsors/" class="bodyColor">
<span class="sponsorModule-head">
Our Sponsors
</span>
</a>
</h2>
</div>
<div class="D_boxsection ">
<div class="sponsorSlot ">
<div class="D_sponsorImage">
<a href="https://www.intercom.io/" target="_blank"><img src="http://photos3.meetupstatic.com/photos/sponsor/8/5/c/2/iab120x90_1534242.jpeg"></a>
</div>
<h4 class="sponsorName">
<a href="https://www.intercom.io/" target="_blank">Intercom</a>
</h4>
<p>We're delighted to sponsor Ruby Ireland at meetup.com &amp; host meetups</p>
</div>
<div class="sponsorSlot ">
<div class="D_sponsorImage">
<a href="http://www.zendesk.com" target="_blank"><img src="http://photos4.meetupstatic.com/photos/sponsor/d/3/7/e/iab120x90_1494142.jpeg"></a>
</div>
<h4 class="sponsorName">
<a href="http://www.zendesk.com" target="_blank">Zendesk</a>
</h4>
<p>Sponsor of Ruby Ireland meetups</p>
</div>
<div class="sponsorSlot last">
<div class="D_sponsorImage">
<a href="http://engineyard.com" target="_blank"><img src="http://photos4.meetupstatic.com/photos/sponsor/e/7/7/4/iab120x90_1379252.jpeg"></a>
</div>
<h4 class="sponsorName">
<a href="http://engineyard.com" target="_blank">Engine Yard</a>
</h4>
<p>A welcoming host for Ruby Ireland meetups over craft beers at our HQ</p>
</div>
</div>
<div class="D_boxfoot ">
<a href="http://www.meetup.com/rubyireland/manage/settings/sponsors/add/" class="D_roundedButton">
Add a Sponsor
</a>
</div>
</div>
</div>                                          
^
  Nokogiri::HTML(example_input)
end
=end


# Bit of a random param
random_param = "#{Time.now.to_i.to_s}=#{Time.now.to_i+1}"


#html = ScraperWiki::scrape("http://www.meetup.com/rubyireland/?#{random_param}")
#doc = Nokogiri::HTML(html)
doc = get_doc_from_example_input

v_ref = nil # to catch the error in the block

sponsor_list = begin
  #doc.css("div.D_sponsors div.D_boxsection div.sponsorSlot").map do |v|
  doc.css("li.wrapNice").map do |v|
    v_ref = v

    {
      name: v.search('a').map(&:inner_text).reject{|item| item == ''}.first,
      url: v.at('a').attribute_nodes.map(&:value).reject{|item| item == '_blank'}.first,
      blurb: v.at('p').inner_text,
      img_url: v.at('a img').attribute_nodes[0].value
    }
  end
rescue
  puts "Error: Looks like the data format has changed or has variances between enumeration...Ensure you have a sponsor name, offering, image and website link added in meetup.com\n\n#{v_ref.inner_html}"
  raise
end

data = {:sponsor_list => sponsor_list.to_json}

puts data

if sponsor_list.empty? 
  puts "Error: did not update. This happens sometimes. It may take 4 or 5 goes :) Or maybe there's no data?"
else
  puts 'Success! Updated!'
  ScraperWiki::sqliteexecute("delete from swdata")
  ScraperWiki::save_sqlite([:sponsor_list], data)
end

