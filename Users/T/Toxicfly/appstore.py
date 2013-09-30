import scraperwiki
import string
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/List.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()

for row in reader:
     
     URL = row[0]+'&tab=r'
     html = scraperwiki.scrape(URL)
     scrape_data = scrape("""
    {*
      <span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:postedBy">{{ [mobile].[title1] }}</span></a>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:revSubject">{{ [mobile].[title2] }}</span>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:reviewShortDescription" class="feed-item-text-short-desc multi-line-to-fix">{{ [mobile].[title3] }}</span>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:createdDate">{{ [mobile].[title4] }}</span>
     

    *}
    """, html=html);
    
     data = [{'URL':URL, 'Reviewer':p['title1'][0], 'Headline':p['title2'][0],'content':p['title3'][0], 'Date':p['title4'][0]} for p in scrape_data['mobile']]
    
     scraperwiki.sqlite.save(unique_keys=["Date"], data=data)
import scraperwiki
import string
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/List.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()

for row in reader:
     
     URL = row[0]+'&tab=r'
     html = scraperwiki.scrape(URL)
     scrape_data = scrape("""
    {*
      <span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:postedBy">{{ [mobile].[title1] }}</span></a>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:revSubject">{{ [mobile].[title2] }}</span>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:reviewShortDescription" class="feed-item-text-short-desc multi-line-to-fix">{{ [mobile].[title3] }}</span>

<span id="listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:mostHelpfulPositive:reviewDetails:createdDate">{{ [mobile].[title4] }}</span>
     

    *}
    """, html=html);
    
     data = [{'URL':URL, 'Reviewer':p['title1'][0], 'Headline':p['title2'][0],'content':p['title3'][0], 'Date':p['title4'][0]} for p in scrape_data['mobile']]
    
     scraperwiki.sqlite.save(unique_keys=["Date"], data=data)
