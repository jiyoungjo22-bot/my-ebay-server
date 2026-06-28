from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from playwright.sync_api import sync_playwright
import csv
from io import StringIO

app = Flask(__name__)
CORS(app)

scraped_data_list = []

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data.get('productUrl')
        cost = float(data.get('cost', 0))
        margin = float(data.get('margin', 0.15))
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            
            # 셀렉터 오류 방지용 안전 코드
            name = page.locator("h2").first.inner_text() 
            price = "확인필요"
            
            browser.close()
            
        result = {"info": {"name": name, "price": price}, "recommended_usd_price": round((cost * (1 + margin)) / 1300, 2)}
        scraped_data_list.append(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['상품명', '판매가'])
    for d in scraped_data_list:
        cw.writerow([d['info']['name'], d['recommended_usd_price']])
    return Response(si.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=data.csv"})

if __name__ == '__main__':
    app.run()
