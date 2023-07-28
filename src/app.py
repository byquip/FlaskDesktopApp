from threading import Thread
import webview
from flask import Flask, render_template, request
from ports import serial_ports, connect, read, disconnect

app = Flask(__name__)
device = None


@app.route('/')
def hello():
    return render_template('index.html')


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


def run_server():
    app.run()


def run_desktop():
    t = Thread(target=run_server)
    t.start()

    # Create a borderless webview window
    webview.create_window("My Flask App", 'http://localhost:5000', frameless=True, transparent=False)
    webview.start(debug=False, http_server=False, user_agent=None)


if __name__ == '__main__':
    # run_server()
    run_desktop()
