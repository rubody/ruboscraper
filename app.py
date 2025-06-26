from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return jsonify({'title': '', 'price': '', 'image': '', 'debug_status': f'HTTP {resp.status_code}'})
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Amazon
        title = soup.select_one('#productTitle')
        price = soup.select_one('.a-price .a-offscreen')
        image = soup.select_one('#landingImage') or soup.select_one('#imgTagWrapperId img')

        return jsonify({
            'title': title.text.strip() if title else '',
            'price': price.text.strip() if price else '',
            'image': image['src'] if image and image.has_attr('src') else ''
        })
    except Exception as e:
        return jsonify({'title': '', 'price': '', 'image': '', 'debug_status': str(e)})

@app.route('/', methods=['GET'])
def home():
    return "RuboShipping Scraper Running!"
