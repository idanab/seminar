import time

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address)


@app.route("/test")
def test():
    return "api is running!"


@app.route("/denial_of_service")
@limiter.limit("10 per minute")
def func_preventing_dos():
    print("doing a very consuming operation")
    return ",".join([str(num) for num in range(1000000)])


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=1234)
