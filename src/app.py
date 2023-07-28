import sys
import threading
import time
from threading import Thread
from contextlib import redirect_stdout
from io import StringIO

# import flaskwebgui
import webview
from flask import Flask, render_template, request
from ports import serial_ports, connect, read, disconnect

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# gui = flaskwebgui.FlaskUI(app)
device = None


@app.route('/')
def hello():
    return render_template('index.html')
    # return "Hello, World!"

@app.route('/api/ports')
def get_ports():
    return serial_ports()


@app.route('/api/connect', methods=['GET'])
def connect_port():
    global device
    port = request.args.get('port')
    com = f"connected to {port}"
    device = connect(port)
    return com


@app.route('/api/disconnect', methods=['GET'])
def disconnect_port():
    global device
    result = disconnect(device)
    device = None
    return result


@app.route('/api/read', methods=['GET'])
def read_data():
    dat = read(device)
    return dat


# def run_server2():
#     gui.run()

def run_server():
    app.run()


def load_html(window):
    window.background_color = '#FFFFFF'

def start_gui():
    stream = StringIO()
    with redirect_stdout(stream):
        window = webview.create_window("My Flask App", url=app, frameless=True, transparent=False)
        webview.start(debug=False)


def run_desktop():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

    start_gui()


if __name__ == '__main__':
    # run_server()
    # run_server2()
    run_desktop()
    sys.exit()
