from flask import Flask, request, jsonify, Response
from secrets import token_hex, compare_digest
# import time
import hashlib
import re

users = {"learner":"p@ssword"}
valid_tokens = {user: [] for user in users.keys()}

app = Flask(__name__)

def is_valid_token(token):
    valid = False
    for t in valid_tokens:
        if compare_digest(t, token):
            valid = True
            break
    return valid

def validate_response(auth_params, method):
    nonce = auth_params.get('nonce', '')
    cnonce = auth_params.get('cnonce', '')
    nc = auth_params.get('nc', '')
    response = auth_params.get('response', '')
    user = auth_params.get('username', '')
    realm = auth_params.get('realm', '')
    opaque = auth_params.get('opaque', '')
    qop = auth_params.get('qop', '')
    password = users.get(user, '')
    path = auth_params.get('uri', '')
    ha1 = hashlib.md5(f'{user}:{realm}:{password}'.encode('utf-8')).hexdigest()
    ha2 = hashlib.md5(f'{method}:{path}'.encode('utf-8')).hexdigest()
    expected = hashlib.md5(f'{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}'.encode('utf-8')).hexdigest()
    return expected == response

@app.route('/tokens', methods=['POST'])
def get_new_token():
    if not request.headers.get('Authorization', ''):
        nonce = token_hex(16)
        opaque = token_hex(16)
        return "Unauthorized", 401, {"WWW-Authenticate": f'Digest realm="example@api.com", nonce="{nonce}", opaque="{opaque}", qop="auth"'}
    reg = re.compile('(\w+)[=] ?"?([a-zA-Z0-9_@./]+)"?')
    auth_params = dict(reg.findall(request.headers.get("Authorization")))
    user = auth_params.get('username', '')
    if validate_response(auth_params, request.method):
        new_token = token_hex(32)
        valid_tokens[user].append(new_token)
        return Response(new_token, mimetype='text/plain')
    return f"Auth failure: expected {expected}, got {response}", 401

@app.route('/text', methods=['GET', 'POST'])
def handle_text():
    if request.method == 'GET':
        return Response('Hello from Flask', mimetype='text/plain')
    else:
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

