import io
import random
from threading import Thread
from typing import Any

import webview
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO

import eventlet
import psutil
import flaskwebgui
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from serial import Serial

from ports import serial_ports, connect, read

app = Flask(__name__)
# app.config['SECRET_KEY'] = '0UXpWnXjTGg45jeBAAAC'
# socketio = SocketIO(app)
# wsgi_app = app.wsgi_app
# gui = flaskwebgui.FlaskUI(app, width=800, height=600)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
data = [0]*120
line, =ax.plot(data)
device = None


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/cpu')
def api_cpu():
    return str(psutil.cpu_percent(interval=0.1))


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


@app.route('/api/read', methods=['GET'])
def read_data():
    data = read(device)
    print(data)
    return data




@app.route('/api/plot.png')
def plot_png():
    global line
    global data
    global fig
    # fig = create_figure()
    dat = request.args.get('data')
    print(f"passed data: {dat}")
    if dat == 'No device connected':
        return None
    try:
        float(dat)
    except:
        return None
    finally:
        data = data[1:] + [float(dat)]
        # if not dat.isdigit():
        #     return None

    print(f"DATA: {data}")
    line.set_ydata(data)
    ax.relim()
    ax.autoscale_view()
    # fig.canvas.draw()
    # plt.plot(data)
    output = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(output)
    # print(data)
    # plt.gcf().savefig('./static/new_plot.png')
    # plt.savefig('./static/new_plot.png')
    print("plotting")
    return Response(output.getvalue(), mimetype='image/png')
    # return render_template('index.html', url='./static/new_plot.png')
    # return None

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


def run():
    app.run()


if __name__ == '__main__':
    # app.run(debug=True) # if you want to run this as a standalone script, use this
    # gui.run()
    t = Thread(target=run)
    t.start()

    # Create a borderless webview window
    webview.create_window("My Flask App", "http://127.0.0.1:5000", frameless=False, width=1024, height=720)
    webview.start()
