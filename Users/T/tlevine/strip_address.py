import re
def strip_address(text):
    return re.sub(r'\s+', ' ', re.sub(r'[\n\r]+', '\n', text.strip()).replace(',\n', ', ').replace('\n', ', '))