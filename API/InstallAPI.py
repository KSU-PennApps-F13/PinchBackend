import API.core as API
from API.ebay import Ebay
from API.syw import SYW

API.ShoppingAPIFactory.register("newEbay",
                                Ebay,
                                appid='danielgu-f316-4fd2-9373-2db1b6883df2')

API.ShoppingAPIFactory.register("newSYW",
                                SYW,
                                app_id=13610,
                                app_secret='c9aabb7017d5437982680872203ce4fc',
                                api_baseurl='http://sandboxplatform.shopyourway.com',
                                syw_baseurl='',
                                app_baseurl='')
