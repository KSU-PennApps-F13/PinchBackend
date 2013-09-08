#!/usr/bin/env python

from API.core import ShoppingAPI
from API.shopyourway import SYWAPI_Session
import simplejson as json

class SYW(ShoppingAPI):
    def __init__(self, app_id, app_secret, api_baseurl, syw_baseurl, app_baseurl):
        ShoppingAPI.__init__(self)
        self.app_id = app_id
        self.app_secret = app_secret
        self.api_baseurl = api_baseurl
        self.syw_baseurl = syw_baseurl
        self.app_baseurl = app_baseurl
        self.session = SYWAPI_Session(app_id, app_secret, api_baseurl, syw_baseurl, app_baseurl)
        self.user_id=5565403
        self.token = self.session.get_offline_token(self.user_id)

    def _run(self):
        tags = self.session.get_tags_for_query(self.token, self._kw)
        self._reply = self.session.get_products_by_tags(self.token, self.session.get_tags(tags))
        return self._reply

    def result(self):
        res = []

        for item in self._reply:
            entry = {}
            entry['title'] = item['name']
            entry['image'] = item['imageUrl']
            entry['link']  = 'http://shopyourway.com' + item['productUrl']
            try:
              entry['price'] = item['price']
            except KeyError:
              entry['price'] = '11'
            res.append(entry)
        return res

