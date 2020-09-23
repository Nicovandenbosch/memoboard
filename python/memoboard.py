import memcache
import pyperclip
import socket
import urlparse
import time

class Client():
    def __init__(self):
        self._memcache = memcache.Client(['10.96.80.111:11211'], debug=0)
        self._memo = None

        # initialize our clipboard settings
        pyperclip.set_clipboard('klipper')

    def copy(self, key=None, value=None):
        """Insert a new key/value pair into the memoboard
        key"""
        # if no value supplied, get the contents of the current clipboard instead
        self._memo = Memo(key, value, mode='copy', memoboard=self)
        return self._memo

    def paste(self, key):
        self._memo = Memo(key, None, mode='paste', memoboard=self)
        return self._memo

    def url2memo(self, url):
        #url_obj = Url(url)
        url_obj = urlparse.urlparse(url)
        url_query = urlparse.parse_qs(url_obj.query)
        memo_key = url_query.get('key')[0]
        self._memo = self.paste(key=memo_key)
        return self._memo

    @property
    def memo(self):
        return self._memo

    @property
    def memcache(self):
        return self._memcache


class Memo():
    def __init__(self, key=None, value=None, mode='copy', memoboard=None):
        """A Memo object represents a single key/value entry in memoboard.
         Instantiated in one of two possible modes (copy/set or paste/get)."""
        self._memoboard = memoboard or Client()
        if mode == 'copy':
            self._key = key or self._generate_key()
            self._value = value or pyperclip.paste()
            self._memoboard.memcache.add(self._key, self._value)
            self._url = self._generate_url()
            self.url2clipboard()
        if mode == 'paste':
            # explicit key needs to be passed in paste mode, since we're retrieving an previously stored value from the cache
            self._key = key
            self._value = self._memoboard.memcache.get(key)
            self.value2clipboard()
            self._url = self._generate_url()

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def url(self):
        return self._url

    def url2clipboard(self):
        pyperclip.copy(self.url)

    def value2clipboard(self):
        pyperclip.copy(self.value)

    def _generate_url(self):
        return "myth://memoboard?key={}".format(self.key)

    def _generate_key(self):
        return "{hostname}_{date_time}".format(hostname=socket.gethostname(), date_time=time.strftime('%Y-%m-%dT%H:%M:%S'))
