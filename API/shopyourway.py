import hashlib
import urllib,urllib2,httplib2
import json
import struct
import time


class SYWAPI_Session:
    def __init__(self,app_id,app_secret,api_baseurl,syw_baseurl,app_baseurl):
        self.app_id=app_id;
        self.app_secret=app_secret
        self.api_baseurl=api_baseurl
        self.syw_baseurl=syw_baseurl
        self.app_baseurl=app_baseurl

    def generate_signature(self,user_id,time_stamp):
        userid_buffer=buffer(struct.pack('@q', user_id),0)
        timestamp_buffer=buffer(struct.pack('@d',time_stamp),0)
        appid_buffer=buffer(struct.pack('@q', self.app_id),0)
        appsecret_buffer=buffer(bytearray(ord(self.app_secret[i]) for i in range(0,len(self.app_secret))),0)
        return hashlib.sha256(str(userid_buffer)+str(appid_buffer)+str(timestamp_buffer)+str(appsecret_buffer)).hexdigest()

    def generate_hash(self,token):
        hash_str=hashlib.sha256(token+self.app_secret).hexdigest();
        return hash_str

    def get_offline_token(self,user_id):
        time_stamp=int(time.time())
        signature_str=self.generate_signature(user_id,time_stamp);
        time_stamp_str=time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time_stamp)).replace(' ','T')
        api_params=urllib.urlencode({'userId':user_id,'appId':self.app_id,'timestamp':time_stamp_str,'signature':signature_str})
        api_url=self.api_baseurl+'/auth/get-token?'+api_params
        api_url=api_url.replace("http","https")
        resp,content=httplib2.Http().request(api_url,"get")
        return content.replace('"','')

    def get_current_user(self,token):
        hash_str=self.generate_hash(token);
        api_params=urllib.urlencode({'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/users/current?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_user_followers(self,user_id,token):
        hash_str=self.generate_hash(token);
        api_params=urllib.urlencode({'userId':user_id,'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/users/followers?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_user_profile_details(self,token):
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/users/profile/current?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_user_catalogs(self,user_id,token):
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'userId':user_id,'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/catalogs/get-user-catalogs?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_catalogs_details(self,catalogs_id,token):
        catalogs_id_str=str(catalogs_id).replace('[','').replace(']','')
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'ids':catalogs_id_str,'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/catalogs/get?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_products_details(self,products_id,token):
        products_id_str=str(products_id).replace('[','').replace(']','')
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'ids':products_id_str,'token':token,'hash':hash_str})
        api_url=self.api_baseurl+'/products/get?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_user_wishlist(self,user_id,token):
        user_catalogs=self.get_user_catalogs(user_id,token)
        user_catalogs_details=self.get_catalogs_details(user_catalogs,token)
        product_ids=[]
        for catalog_details in user_catalogs_details:
            if catalog_details['name']=='My Wish List':
                for product in catalog_details['items']:
                    product_ids.append(product['id'])
                break
        if product_ids!=[]:
            user_wishlist=self.get_products_details(product_ids,token)
            return user_wishlist 
        else:
            return []

    def get_tags_for_query(self, token, query):
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'token':token,'hash':hash_str,'query':query})
        api_url=self.api_baseurl+'/search/tags?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)

    def get_products_by_tags(self, token, tags):
        hash_str=self.generate_hash(token)
        api_params=urllib.urlencode({'token':token,'hash':hash_str,'tagIds':",".join(tags), 'orderBy':'like', 'limit': '5'})
        api_url=self.api_baseurl+'/products/get-by-tags?'+api_params
        resp,content=httplib2.Http().request(api_url,"get")
        return json.loads(content)


    def get_tags(self, tags):
        tag_list = []
        for tag in tags:
            tag_list.append(str(tag['id']))
        return tag_list

if __name__=='__main__':
    user_id=5565403
    app_id=13610
    app_secret='c9aabb7017d5437982680872203ce4fc'
    api_baseurl='http://sandboxplatform.shopyourway.com'

    sywapi_session=SYWAPI_Session(app_id,app_secret,api_baseurl,'','')
    token = sywapi_session.get_offline_token(user_id)
    tags = sywapi_session.get_tags_for_query(token, "teddy")
    print sywapi_session.get_products_by_tags(token, sywapi_session.get_tags(tags))
