from flask import Flask, Response, request
import requests

app = Flask(__name__)

out = 'no_obj'

@app.route("/", methods=['POST'])
def post_data():
	global out
	out = request.form.get('obj')
	print("Received: {}".format(out))
	return out

@app.route("/", methods=['GET'])
def get_data():
	global out
	return Response('{}'.format(out))
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
