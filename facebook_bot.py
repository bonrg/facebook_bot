import re, os, time
import urllib.request
import urllib.parse
import http.cookiejar
import requests
from requests.exceptions import RequestException
import logging


logger = logging.getLogger("FacebookBot")
logger.setLevel(logging.WARNING)
# ======================================================================================================================
# create console handler and set level to info
handler_log = logging.StreamHandler()
handler_log.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s')
handler_log.setFormatter(formatter)
logger.addHandler(handler_log)


class FacebookBot:

    AUTH_URL = 'https://m.facebook.com/login.php'

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.COOKIE_FILE = 'facebook_' + self.login + '_cookies.txt'
        #  Cookies expire 12 months since the last modification

    def get_cookies(self):
        try:
            with requests.get(self.AUTH_URL):
                pass
            payload = {
                'email': self.login,
                'pass': self.password
            }
            data = urllib.parse.urlencode(payload).encode('utf-8')
            cookies = http.cookiejar.MozillaCookieJar(self.COOKIE_FILE)
            handler = urllib.request.HTTPCookieProcessor(cookies)
            opener = urllib.request.build_opener(handler)
            request = urllib.request.Request(self.AUTH_URL, data)
            opener.open(request)
            c_user = re.search(r'c_user', str(cookies))  # facebook cookie parameter
            if c_user:
                cookies.save(ignore_discard=True, ignore_expires=False)
            else:
                logger.warning('Invalid login or password | Account blocked')
            opener.close()
            return cookies
        except RequestException:
            logger.warning('Facebook host not responding')

    def load_cookies(self):
        check_file_exists = os.path.isfile(self.COOKIE_FILE)
        if check_file_exists:
            cookies = http.cookiejar.MozillaCookieJar(self.COOKIE_FILE)
            cookies.load()
            expiry = list(cookie for cookie in cookies)[0].expires
            if expiry < time.time():
                cookies = self.get_cookies()
            return cookies
        else:
            logger.warning(f'Cookie file not found, getting... a new cookie file')
            cookies = self.get_cookies()
            return cookies


if __name__ == "__main__":
    user = ''
    password = ''
    bot = FacebookBot(user, password)
    print(bot.get_cookies())
