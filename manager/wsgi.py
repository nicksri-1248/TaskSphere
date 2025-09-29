"""
WSGI config for manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

# Add compatibility shims for Python 3.13+
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Fix collections.Iterator compatibility for Django 2.0.3 with Python 3.13+
try:
    import collections
    if not hasattr(collections, 'Iterator'):
        import collections.abc
        collections.Iterator = collections.abc.Iterator
        collections.Iterable = collections.abc.Iterable
        collections.Mapping = collections.abc.Mapping
        collections.MutableMapping = collections.abc.MutableMapping
        collections.Set = collections.abc.Set
        collections.MutableSet = collections.abc.MutableSet
        collections.Sequence = collections.abc.Sequence
        collections.MutableSequence = collections.abc.MutableSequence
except (ImportError, AttributeError):
    pass

# Fix gettext.translation codeset parameter compatibility for Python 3.13+
try:
    import gettext
    _original_translation = gettext.translation
    
    def patched_translation(domain, localedir=None, languages=None, class_=None, fallback=False, codeset=None):
        """Remove codeset parameter for Python 3.13+ compatibility"""
        kwargs = {
            'domain': domain,
            'localedir': localedir, 
            'languages': languages,
            'fallback': fallback
        }
        if class_ is not None:
            kwargs['class_'] = class_
        # Filter out None values and codeset
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return _original_translation(**kwargs)
    
    gettext.translation = patched_translation
except (ImportError, AttributeError):
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manager.settings")

application = get_wsgi_application()