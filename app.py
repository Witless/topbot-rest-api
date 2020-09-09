import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import redis

load_dotenv()

r = redis.Redis(host=os.getenv('HOST'), port=os.getenv('PORT'), db=0, password=os.getenv('PASSWORD'),
                decode_responses=True)

app = Flask(__name__)


@app.route('/')
def gethelp():
    return jsonify({"TopBot api v1, endpoints": {
        "PUT": "/api/v1/auth=<string>/topID=<string>/key=<string>/value=<string>",
        "POST": "/api/v1/auth=<string>/topID=<string>/key=<string>/value=<string>",
        "DELETE": "/api/v1/auth=<string>/topID=<string>/key=<string>"}})


@app.route('/api/v1/auth=<string:token>/topID=<string:topID>/key=<string:key>/value=<string:value>', methods=['PUT'])
def put(token, topID, key, value):
    if topID != "tokens" or key == "channel" or key == "message" or key == "_v":
        return jsonify({"res": "-1"})
    token = r.hget("tokens", token)
    if token == topID.split("_")[0] and r.hgetall(topID) and r.hget(topID, key):
        _v = str(int(r.hget(topID, "_v")) + 1)
        r.hset(topID, key, value)
        r.hset(topID, "_v", _v)
        return jsonify({"res": "1"})
    else:
        return jsonify({"res": "-1"})


@app.route('/api/v1/auth=<string:token>/topID=<string:topID>/key=<string:key>')
def get(token, topID, key):
    if topID != "tokens" or key == "channel" or key == "message" or key == "_v":
        return jsonify({"res": "-1"})
    token = r.hget("tokens", token)
    if token == topID.split("_")[0] and r.hgetall(topID) and r.hget(topID, key):
        return jsonify({"res": "1"})
    elif token == topID.split("_")[0] and r.hgetall(topID) and not r.hget(topID, key):
        return jsonify({"res: -2"})
    else:
        return jsonify({"res": "-1"})


@app.route('/api/v1/auth=<string:token>/topID=<string:topID>/key=<string:key>', methods=['PATCH'])
def patch(token, topID, key):
    if topID != "tokens" or key == "channel" or key == "message" or key == "_v":
        return jsonify({"res": "-1"})
    token = r.hget("tokens", token)
    if token == topID.split("_")[0] and r.hgetall(topID) and r.hget(topID, key):
        value = str(int(r.hget(topID, key)) + 1)
        _v = str(int(r.hget(topID, "_v")) + 1)
        r.hset(topID, key, value)
        r.hset(topID, "_v", _v)
        return jsonify({"res": "1"})
    else:
        return jsonify({"res": "-1"})


@app.route('/api/v1/auth=<string:token>/topID=<string:topID>/key=<string:key>/value=<string:value>', methods=['POST'])
def post(token, topID, key, value):
    if topID != "tokens" or key == "channel" or key == "message" or key == "_v":
        return jsonify({"res": "-1"})
    token = r.hget("tokens", token)
    if token == topID.split("_")[0] and r.hgetall(topID) and not r.hget(topID, key):
        _v = str(int(r.hget(topID, "_v")) + 1)
        r.hset(topID, key, value)
        r.hset(topID, "_v", _v)
        return jsonify({"res": "1"})
    else:
        return jsonify({"res": "-1"})


@app.route('/api/v1/auth=<string:token>/topID=<string:topID>/key=<string:key>', methods=['DELETE'])
def delete(token, topID, key):
    if topID != "tokens" or key == "channel" or key == "message" or key == "_v":
        return jsonify({"res": "-1"})
    token = r.hget("tokens", token)
    if token == topID.split("_")[0] and r.hgetall(topID) and r.hget(topID, key):
        _v = str(int(r.hget(topID, "_v")) + 1)
        r.hdel(topID, key)
        r.hset(topID, "_v", _v)
        return jsonify({"res": "1"})
    else:
        return jsonify({"res": "-1"})


if __name__ == '__main__':
    app.run(debug=True, port=4000)
