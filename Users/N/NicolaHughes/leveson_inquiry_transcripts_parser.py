import scraperwiki
import re

scraperwiki.sqlite.attach("leveson_inquiry_transcripts_urls")
scraper = scraperwiki.sqlite.select("Transcription, URL from leveson_inquiry_transcripts_urls.swdata")
for info in scraper:

    transcript = info['Transcription']
    URL = info['URL']
    title = URL.split('/')[-1]
    transcript_parsed = re.sub("\d+\s{0,3}", "", transcript).replace('\n\r','').replace('(.pm)', '').replace('Thursday, December (.am)', '')
    # Replace \n\r because we really want \r\n\r\n but that will remove too many
    # and so we will replace the middle two chars leaving ... \r\n ;)
    data = {'URL': URL, 'Title': title, 'Text': transcript_parsed}
    scraperwiki.sqlite.save(['URL'], data)import scraperwiki
import re

scraperwiki.sqlite.attach("leveson_inquiry_transcripts_urls")
scraper = scraperwiki.sqlite.select("Transcription, URL from leveson_inquiry_transcripts_urls.swdata")
for info in scraper:

    transcript = info['Transcription']
    URL = info['URL']
    title = URL.split('/')[-1]
    transcript_parsed = re.sub("\d+\s{0,3}", "", transcript).replace('\n\r','').replace('(.pm)', '').replace('Thursday, December (.am)', '')
    # Replace \n\r because we really want \r\n\r\n but that will remove too many
    # and so we will replace the middle two chars leaving ... \r\n ;)
    data = {'URL': URL, 'Title': title, 'Text': transcript_parsed}
    scraperwiki.sqlite.save(['URL'], data)