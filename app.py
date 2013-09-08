from flask import Flask, request, render_template, abort
from API.core import ShoppingAPIFactory

import API.InstallAPI
import json
import gevent
import os

app = Flask(__name__)

@app.route('/q', methods=["POST"])
def query():
  if request == 'GET': 
    abort(401)
  try:
    data = json.loads(request.data)
    req = data['data']
  except (ValueError, KeyError, TypeError):
    abort(400)

  apiFunctors = ShoppingAPIFactory.all_registered_apis()
  apis = []
  for api in apiFunctors:
    apis.append(api())

  for a in apis:
    a.prepare(req)
    a.start()
  gevent.joinall(apis)

  res = []
  for a in  apis:
    r = a.result()
    if r:
      res.append(r)

  return json.dumps(res)


if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
