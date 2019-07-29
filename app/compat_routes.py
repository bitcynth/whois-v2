from flask import Response
from app import app
from app.whois import query_whois
import re

COMMENTS_REGEX = re.compile('%.*')

@app.route('/whoistxt/<path:query>')
def plaintext_whois(query):
    res = query_whois(query)
    lines = res.split('\n')
    for line in lines:
        match = COMMENTS_REGEX.match(line)
        if match:
            lines.remove(line)
    res = '\n'.join(lines)
    return Response(res, mimetype='text/plain')