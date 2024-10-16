import requests
from bs4 import BeautifulSoup

def scrape_iwate_bousai():
    url = "https://iwate-bousai.my.salesforce-sites.com/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 緊急情報を取得
        info_area = soup.find('div', class_='contBox', id='infoArea')
        # print(info_area)
        
        if info_area:
            title = info_area.find('h2').text.strip() if info_area.find('h2') else "タイトルなし"
            
            emergency_info = info_area.find('span', class_='nullResult')
            if emergency_info:
                content = emergency_info.text.strip()
            else:
                content = "緊急情報の内容が見つかりません"
        else:
            title = "緊急情報セクションが見つかりません"
            content = "緊急情報セクションが見つかりません"
        
        # 結果を辞書として返す
        result = {
            "title": title,
            "content": content
        }
        
        return result
    else:
        return {"error": f"Failed to retrieve the webpage. Status code: {response.status_code}"}
