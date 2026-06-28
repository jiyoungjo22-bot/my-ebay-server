from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from playwright.sync_api import sync_playwright
import csv
from io import StringIO
import traceback

app = Flask(__name__)
CORS(app)

scraped_data_list = []

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('productUrl')
        # ... 크롤링 로직 ...
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            name = page.locator("h2").first.inner_text() 
            browser.close()
            
        result = {"info": {"name": name}, "recommended_usd_price": 100}
        scraped_data_list.append(result)
        return jsonify(result)
    except Exception:
        # 에러 발생 시 상세 내용을 서버 로그에 출력
        print(traceback.format_exc())
        return jsonify({"error": "서버 내부 오류 발생"}), 500

@app.route('/api/download', methods=['GET'])
def download():
    # ... 동일 ...
    return Response("test", mimetype='text/csv')

if __name__ == '__main__':
    app.run()
