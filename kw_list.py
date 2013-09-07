#!/usr/bin/env python

from app import app
import json

@app.route('q', methods=['POST'])
def query(q):
    # just return bad request for GET
    if request == 'GET': abort(400)

    query_dict = json.loads(qstr)
    try:
        kw = query_dict['kw']
        cat = query_dict['cat']
    except TypeError:
        # return bad request for invalid data
        abort(400)
