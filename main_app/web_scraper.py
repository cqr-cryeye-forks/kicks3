# web_scraper.py

import requests
import re
from urllib.parse import urljoin, unquote
from .constants import REGJS, REGS3
import kickdomain

def finds3(sitelist, cookies='', sub=False):
    bucket = []
    if not isinstance(sitelist, list):
        sitelist = [sitelist]
    for targetsite in sitelist:
        try:
            if sub:
                subdomains = kickdomain.getSubdomains(targetsite)
                targetsite_list = [targetsite] + subdomains
            else:
                targetsite_list = [targetsite]
            for target in targetsite_list:
                if not target.startswith('http'):
                    target = f'http://{target.strip()}'
                html = ''
                try:
                    headers = {"Cookie": cookies} if cookies else {}
                    response = requests.get(target, headers=headers, timeout=10)
                    html = unquote(response.text)
                except:
                    pass
                js = re.findall(REGJS, html)
                s3 = re.findall(REGS3, html)
                bucket.extend(s3)
                for i in js:
                    if i.startswith('//'):
                        jsurl = f'http:{i}'
                    elif i.startswith('http'):
                        jsurl = i
                    else:
                        jsurl = urljoin(target, i)
                    try:
                        headers = {"Cookie": cookies} if cookies else {}
                        jsfile = requests.get(jsurl, timeout=10, headers=headers).text
                        s3 = re.findall(REGS3, jsfile)
                        bucket.extend(s3)
                    except:
                        pass
        except:
            pass
    if not bucket:
        return ['Bucket not found']
    return bucket