import ebaysdk as ebay
import json
from API.core import ShoppingAPI
from ebaysdk import finding

from distutils.file_util import write_file

class Ebay(ShoppingAPI):
    def __init__(self, appid):
        ShoppingAPI.__init__(self)
        self._api = ebay.finding(appid=appid)
    def _run(self):
        self._api.execute('findItemsAdvanced', {'keywords': self._kw, 'entriesPerPage':10 })
        reply = self._api.response_dict()
        self._reply = self._api.response_dict()
        #write_file('ebay.json', str(self._reply[0]['searchResult']['item'][0]))
        #return self._reply
        return self._reply

    def result(self):
        res = []
        entry = {}
        for item in self._reply['searchResult']['item']:
          if item.country == "US":
            entry['title'] = item.title
            entry['image'] = item.galleryURL
            entry['link'] = item.viewItemURL
            entry['price'] = item.sellingStatus.convertedCurrentPrice.value
            res.append(entry)
        return res

