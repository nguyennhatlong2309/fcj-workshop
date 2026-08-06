import urllib.request
import re

try:
    html = urllib.request.urlopen('http://localhost:1313/fcj-workshop/vi/').read().decode('utf-8')
    hrefs = re.findall(r'href="([^"]*)"', html)
    for h in hrefs:
        if '5-workshop' in h or '5-Workshop' in h:
            print("FOUND LINK:", h)
except Exception as e:
    print("ERROR:", e)
