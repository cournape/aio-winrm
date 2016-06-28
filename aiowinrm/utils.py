import re
import urllib.parse

from .constants import TranportKind


R_HOST = re.compile("""
(?i)
^((?P<scheme>http[s]?)://)?
(?P<host>[0-9a-z-_.]+)
(:(?P<port>\d+))?
(?P<path>(/)?(wsman)?)?
""", re.VERBOSE)


# Adapted from pywinrm
def parse_host(url, transport=TranportKind.ssl):
    match = R_HOST.match(url)
    scheme = match.group('scheme')
    if not scheme:
        if transport == TranportKind.http:
            scheme = "http"
        elif transport == TranportKind.ssl:
            scheme = "https"
        else:
            raise ValueError("Invalid tranport {!r}".format(tranport))

    host = match.group('host')
    port = match.group('port')
    if not port:
        port = 5986 if transport == TranportKind.ssl else 5985
    path = match.group('path')
    if not path:
        path = 'wsman'
    return '{0}://{1}:{2}/{3}'.format(scheme, host, port, path.lstrip('/'))
