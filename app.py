import csv
from io import StringIO
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from crawler import UniversalCrawler

app = Flask(__name__)
CORS(app)

# 수집된 데이터를 메모리에 저장하는 리스트
scraped_data_list = []

@app.route('/api/scrape', methods=['POST'])
def scrape_and_calculate():
    data = request.json
    url = data.get('productUrl')
    cost = float(data.get('cost', 0))
    margin = float(data.get('margin', 0.1))
    
    crawler = UniversalCrawler()
    # 수집 규칙 정의
    config = {'name': 'h2', 'price': '.total-price', 'origin': '.prod-attr-item', 'shipping': '.delivery-fee'}
    info = crawler.fetch_data(url, config)
    
    # 추천 판매가 계산 (환율 1380원, 수수료 15% 가정)
    usd_price = (cost * (1 + margin)) / (1380 * (1 - 0.15))
    
    result = {
        "info": info,
        "recommended_usd_price": round(usd_price, 2)
    }
    scraped_data_list.append(result)
    return jsonify(result)

@app.route('/api/download', methods=['GET'])
def download_csv():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['상품명', '추천판매가(USD)', '원산지', '배송비'])
    for d in scraped_data_list:
        info = d.get('info', {})
        cw.writerow([info.get('name'), d.get('recommended_usd_price'), info.get('origin'), info.get('shipping')])
    
    return Response(si.getvalue(), mimetype='text/csv', 
                    headers={"Content-Disposition": "attachment;filename=ebay_products.csv"})

if __name__ == '__main__':
    app.run()
