import json
import scraperwiki
import lxml.html

# to index comments for all articles on the tag use the following instead:
site = 'http://content.guardianapis.com//commentisfree/joris-luyendijk-banking-blog.json?show-fields=all&show-tags=all&page-size=50&order-by=newest'

# to index comments for all articles on the tag in the last thirty days use:
#site = 'http://content.guardianapis.com//commentisfree/joris-luyendijk-banking-blog?format=json&show-fields=all&show-tags=all&page-size=50&order-by=newest&date-id=date%2Flast30days'



def get_content_list_json(page_num):
    return json.loads( scraperwiki.scrape( '%s&page=%s' % (site, page_num) ) )['response']

def get_lxml(url):
    return lxml.html.fromstring( scraperwiki.scrape( url ) )

def get_comments_page_lxml(blog_url):
    return get_lxml( blog_url + '?commentpage=all' )

def get_num_comments(comments_page):
    # interactives, videos, etc don't have comments
    num_comments = 0
    for comments_preamble in comments_page.cssselect( 'form#sort-comments' ):
        comments_preamble_text = comments_preamble.cssselect( 'p' )[0].text_content().strip()
        num_comments = comments_preamble_text.partition(' ')[0]
    return num_comments




# use Content API to list blogs to scrape comments for
content_list_page_num = 1
content_list = get_content_list_json( content_list_page_num )

content_list_total_pages = content_list['pages']

while content_list_page_num <= content_list_total_pages:
    print 'Scraping Content API index page %s of %s' % (content_list_page_num, content_list_total_pages)

    for page in content_list['results']:
        blog_url = page['webUrl']
        blog_date = page['webPublicationDate']
        blog_title = page['webTitle']

        print '%s' % blog_title

        comments_page = get_comments_page_lxml( blog_url )
        num_comments = get_num_comments( comments_page )

        print '#comments: %s' % num_comments

        # scrape individual comments
        comment_number = 0
        for comment in comments_page.cssselect( 'ul.comment' ):
            comment_number += 1

            comment_date = comment.cssselect( 'p.date' )[0].text_content()
            commentor = comment.cssselect( 'div.profile' )[0].cssselect( 'a' )[0].text_content()

            # may really prefer html to .text_content() here...
            comment_body = comment.cssselect( 'div.comment-body' )[0].text_content()

            # responses are not available for moderated comments
            comment_responses = '0'
            for comment_response in comment.cssselect('li.reply'):
                comment_response_text = comment_response.text_content().strip()
                # looks like 'Responses (123)'
                comment_responses = comment_response_text.partition( '(' )[2].replace( ')' , "" )

            # recommedations are not available for moderated comments
            comment_recommendations = '0'
            for recommendations in comment.cssselect('span.recommended'):
                comment_recommendations = recommendations.text_content()

            data = {
                'blog_url': blog_url,
                'comment_number': comment_number,
                'blog_date': blog_date,
                'blog_title': blog_title,
                'total_comments' : num_comments,
                'comment_date' : comment_date,
                'commentor': commentor,
                'comment_body': comment_body,
                'comment_responses': comment_responses,
                'comment_recommendations': comment_recommendations
            }

            scraperwiki.sqlite.save( ['blog_url', 'comment_number'], data, table_name='blog' )


    # update for next loop iteration without error for out of bounds page index
    content_list_page_num += 1
    if content_list_page_num <= content_list_total_pages:
        content_list = get_content_list_json( content_list_page_num )
