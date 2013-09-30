import scraperwiki
# Blank Python
# http://arshaw.com/scrapemark/
# sample 1 not working
import scrapemark
# sample 1.1 semi-fixed
print scrapemark.scrape("""
{*
<div class="story-item-details">
<h3 class="story-item-title">
<a target="_blank" href="{{ [links].url }}">{{ [links].title }}</a>
</h3>
<p class="story-item-description">
<a class="story-item-teaser" href="{{ [story-item-teaser].url }}">{{ [story-item-teaser].title }}</a>
<a href="{{ [crawl4link].url }}" class="crawl4link">{{ [View-in-Crawl] }}</a>
</p>
*}
""",
url='http://digg.com/'
)
scraperwiki.sqlite.commit()

import scraperwiki
# Blank Python
# http://arshaw.com/scrapemark/
# sample 1 not working
import scrapemark
# sample 1.1 semi-fixed
print scrapemark.scrape("""
{*
<div class="story-item-details">
<h3 class="story-item-title">
<a target="_blank" href="{{ [links].url }}">{{ [links].title }}</a>
</h3>
<p class="story-item-description">
<a class="story-item-teaser" href="{{ [story-item-teaser].url }}">{{ [story-item-teaser].title }}</a>
<a href="{{ [crawl4link].url }}" class="crawl4link">{{ [View-in-Crawl] }}</a>
</p>
*}
""",
url='http://digg.com/'
)
scraperwiki.sqlite.commit()

