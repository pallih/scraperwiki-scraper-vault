import scraperwiki

def test(company):
    media_list = ["guardian", "telegraph", "bbc", "bskyb", "times", "millbank", "news"]
    return not any(media in company.split(" ") for media in media_list)

print test("the times")
print test("albatross bumpkin")