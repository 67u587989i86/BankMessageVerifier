import re

def check_links(text):
    # Find all URLs starting with http:// or https://
    urls = re.findall(r'http[s]?://\S+', text)

    # Define trusted domains
    trusted_domains = ["www.hdfc.com", "www.sbi.com"]

    # Mark as suspicious if they are shortened links and not trusted
    suspicious = [
        url for url in urls
        if ("bit.ly" in url or "tinyurl" in url) and not any(trusted in url for trusted in trusted_domains)
    ]

    return suspicious
