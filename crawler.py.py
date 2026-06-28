from playwright.sync_api import sync_playwright

class UniversalCrawler:
    def fetch_data(self, url, config):
        with sync_playwright() as p:
            # 브라우저 실행 설정
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()
            
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # 설정된 CSS 셀렉터에 따라 정보 수집
                data = {
                    "name": page.locator(config['name']).inner_text() if page.locator(config['name']).count() > 0 else "이름 없음",
                    "price": page.locator(config['price']).inner_text() if page.locator(config['price']).count() > 0 else "가격 확인 불가",
                    "origin": page.locator(config['origin']).inner_text() if config.get('origin') else "정보 없음",
                    "shipping": page.locator(config['shipping']).inner_text() if config.get('shipping') else "무료"
                }
            except Exception as e:
                data = {"error": f"수집 실패: {str(e)}"}
            
            browser.close()
            return data