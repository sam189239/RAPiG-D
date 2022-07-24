from flask import Flask, Response, request, render_template, make_response, stream_with_context
import requests
import json
import time
from datetime import datetime
import random

app = Flask(__name__)

step = 0
ep = 0
m = [0,0,0,0,0,0,0,0,0]
action = 'Default'

@app.route("/", methods=['POST'])
def post_data():
	global step, ep, m, action
	step = request.form.get('step')
	ep = request.form.get('ep')
	m = request.form.get('m')
	action = request.form.get('action')


# @app.route("/", methods=['GET'])
# def get_data():
# 	global out
# 	return Response('{}'.format(out))

@app.route('/')
def index():
	return render_template('index.html', step=step, ep=ep, m=m, action=action)


@app.route('/data', methods=["GET", "POST"])
def data():
    # Using Static data
    #data = [time() * 1000, random() * 100]


    data = [ep,step]
    print(data)

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port = 8000)





