import ebaysdk as ebay
import json
import API

class Ebay(ShoppingAPI):
    def __init__(self, appid):
        ShoppingAPI.__init__(self)
        self._api = ebay.finding(appid=appid)
    def prepare(self, query):
        self._set_category(query['cat'])
        self._set_keyword_list(query['kw'])
    def _set_category(self, cat):
        self._cat = cat
    def _set_keyword_list(self, kw):
        self._kw = kw
    def _run(self):
        self._api.execute('findItemsAdvanced', {'keywords': self._kw })
        return json.dumps(self._api.response_dict(), sort_keys = False, indent=2)
