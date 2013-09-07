from flask import Flask, request, render_template
import API.core as API
import simplejson as json
import os

app = Flask(__name__)

@app.route('/q', methods=["POST"])
def query():
    # deny access for GET
    if request == 'GET': abort(401)

    query_dict = json.loads(request.content)
    try:
        kw = query_dict['kw']
        cat = query_dict['cat']
    except TypeError:
        # return bad request for invalid data
        abort(400)
    # get all supported APIs
    apis = API.ShoppingAPIFactory.all_registered_apis()
    for a in apis:
        a.prepare(query)
        a.start()
    API.ShoppingAPIFactory.joinall()
    # collect result
    res = []
    for a in apis:
        res.append(a.reformatted_result())
    # render
    return json.dumps(res)

@app.route('/search')
def search():
    if request.method == 'GET':
        return render_template('form.html')

if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
