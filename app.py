from flask import Flask, request, render_template, abort
from API.core import ShoppingAPIFactory
import API.InstallAPI
import json
import gevent
import os

app = Flask(__name__)

@app.route('/q', methods=["POST"])
def query():
    # deny access for GET
    if request == 'GET': abort(401)
    print("data=", request.data)
    try:
        data = json.loads(request.data)
        req = data['data']
<<<<<<< HEAD
        print req
=======
        print('req=', req)
>>>>>>> 84b83c4a6cf7018897d8190b2768695cae83c73b
    except (ValueError, KeyError, TypeError):
        abort(400)
    # get all supported APIs
    apiFunctors = ShoppingAPIFactory.all_registered_apis()
    apis = []
    for api in apiFunctors:
        apis.append(api())
    for a in apis:
        a.prepare(req)
        a.start()
    gevent.joinall(apis)
    # collect result
    res = []
<<<<<<< HEAD
    for a in apis:
        res.append(a.result())
    print res
=======
    for a in  apis:
        r = a.result()
        if r: res.append(r)
    # render
>>>>>>> 84b83c4a6cf7018897d8190b2768695cae83c73b
    return json.dumps(res)

@app.route('/search')
def search():
    if request.method == 'GET':
        return render_template('form.html')

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
