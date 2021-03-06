from API.core import ShoppingAPI
from ebaysdk import finding
from distutils.file_util import write_file

import ebaysdk as ebay
import json

class Ebay(ShoppingAPI):

  def __init__(self, appid):
    ShoppingAPI.__init__(self)
    self._api = ebay.finding(appid=appid)

  def _run(self):
    # TODO: limit this to maybe 20-50 items...
    self._api.execute('findItemsAdvanced', {'keywords': self._kw})
    self._reply = self._api.response_dict()
    return self._reply

  def result(self):
    res = []
    try:
      items = self._reply['searchResult']['item']
    except:
      return None

    for item in items:
      if item.country == "US":
        entry = {}
        entry['title'] = item.title
        entry['image'] = item.galleryURL
        entry['link'] = item.viewItemURL
        entry['price'] = item.sellingStatus.convertedCurrentPrice.value
        res.append(entry)

    return res
