from app import app
from app.whois import query_whois
from flask import render_template, jsonify, request, Response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/swagger.json')
def swagger():
    return app.send_static_file('swagger.json')

@app.route('/whois/<path:query>')
def whois(query):
    print(request.headers['Accept'])
    data = query_whois(query)
    return render_template('whois_response.html', data=data, title='WHOIS Result')

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