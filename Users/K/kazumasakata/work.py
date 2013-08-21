import scraperwiki
import re

html =scraperwiki.scrape('http://chouseisan.com/schedule/List?h=1188bed8c6b0b30c4002d34ea6e2c013')


# 必要部分を取得
#b1 = re.findall('<div class="entry">.*<div id="edit_delete" style="display:none">', html,re.DOTALL)
#b2 = re.findall('<td valign="top" style="border-bottom:1px solid #ddd">.*</a></td>',html)

b2 = re.match(r'<a href=.*>.*</a>',html)

print b2


    
