# kicks3.py

import argparse
import json
import pathlib
from typing import Final

from .s3_utils import check_listings, get_bucket_acl, put_bucket_policy, check_upload
from .url_utils import get_bucket_name
from .web_scraper import finds3


def check_bucket(bucket: str) -> dict:
    unauth_list, auth_list = check_listings(bucket)
    upload = check_upload(bucket)
    get_acl = get_bucket_acl(bucket)
    put_policy = put_bucket_policy(bucket)

    return {
        "bucket": bucket,
        "unauth_list": unauth_list,
        "auth_list": auth_list,
        "upload": upload,
        "get_acl": get_acl,
        "put_policy": put_policy
    }


def print_bucket_results(bucket, unauth_list, auth_list, upload, get_acl, put_policy):
    print(f"Bucket name: {bucket}")
    if unauth_list:
        print("[*] S3 Bucket Lists Files for unauthenticated users [*]")
    if auth_list:
        print("[*] S3 Bucket Lists Files for all aws authenticated users [*]")
    else:
        print("[-] Directory Listings ... Access Denied [-]")
    if upload:
        print("[+] File uploaded Successfully [+]")
    else:
        print("[-] File  Not Upload ... Access Denied [-]")
    if get_acl:
        print("[*] Get acl read [*]")
    if put_policy:
        print("[*] Put bucket_policy [*]")


def parse_args():
    parser = argparse.ArgumentParser(description="Tool for checking and interacting with AWS S3 buckets.")

    parser.add_argument("--url", help="Target URL to scan for S3 URLs, starting with http or https.")
    parser.add_argument("--bucket", help="Single S3 bucket name to check.")
    parser.add_argument("--bucketlist", help="File containing list of S3 bucket names to check.")
    parser.add_argument("--cookie", help="Cookie values for authentication when scanning URLs.")
    parser.add_argument("--list", help="File containing list of URLs to scan for S3 URLs, e.g., sitelist.txt.")
    parser.add_argument("--subdomain", action="store_true", help="Enable subdomain enumeration when scanning URLs.")
    parser.add_argument("--output", help="Save results to a file JSON.")

    return parser.parse_args()



def main():
    args = parse_args()

    MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).resolve().parents[0]
    OUTPUT_JSON = MAIN_DIR / args.output
    results = None

    if not any([args.url, args.bucket, args.bucketlist]):
        print("Please provide at least one of --url, --bucket, or --bucketlist.")
        exit()

    if args.url or args.list:
        sitelist = []
        if args.url:
            sitelist.append(args.url)
        if args.list:
            with open(args.list, 'r') as f:
                sitelist.extend([line.strip() for line in f])
        cookies = args.cookie if args.cookie else ''
        sub = args.subdomain
        s3urls = finds3(sitelist, cookies, sub)
        if s3urls[0] == 'Bucket not found':
            print("Bucket not found")
        else:
            bucketnames = get_bucket_name(s3urls)
            for bucket in bucketnames:
                results = check_bucket(bucket)
                print_bucket_results(bucket, *results)

    if args.bucket:
        bucket = args.bucket
        results = check_bucket(bucket)
        print_bucket_results(bucket, *results)

    if args.bucketlist:
        with open(args.bucketlist, 'r') as f:
            bucket_list = [line.strip() for line in f]
        for bucket in bucket_list:
            results = check_bucket(bucket)
            print_bucket_results(bucket, *results)

    if not results:
        results = {
            "message": "Bucket not found",
        }
    with OUTPUT_JSON.open('w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
