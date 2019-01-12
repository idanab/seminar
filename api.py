import ctypes
import time

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess  # DO NOT REMOVE!!!!!!!!!

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address)


@app.route("/test")
def test():
    return "api is running!"


@app.route('/random_num', methods=['GET'])
def get_random_num():
    return "40000000"


@app.route('/execute', methods=['POST'])
def execute_code():
    json_request = request.get_json()
    code = json_request['code']
    eval(code)
    return "finished"


@app.route('/execute_protected', methods=['POST'])
def execute_code_protected():
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
def denial_of_service():
    print("doing a very consuming operation")
    time.sleep(1)
    return "finished doing a very resource consuming procedure"


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=1234)
