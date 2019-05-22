from app import app
from app.whois import query_whois
from flask import render_template, jsonify, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/whois/<path:query>')
def whois(query):
    print(request.headers['Accept'])
    data = query_whois(query)
    return render_template('whois_response.html', data=data, title='WHOIS Result')

@app.route('/api/v1/query_whois', methods=['POST'])
def api_v1_query_whois():
    query = request.json['query']
    res = {
        'raw_whois': query_whois(query)
    }
    return jsonify(res)