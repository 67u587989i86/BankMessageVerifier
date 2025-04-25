import re

def check_links(text):
    urls = re.findall(r'http[s]?://\S+', text)
    suspicious = [url for url in urls if "bit.ly" in url or "tinyurl" in url]
    return suspicious
