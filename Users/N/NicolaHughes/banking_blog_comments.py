import lxml.html
import urlparse
import scraperwiki
import time
import re
import string

site = 'http://www.guardian.co.uk/commentisfree/joris-luyendijk-banking-blog?page='

# use lxml to gt an object we can look for html stuff in
def get_page_object(url):
    return lxml.html.fromstring( scraperwiki.scrape( url ) )

def is_last_page( obj ):
    # Find the text on the page that looks like x-y of x for .....
    ctnt = obj.cssselect( '.explainer' )[0].text_content().strip()

    # Remove the non-printable characters
    ctnt = ''.join([c for c in ctnt if ord(c) > 31])
    
    # Make sure duplicate spaces are collapsed down to one space
    ctnt = re.sub(' +',' ', ctnt )
    match = re.match( "\d+-(\d+)of (\d+) for", ctnt ).groups(0)

    # If the max page we are viewing is the same as the total, we should finish after this page
    return match[0] == match[1]

last_page = False
count = 1

# Large number, we will break out another way
for pagenum in range(1, 10):
    page = get_page_object( '%s%s' % (site, pagenum) )

    # Check if this is going to be the last page
    if last_page:
        break
    last_page = is_last_page( page )
    if last_page:
        print "This is the last page", pagenum


    offset = 0
    if pagenum == 1:
        offset = 2
    # process some data
    posts = page.cssselect('div.trail-caption')
    for post in posts[offset:]:
        title_link = post.cssselect('div.linktext h3 a')
        if not title_link:
            continue

        count = count + 1
        title = title_link[0].text_content()
        title_link = title_link[0].attrib.get('href')

        obj = post.cssselect('div.trailtext')[0]
        p = obj.cssselect('p')
        if not p:
            continue
        trailtext = p[0].text_content()

        span = obj.cssselect('span.date')
        if not span:
            continue
        date = span[0].text_content().replace(':', '')

        a = obj.cssselect('a')
        if not a:
            continue
        comment_link = a[0].attrib.get('href')

        comment_link = comment_link.replace('#', '?commentpage=all#')        
        # Scrape comments here, make sure you add a field called blog_url to it and set it to
        # title_link
        
        comments_source = get_page_object( comment_link )
        discussion_comments = comments_source.cssselect('ul.comment') #   use # for id, . for class


        for sort_comment_form in comments_source.cssselect('form#sort-comments'):
            num_comments_text = sort_comment_form.cssselect('p')[0].text_content().strip()
            num_comments = re.match('(\d+).*', num_comments_text).groups(1)[0]

        comment_number = 1
        for comment in discussion_comments:
            comments_body = comment.cssselect('div.comment-body')
            for body in comments_body:
                comment_body = body.text_content().strip()

            comment_responses = comment.cssselect('li.reply')
            for comment_response in comment_responses:
                comment_response_text = comment_response.text_content().strip()
                number_responses = re.match('Responses \((\d+)\)', comment_response_text)
                response_count = number_responses.groups(1)[0]

            for recommendations in comment.cssselect('span.recommended'):
                comment_recommendations = recommendations.text_content()

            comment_date = comment.cssselect('p.date')[0].text_content()
            commentor_name = comment.cssselect('div.profile')[0].cssselect('a')[0].text_content()

            data = {
                'article_date': date,
                'comment_date' : comment_date,
                'total_comments' : num_comments,
                'url': title_link,
                'comment_number': comment_number,
                'title': title,
                'body': comment_body,
                'commentor': commentor_name,
                'responses': response_count,
                'recommendations': comment_recommendations
            }

            comment_number += 1

            # Save the blog entry here.
            #print data['url'], data['comment_number']
            scraperwiki.sqlite.save(['url', 'comment_number'], data, table_name='blog')
        
# /Responses \((\d+)\)/.exec("Responses (5)")

#print count