import flask
import json
import requests
from flask import request
from flask_cors import CORS

DEFAULT_LIMIT = 100

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/barchart', methods = ['POST'])
def barchart():
    try:
      post = request.json
      print(post)
      drug = post["drug"]
      adverse_reaction = post["ar"]

    except Exception as e:
      results = {}
      results['status'] = 'fail'
      results['error'] = repr(e)
      return json.dumps(results)

    # code to send csv here
    return None

@app.route('/treemap', methods = ['POST'])
def treemap():
   return None

@app.route('/graph', methods = ['POST'])
def forcegraph():
   
   # code to send force graph here
   return None

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)