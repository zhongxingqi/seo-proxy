from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'endpoints': ['/search', '/rank', '/keyword']})

@app.route('/search')
def search():
    keyword = request.args.get('keyword', 'test')
    try:
        response = requests.get(
            f'https://www.google.com/search?q={keyword}&num=100',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            timeout=30
        )
        html = response.text
        results = []
        for match in re.finditer(r'href="/url\?q=([^"&]+)', html):
            link = match.group(1)
            if link.startswith('http') and 'google.com' not in link:
                results.append({'url': link})
        return jsonify({'keyword': keyword, 'total': len(results), 'results': results[:100]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
