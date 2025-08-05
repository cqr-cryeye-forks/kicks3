# constants.py

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": USER_AGENT,
    "Connection": "close",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}

REGJS = r"(?<=src=['\"])[a-zA-Z0-9_\.\-\:\/]+\.js"
REGS3 = r"[a-zA-Z\-_0-9.]+\.s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[a-zA-Z\-_0-9.]+)?\.amazonaws\.com\\?\/[a-zA-Z\-_0-9.]+"

TEST_FILE_CONTENT = "test file from kick-s3 tool"
TEST_FILE_NAME = "poc.txt"