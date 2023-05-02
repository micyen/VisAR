import flask
import json
import drug_reac
import force
import barChartServer as bc
from flask import request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/treemap', methods = ['POST'])
def treemap():
    #print("running")
    try:
        #print(request)
        post = request.json
        #print(post)
        output = drug_reac.getTreeMapFiltered(post)
        #print(output)
        return {"statusCode": 200, "body" :output}

    except Exception as e:
        return "ERROR"



@app.route('/forceGraph', methods = ['POST'])
def forceGraph():
    #print("running")
    try:
        #print(request)
        post = request.json
        #print(post)
        if 'minWt' not in post:
            post['minWt'] = 1

        if 'drug' not in post:
            output = force.fullGraph(post['minWt'])
            return {"statusCode": 200, "body" :output}
            
        if 'distance' not in post:
            post['distance'] = 1000
            
        output = force.coDosingGraphFromFile(post['drug'],post['distance'],post['minWt'])
        #print(output)
        return {"statusCode": 200, "body" :output}

    except Exception as e:
        return "ERROR"

@app.route('/drugList', methods = ['GET'])
def drugList():
    #print("running")
    try:
        #print(request)
        #post = request.json
        #print(post)
        #output = force.coDosingGraphFromFile(post['drug'],post['distance'],post['minWt'])
        #print(output)
        list = []
        with open("DrugList.txt", 'r+') as f:
            list = [line.rstrip('\n') for line in f]
        
        return {"statusCode": 200, "body" :json.dumps(list)}

    except Exception as e:
        return "ERROR"

@app.route('/barChartMain', methods = ['POST'])
def barChartMain():
    #print("running")
    try:
        print("BarChartMain")
        post = request.json
        print(str(post))
        output = bc.getDrugJson(post['drug'])
        #print(output)
        return {"statusCode": 200, "body" :output}

    except Exception as e:
        print(e)
        return "ERROR"

@app.route('/barChartSub', methods = ['POST'])

def barChartSub():
    #print("running")
    try:
        print("BarChart")
        post = request.json
        print(str(post))
        output = bc.getAEJson(post['drug'],post['ae'])
        #print(output)
        return {"statusCode": 200, "body" :output}

    except Exception as e:
        print(e)
        return "ERROR"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port = 5000, debug=False)
    #serve(app, host='0.0.0.0', port=5000)