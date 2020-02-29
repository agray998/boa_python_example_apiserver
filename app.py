from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/get/text', methods=['GET'])
def get_text():
    return Response('Hello from Flask', mimetype='text/plain')

@app.route('/post/text', methods=['POST'])
def post_text():
    return Response("Data you sent: " + request.data.decode("utf-8"), mimetype='text/plain')

@app.route('/get/json', methods=['GET'])
def get_json():
    return Response({"data": "Hello from Flask"}, mimetype='application/json')

@app.route('/post/json', methods=['POST'])
def post_json():
    return Response({"data": request.get_json()}, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

