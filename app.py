from flask import Flask, jsonify, request
from flask_cors import CORS
from crawler import UniversalCrawler

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['POST'])
def scrape_and_calculate():
    data = request.json
    url = data.get('productUrl')
    cost = float(data.get('cost', 0))
    margin = float(data.get('margin', 0.1))
    
    # 1. 크롤링 수행
    crawler = UniversalCrawler()
    # 쿠팡용 규칙 (실제 사이트 구조에 따라 조정 가능)
    config = {'name': 'h2', 'price': '.total-price', 'origin': '.prod-attr-item', 'shipping': '.delivery-fee'}
    info = crawler.fetch_data(url, config)
    
    # 2. 역직구 가격 계산 로직 (환율 1380원, 수수료 15% 가정)
    usd_price = (cost * (1 + margin)) / (1380 * (1 - 0.15))
    
    return jsonify({
        "info": info,
        "recommended_usd_price": round(usd_price, 2)
    })

if __name__ == '__main__':
    app.run()
