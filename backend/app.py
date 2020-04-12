from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

def login(username, password):
    if username is "username" and password is "password":
        return True
    else:
        return False

def get_shared_trans(group):
    return

def put_trans():
    return

def upd_trans():
    return

def get_stats():
    return

def put_rule():
    return

def get_rules():
    return

def get_total():
    return

if __name__ == '__main__':
    app.run()