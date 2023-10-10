import ssl
import urllib.request

def get_html(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_a4a3b5b0-zone-test_unlocker:4197l1fnslrm@brd.superproxy.io:22225'}))
    response = opener.open(url)

    response_headers = response.info()
    content_type = response_headers.get('Content-Type')
    encoding = 'utf-8'  

    if content_type:
        content_type_parts = content_type.split(';')
        for part in content_type_parts:
            if 'charset=' in part:
                encoding = part.split('charset=')[-1].strip()
    html_string = response.read().decode(encoding)
    return html_string
