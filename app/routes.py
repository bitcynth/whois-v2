from app import app, app_version, app_supporters
from app.whois import query_whois
from flask import render_template, jsonify, request, Response, send_from_directory

@app.route('/')
def index():
    return render_template('index.html', version=app_version, supporters=app_supporters)

@app.route('/data/<path:path>', methods=['GET'])
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/whois/<path:query>')
def whois(query):
    accept = request.headers['Accept'].split(',')
    data = query_whois(query)
    if 'text/html' in accept:
        return render_template('whois_response.html', data=data, title='WHOIS Result')
    return Response(data, mimetype='text/plain')

@app.route('/whois', methods=['POST'])
def whois_post():
    if not 'query' in request.form:
        return 'error'
    query = request.form['query']
    data = query_whois(query)
    return render_template('whois_response.html', data=data, title='WHOIS Result')

@app.route('/api/v1/whois/query/<query>', methods=['GET'])
def api_v1_query_whois_get(query):
    res = query_whois(query)
    return Response(res, mimetype='text/plain')

@app.route('/api/v1/whois/query', methods=['POST'])
def api_v1_query_whois():
    query = request.json['query']
    res = {
        'raw': query_whois(query)
    }
    return jsonify(res)
