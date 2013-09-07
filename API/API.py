#!/usr/bin/env python

import gevent
from gevent import monkey,Greenlet
from urllib import urlencode
from urllib2 import urlopen
from abc import ABCMeta,abstractmethod

class InvalidReq(Exception):
    def __str__():
        return u'Not a valid request'

class ShoppingAPIFactory(object):
    def __init__(self):
        self._apis = []

    def register(self, method, const, *args, **kargs):
        """ Register a new API """
        apiInit = Functor(const, *args, **kargs)
        self._apis[method] = apiInit
        setattr(self, method, apiInit)

    def unregister(self, method):
        """ Unregister an API """
        delattr(self, method)

class Functor(object):
    def __init__(self, fun, *args, **kargs):
        assert callable(fun)
        self._args = args
        self._kargs = kargs
        self._fun = fun
    def __call__(self, *args, **kargs):
        return self._fun(*self._args, **self._kargs)

class ShoppingAPIObserver(object):
    def __init__(self):
        _observer = []

    def attach(self, observer):
        if not observer in _observer:
            _observer.append(observer)

    def detach(self, observer):
        try:
            _observer.remove(observer)
        except ValueError:
            pass

    def RunQuery(self, query):
        for req in _observer:
            req.start()

class ShoppingAPI(gevent.Greenlet):
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kargs):
        Greenlet.__init__(self)
        self._args = args
        self._kargs = kargs

    def prepare(self, query):
        self._set_category(query['cat'])
        self._set_keyword_list(query['kw'])

    @abstractmethod
    def _set_category(self, cat):
        """ Add categories info to the query """
        pass

    @abstractmethod
    def _set_keyword_list(self, kw):
        """ Add keywords to the query"""
        pass

    @abstractmethod
    def result(self):
        """ Parse reply data and give product info"""
        # play with self._reply
        pass

    def _run(self):
        """ the result is a file object that can do read() """
        #if not (self._query and self._baseurl and self._method):
            #raise InvalidReq()
        #if self._method == 'GET':
            #req = urlopen('?'.join([self._baseurl, urlencode(self._args)]))
        #else:
            #req = urlopen(self._baseurl, self._args)
        #self._reply = req
        pass

