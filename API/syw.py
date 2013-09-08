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
        tags = self.session.get_tags_for_query(self.token, " ".join(self._kw))
        self._reply = self.session.get_products_by_tags(self.token, self.session.get_tags(tags))
        return self._reply

    def result(self):
        res = []
        #print(str(self._reply))

        for item in self._reply:
            entry = {}
            if not isinstance(item, dict):
              continue
            try:
              entry['title'] = item['name']
              entry['image'] = item['imageUrl']
              entry['link']  = 'http://shopyourway.com' + item['productUrl']
              entry['price'] = item['price']
            except KeyError, TypeError:
              entry['title'] = "Some Title"
              entry['image'] = "http://c.shld.net/rpx/i/s/i/spin/image/spin_prod_500334201"
              entry['link']  = "http://shopyourway.com/sharp-60-class-aquos-1080p-120hz-led-smart-hdtv-lc60le640u/163097737"
              entry['price'] = '11'
            res.append(entry)
        return res

