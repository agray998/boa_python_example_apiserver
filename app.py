from flask import Flask, request, jsonify, Response
from secrets import token_hex, compare_digest
# import time
import hashlib
import re

valid_tokens = dict()
valid_tokens["learner"] = []
users = {"learner":"p@ssword"}

app = Flask(__name__)

def is_valid_token(token):
    valid = False
    for t in valid_tokens:
        if compare_digest(t, token):
            valid = True
            break
    return valid

@app.route('/tokens', methods=['POST'])
def get_new_token():
    if not request.headers.get('Authorization', ''):
        nonce = token_hex(16)
        opaque = token_hex(16)
        return "Unauthorized", 401, {"WWW-Authenticate": f'Digest realm="example@api.com", nonce="{nonce}", opaque="{opaque}", qop="auth"'}
    print(request.headers.get("Authorization"))
    reg = re.compile('(\w+)[=] ?"?([a-zA-Z0-9_@./]+)"?')
    auth_params = dict(reg.findall(request.headers.get("Authorization")))
    print(auth_params)
    nonce = auth_params['nonce']
    cnonce = auth_params['cnonce']
    nc = auth_params['nc']
    response = auth_params['response']
    user = auth_params['username']
    realm = auth_params['realm']
    opaque = auth_params['opaque']
    qop = auth_params['qop']
    password = users.get(user, '')
    method = request.method
    path = auth_params['uri']
    print(f'{user}:{realm}:{password}')
    print(f'{method}:{path}')
    ha1 = hashlib.md5(f'{user}:{realm}:{password}'.encode('utf-8')).hexdigest()
    ha2 = hashlib.md5(f'{method}:{path}'.encode('utf-8')).hexdigest()
    expected = hashlib.md5(f'{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}'.encode('utf-8')).hexdigest()
    if expected == response:
        new_token = token_hex(32)
        valid_tokens[user].append(new_token)
        return Response(new_token, mimetype='text/plain')
    return f"Auth failure: expected {expected}, got {response}", 401

@app.route('/text', methods=['GET', 'POST'])
def handle_text():
    if request.method == 'GET':
        return Response('Hello from Flask', mimetype='text/plain')
    else:
        request_token = request.authorization.token
        if not is_valid_token(request_token):
            return "Unauthorized", 401
        return Response("Data you sent: " + request.data.decode('utf-8'), mimetype='text/plain')

@app.route('/json', methods=['GET', 'POST'])
def handle_json():
    if request.method == 'GET':
        return jsonify({"data": "Hello from Flask"})
    else:
        request_token = request.headers["Authorization"].split(" ")[1]
        if not is_valid_token(request_token):
            return "Unauthorized", 401
        return jsonify({"data": request.get_json()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

