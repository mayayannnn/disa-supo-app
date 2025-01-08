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
    
def scrape_terebi_saigai():
    url = "https://www.tvi.jp/weather/disaster"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all("td")
    # contents = []
    # tables = soup.find_all('table')
    # result = {}
    # for table in tables:
    #     ths = table.find_all("th")
    #     lists = table.find_all("li")
    #     for th in ths:
    #         title = th.get_text()
    #     for list in lists:
    #         content = list.get_text()
    #     result[title] = content
    #     contents.append(content)
    # print(result)
    # # print(ths)
    # # print(lists)
    # # count = 0

    # # result["タイトル"] = "水警報"
    # # # for th in ths:
    # # #     count = count + 1
    # # #     result[th] = lists[count]
    # # # return result
    
    

    # # # result[list.get_th()] = list.get_text()
    print(results)
    return results

scrape_terebi_saigai()