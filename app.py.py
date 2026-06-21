from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "글로벌 역직구 대시보드 서버 정식 구동 중"

@app.route('/api/calculate', methods=['POST'])
def calculate_price():
    data = request.json
    cost = data.get('cost', 0)
    margin = data.get('margin', 0.1)
    
    # 환율 1380원, 이베이 수수료 15% 기준 역산
    usd_price = (cost * (1 + margin)) / (1380 * (1 - 0.15))
    return jsonify({"recommended_usd_price": round(usd_price, 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)