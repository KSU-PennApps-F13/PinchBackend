from flask import Flask, request, render_template, abort
from API.core import ShoppingAPIFactory
import API.InstallAPI
import json
import os

app = Flask(__name__)

@app.route('/q', methods=["POST"])
def query():
    # deny access for GET
    if request == 'GET': abort(401)
    try:
        data = json.loads(request.data)
        req = data['data']
        print req
    except (ValueError, KeyError, TypeError):
        abort(400)
    # get all supported APIs
    apis = ShoppingAPIFactory.all_registered_apis()
    for a in apis:
        a.prepare(req)
        a.start()
    ShoppingAPIFactory.joinall()
    # collect result
    res = []
    for a in apis:
        res.append(a.result())
    # render
    return json.dumps(res)

@app.route('/search')
def search():
    if request.method == 'GET':
        return render_template('form.html')

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
