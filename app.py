from flask import Flask, jsonify, request
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
# 모든 접근을 허용하는 설정
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('productUrl')
        cost = float(data.get('cost', 10000))
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            name = page.locator("h2").first.inner_text()
            browser.close()
            
        return jsonify({"info": {"name": name}, "recommended_usd_price": round(cost / 1300, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
