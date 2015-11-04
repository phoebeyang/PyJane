#encoding=utf-8

"""
using new decorator to transfer test_name from case to setup and teardown function
"""

from nose import with_setup

def with_named_setup(setup=None, teardown=None):
    def wrap(f):
        return with_setup(
            lambda: setup(f.__name__) if (setup is not None) else None, 
            lambda: teardown(f.__name__) if (teardown is not None) else None)(f)
    return wrap
