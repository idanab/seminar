import ctypes
import time
from random import randint

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address)


@app.route("/test")
def test():
    return "api is running!"


@app.route('/random_nums', methods=['GET'])
def get_random_nums():
    size = int(request.args['size'])
    return jsonify([randint(0, 1000) for _ in range(size)])


@app.route('/execute', methods=['POST'])
def execute_code():
    json_request = request.get_json()
    code = json_request['code']
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if is_admin:
        return "Failed - could not eval expression because api is run by an administrator"
    for expression in ["subprocess.", "shell", "rm ", "mv "]:
        if expression in code:
            return "Failed - the code you are trying to run might be malicious"
    eval(code)
    return "finished"


@app.route("/denial_of_service")
@limiter.limit("10 per minute")
def func_preventing_dos():
    print("doing a very consuming operation")
    return ",".join([str(num) for num in range(1000000)])


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=1234)
