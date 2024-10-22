from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Chromeドライバーのセットアップ
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URLにアクセス
url = "https://iwate-bousai.my.salesforce-sites.com/PUB_VF_Index#/shelter-congestion-map?poi=false&city-code=201"
driver.get(url)

# 必要なデータを取得
# ページのタイトルを取得
title = driver.title
print(title)

# 特定のクラス名を持つすべての要素を取得
elements = driver.find_element(By.CSS_SELECTOR, ".css-1gfd10d-shelter-congestion-map-shelters-CShelters")


if elements:
    # 各要素のテキストを表示
    for element in elements:
        print(element.text)
else:
    print("要素が見つかりませんでした")


# ブラウザを閉じる
driver.quit()