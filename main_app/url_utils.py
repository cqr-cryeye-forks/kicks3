# url_utils.py

from urllib.parse import urlparse

def remove_duplicate(x):
    return list(dict.fromkeys(x))

def get_bucket_name(urllist):
    b_list = []
    for line in urllist:
        url = line.replace('\/', '/')
        if not url.startswith('http'):
            url = f'http://{url}'
        parsed = urlparse(url)
        if parsed.netloc.endswith('.s3.amazonaws.com'):
            b_name = parsed.netloc.split('.')[0]
        elif parsed.netloc == 's3.amazonaws.com' or '.s3-' in parsed.netloc:
            if parsed.path.strip('/'):
                b_name = parsed.path.strip('/').split('/')[0]
            else:
                continue
        else:
            continue
        b_list.append(b_name)
    return remove_duplicate(b_list)