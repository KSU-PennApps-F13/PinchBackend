from flask import Flask
from ebaysdk import finding
import simplejson as json
import os

app = Flask(__name__)
api = finding(appid='danielgu-f316-4fd2-9373-2db1b6883df2')


@app.route("/<categories>")
def hello(categories=None):
  if not categories:
    return []
  api.execute('findItemsAdvanced', {'keywords': categories})
  return json.dumps(api.response_dict(), sort_keys = False, indent=2)


if __name__ == "__main__":
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
