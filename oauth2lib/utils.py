from __future__ import absolute_import, division, print_function, unicode_literals
import string
import urllib
try:
    from urllib.parse import urlparse, urlencode, urljoin, parse_qsl, urlunparse
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urlparse import urlparse, urljoin, urlunparse, parse_qsl
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

from random import SystemRandom

try:
    UNICODE_ASCII_CHARACTERS = (string.ascii_letters +
        string.digits)
except AttributeError:
    UNICODE_ASCII_CHARACTERS = (string.ascii_letters.decode('ascii') +
        string.digits.decode('ascii'))


def random_ascii_string(length):
    random = SystemRandom()
    return ''.join([random.choice(UNICODE_ASCII_CHARACTERS) for x in range(length)])


def url_query_params(url):
    """Return query parameters as a dict from the specified URL.

    :param url: URL.
    :type url: str
    :rtype: dict
    """
    return dict(parse_qsl(urlparse(url).query, True))


def url_dequery(url):
    """Return a URL with the query component removed.

    :param url: URL to dequery.
    :type url: str
    :rtype: str
    """
    url = urlparse(url)
    return urlunparse((url.scheme,
                                url.netloc,
                                url.path,
                                url.params,
                                '',
                                url.fragment))


def build_url(base, additional_params=None):
    """Construct a URL based off of base containing all parameters in
    the query portion of base plus any additional parameters.

    :param base: Base URL
    :type base: str
    ::param additional_params: Additional query parameters to include.
    :type additional_params: dict
    :rtype: str
    """
    url = urlparse(base)
    query_params = {}
    query_params.update(parse_qsl(url.query, True))
    if additional_params is not None:
        query_params.update(additional_params)
        for k, v in additional_params.items():
            if v is None:
                query_params.pop(k)

    # Py3 future compatibility
    return urlunparse((str(url.scheme),
                      str(url.netloc),
                      str(url.path),
                      str(url.params),
                      str(urlencode(query_params)),
                      str(url.fragment)))

