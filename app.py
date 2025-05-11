from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)

latest = {"lat": None, "lon": None, "time": None, "speed": None}

@app.route('/log', methods=['GET', 'POST'])
def log_location(): 
	data = request.args.to_dict() 
	if request.method == 'POST': 
		json_body = request.get_json(silent=True) or {} 
		data.update({k: v for k, v in json_body.items() if k in ['lat', 'lon', 'longitude', 'time', 's', 'speed']})

	lat = data.get('lat')
	lon = data.get('longitude') or data.get('lon')
	if not lat or not lon:
		return jsonify({"error": "missing lat/lon", "received": data}), 400

	latest.update({
    "lat": float(lat),
    "lon": float(lon),
    "time": data.get('time'),
    "speed": data.get('s') or data.get('speed')
	})
	return jsonify({"status": "logged"}), 200

@app.route('/location', methods=['GET']) 
def get_location(): 
	if latest["lat"] is None: 
		return jsonify({"error": "no data"}), 404
	return jsonify(latest)
@app.route('/')
def homr():
	return render_template("index4.html")
if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=5000)

