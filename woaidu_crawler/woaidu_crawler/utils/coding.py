from __future__ import with_statement

import os
import os.path
import datetime
import logging
import shutil
import urllib
import IPy
import hashlib

def make_dir(dir):
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except (IOError, OSError):
            if os.path.exists(dir) and os.path.isdir(dir):
                return
            else:
                raise

def make_unicode(value, prefer_encodings=None):
    if prefer_encodings is None:
        prefer_encodings = ['utf8', 'gbk', 'gbk?']
    
    if isinstance(value, unicode) or value is None:
        return value
    
    if not isinstance(value, str):
        return value

    for enc in prefer_encodings:
        try:
            if enc.endswith('!'):
                return value.decode(enc[:-1], 'ignore')
            elif enc.endswith('?'):
                return value.decode(enc[:-1], 'replace')
            elif enc.endswith('&'):
                return value.decode(enc[:-1], 'xmlcharrefreplace')
            elif enc.endswith('\\'):
                return value.decode(enc[:-1], 'backslashreplace')
            else:
                return value.decode(enc)
        except UnicodeError:
            pass
    else:
        raise

def _make_unicode_elem(obj, **options):
    if isinstance(obj, list):
        obj = [_make_unicode_elem(elem, **options) for elem in obj]
    elif isinstance(obj, dict):
        obj = dict((make_unicode(k, **options), _make_unicode_elem(v, **options)) for k,v in obj.items())
    elif isinstance(obj, str):
        obj = make_unicode(obj, **options)
    return obj

def make_unicode_obj(obj, **options):
    return _make_unicode_elem(obj, **options)

def make_utf8(value, prefer_encodings=None):
    uv = make_unicode(value, prefer_encodings)
    if uv is None:
        return None
    
    if not isinstance(uv, unicode):
        return uv
        
    return uv.encode('utf8', 'xmlcharrefreplace')

def _make_utf8_elem(obj, **options):
    if isinstance(obj, list):
        obj = [_make_utf8_elem(elem, **options) for elem in obj]
    elif isinstance(obj, dict):
        obj = dict((make_utf8(k, **options), _make_utf8_elem(v, **options)) for k,v in obj.items())
    elif isinstance(obj, unicode):
        obj = make_utf8(obj, **options)

    return obj

def make_utf8_obj(obj, prefer_encodings=None):
    return _make_utf8_elem(obj, prefer_encodings=prefer_encodings)

def is_ip_address(s):
    try:
        IPy.IP(s)
    except Exception, e:
        return False
    else:
        return True

def get_file_md5(path):
    """Calc file MD5 with a save-memory method."""
    
    md5 = hashlib.md5()
    with open(path, 'r') as f:
        data = f.read(512*1024)
        while data:
            md5.update(data)
            data = f.read(512*1024)
            
    return md5.hexdigest()
