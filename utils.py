# encoding: utf-8

import functools
import time

# Decorators for instance methods
def show_info(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.debug:
            print('[{}]'.format(func.__name__))
            start = time.time()
        result = func(self, *args, **kwargs)
        if self.debug:
            end = time.time()
            print('Time: {}\n'.format(end-start))
        return result
    return wrapper

def show_return_value(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.debug:
            print("Return value:")
            pp = pprint.PrettyPrinter()
            pp.pprint(result)
        return result
    return wrapper
# --

def show_func_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('[{}]'.format(func.__name__))
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('Time: {}\n'.format(end-start))
        return result
    return wrapper
