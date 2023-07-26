from threading import Thread

import webview
from flask import Flask, render_template
import psutil
import flaskwebgui

app = Flask(__name__)
# wsgi_app = app.wsgi_app
# gui = flaskwebgui.FlaskUI(app, width=800, height=600)

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/cpu')
def api_cpu():
    return str(psutil.cpu_percent(interval=0.1))

def run():
    app.run()

if __name__ == '__main__':
    # app.run(debug=True) # if you want to run this as a standalone script, use this
    # gui.run()
    t = Thread(target=run)
    t.start()

    # Create a borderless webview window
    webview.create_window("My Flask App", "http://127.0.0.1:5000", frameless=True, width=200, height=100)
    webview.start()
