from flask import Flask, request
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/server', methods=['POST'])
@cross_origin()
def sort():
    json: list[int] = request.get_json()
    json.sort()
    return json


if __name__ == '__main__':
    app.run(debug=True)
