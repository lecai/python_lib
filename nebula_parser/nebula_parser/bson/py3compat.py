"""Utility functions and definitions for python3 compatibility."""

import sys

PY3 = sys.version_info[0] == 3

if PY3:
    import codecs
    import _thread as thread
    from io import BytesIO as StringIO
    MAXSIZE = sys.maxsize

    imap = map

    def b(s):
        # BSON and socket operations deal in binary data. In
        # python 3 that means instances of `bytes`. In python
        # 2.6 and 2.7 you can create an alias for `bytes` using
        # the b prefix (e.g. b'foo').
        # See http://python3porting.com/problems.html#nicer-solutions
        return codecs.latin_1_encode(s)[0]

    def u(s):
        # PY3 strings may already be treated as unicode literals
        return s

    def bytes_from_hex(h):
        return bytes.fromhex(h)

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    def reraise(exctype, value, trace=None):
        raise exctype(str(value)).with_traceback(trace)

    def _unicode(s):
        return s

    text_type = str
    string_type = str
    integer_types = int
else:
    import thread

    from itertools import imap
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    MAXSIZE = sys.maxint

    def b(s):
        # See comments above. In python 2.x b('foo') is just 'foo'.
        return s

    def u(s):
        """Replacement for unicode literal prefix."""
        return unicode(s.replace('\\', '\\\\'), 'unicode_escape')

    def bytes_from_hex(h):
        return h.decode('hex')

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    # "raise x, y, z" raises SyntaxError in Python 3
    exec("""def reraise(exctype, value, trace=None):
    raise exctype, str(value), trace
""")

    _unicode = unicode

    string_type = basestring
    text_type = unicode
    integer_types = (int, long)
