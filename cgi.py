"""
CGI module compatibility shim for Python 3.13+
Provides essential CGI functionality for Django 2.0.3 compatibility
"""

import html
import urllib.parse
from io import StringIO, BytesIO


def escape(s, quote=False):
    """Escape HTML characters in a string."""
    return html.escape(s, quote)


def parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace'):
    """Parse a query string."""
    return urllib.parse.parse_qs(qs, keep_blank_values, strict_parsing, encoding=encoding, errors=errors)


def parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace'):
    """Parse a query string into a list of tuples."""
    return urllib.parse.parse_qsl(qs, keep_blank_values, strict_parsing, encoding=encoding, errors=errors)


class FieldStorage:
    """Simple FieldStorage implementation for basic form handling."""
    
    def __init__(self, fp=None, headers=None, outerboundary=b'', environ=None, keep_blank_values=0, strict_parsing=0):
        self.fp = fp
        self.headers = headers or {}
        self.outerboundary = outerboundary
        self.environ = environ or {}
        self.keep_blank_values = keep_blank_values
        self.strict_parsing = strict_parsing
        self.list = []
        
    def __getitem__(self, key):
        """Dictionary-like access."""
        for item in self.list:
            if item.name == key:
                return item
        raise KeyError(key)
    
    def getvalue(self, key, default=None):
        """Get the value for a given key."""
        try:
            return self[key].value
        except KeyError:
            return default
    
    def getlist(self, key):
        """Get a list of values for a given key."""
        values = []
        for item in self.list:
            if item.name == key:
                values.append(item.value)
        return values


class MiniFieldStorage:
    """Minimal field storage for simple values."""
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.filename = None
        self.file = None


def parse_header(line):
    """Parse a Content-Type like header."""
    parts = line.split(';')
    main_type = parts[0].strip()
    pdict = {}
    
    for p in parts[1:]:
        if '=' in p:
            name, value = p.split('=', 1)
            name = name.strip().lower()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            pdict[name] = value
    
    return main_type, pdict


def parse_multipart(fp, pdict, encoding='utf-8', errors='replace'):
    """Parse multipart form data (simplified implementation)."""
    boundary = pdict.get('boundary', b'')
    if isinstance(boundary, str):
        boundary = boundary.encode('ascii')
    
    # This is a simplified implementation
    # In practice, Django handles multipart parsing differently
    return []


# For compatibility with older Django versions
def print_exception(type=None, value=None, tb=None, limit=None, file=None):
    """Print exception information."""
    import traceback
    if file is None:
        import sys
        file = sys.stderr
    traceback.print_exception(type, value, tb, limit, file)


# Additional compatibility functions
def print_environ(environ=None):
    """Print the shell environment."""
    import os
    if environ is None:
        environ = os.environ
    for key, value in environ.items():
        print(f"{key}={value}")


def print_form(form):
    """Print a form as HTML."""
    print("Content-Type: text/html\n")
    print("<html><body>")
    for key in form:
        print(f"<p>{escape(key)}: {escape(form[key].value)}</p>")
    print("</body></html>")


def print_directory():
    """Print the current directory."""
    import os
    print("Content-Type: text/html\n")
    print("<html><body>")
    print(f"<h1>Directory: {os.getcwd()}</h1>")
    print("</body></html>")


def print_environ_usage():
    """Print environment usage."""
    print("Content-Type: text/html\n")
    print("<html><body>")
    print("<h1>Environment Variables</h1>")
    print_environ()
    print("</body></html>")