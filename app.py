from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
        }
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Try to find product title, price, and image
        title = soup.select_one('#productTitle')
        title = title.text.strip() if title else ''

        price = soup.select_one('#corePrice_feature_div .a-offscreen')
        if not price:
            price = soup.select_one('.a-price .a-offscreen')
        price = price.text.strip() if price else ''

        image = soup.select_one('#landingImage')
        if not image:
            img_tag = soup.select_one('#imgTagWrapperId img')
            image = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''
        else:
            image = image['src']

        return jsonify({
            'title': title,
            'price': price,
            'image': image
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "API is working!"
