from flask import Flask, request

app = Flask(__name__)

@app.route('/get/text', methods=['GET'])
def get_text():
    return 'Hello from Flask'

@app.route('/post/text', methods=['POST'])
def post_text():
    return "Data you sent: " + request.data.decode("utf-8")

@app.route('/get/json', methods=['GET'])
def get_json():
    return {"data": "Hello from Flask"}

@app.route('/post/json', methods=['POST'])
def post_json():
    return {"data": request.data}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

