#!/usr/bin/env python

import gevent
from gevent import monkey,Greenlet
from urllib import urlencode
from urllib2 import urlopen
from abc import ABCMeta,abstractmethod

gevent.monkey.patch_all()

class InvalidReq(Exception):
    def __str__():
        return u'Not a valid request'

class ShoppingAPIFactory(object):
    _apis = {}
    def __init__(self):
        pass

    @staticmethod
    def register(method, const, *args, **kargs):
        """ Register a new API """
        apiInit = Functor(const, *args, **kargs)
        ShoppingAPIFactory._apis[method] = apiInit()
        setattr(ShoppingAPIFactory, method, apiInit)

    @staticmethod
    def unregister(method):
        """ Unregister an API """
        delattr(ShoppingAPIFactory, method)

    @staticmethod
    def all_registered_apis():
        return ShoppingAPIFactory._apis.values()

    @staticmethod
    def joinall():
        gevent.joinall(ShoppingAPIFactory._apis.values())

class Functor(object):
    def __init__(self, fun, *args, **kargs):
        assert callable(fun)
        self._args = args
        self._kargs = kargs
        self._fun = fun

    def __call__(self, *args, **kargs):
        return self._fun(*self._args, **self._kargs)

class ShoppingAPI(gevent.Greenlet):
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kargs):
        Greenlet.__init__(self)
        self._args = args
        self._kargs = kargs

    def prepare(self, query):
        query_list = []
        for q in query:
          query_list.append(q['name'])
        print query_list
        self._set_keyword_list(query_list)

    def _set_keyword_list(self, kw):
        """ Add keywords to the query"""
        self._kw = kw

    @abstractmethod
    def result(self):
        """ Parse reply data and give product info"""
        # play with self._reply
        return self._reply

    def _run(self):
        """ the result is a file object that can do read() """
        #if not (self._query and self.V_baseurl and self._method):
            #raise InvalidReq()
        #if self._method == 'GET':
            #req = urlopen('?'.join([self._baseurl, urlencode(self._args)]))
        #else:
            #req = urlopen(self._baseurl, self._args)
        #self._reply = req
        pass

