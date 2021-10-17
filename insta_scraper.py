from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from http.client import RemoteDisconnected
import bs4
import os
import requests
import re
import urllib

DOMAIN_BASE = "https://www.instagram.com/"
CHROMEDRIVER = "path"
LOGIN_ID = "your_instaid"
PASSWORD = "your_password"
DIRECTORY = "directory_pass"
MAXPOSTCOUNT = max_post_count


def get_driver():
    #　ヘッドレスモードでブラウザを起動
    options = Options()
    options.add_argument('--headless')
    # ブラウザーを起動
    driver = webdriver.Chrome(CHROMEDRIVER, options=options)
    return driver


def do_login(driver):
    # ログインURL
    login_url = DOMAIN_BASE + "accounts/login/"
    driver.get(login_url)
    # 電話、メールまたはユーザー名のinput要素が読み込まれるまで待機（最大10秒）
    elem_id = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )

    try:
        # パスワードのinput要素
        elem_password = driver.find_element_by_name("password")
        if elem_id and elem_password:
            # ログインID入力
            elem_id.send_keys(LOGIN_ID)
            # パスワード入力
            elem_password.send_keys(PASSWORD)
            # ログインボタンクリック
            elem_btn = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(elem_btn)
            actions.click(elem_btn)
            actions.perform()
            # 適当（3秒間待つように対応しています）
            time.sleep(3)
            # 遷移
            # 遷移後のURLでログイン可否をチェック
            perform_url = driver.current_url
            if perform_url.find(login_url) == -1:
                # ログイン成功
                return True
            else:
                # ログイン失敗
                return False
        else:
            return False
    except:
        return False


# 最後の要素までスクロール
def scroll_to_elem(driver, footer_move_flg):
    try:
        if footer_move_flg:
            last_elem = driver.find_element_by_id("fb-root")

            actions = ActionChains(driver)
            actions.move_to_element(last_elem)
            actions.perform()
        else:
            # 最後の要素の一つ前までスクロール
            elems = driver.find_elements_by_class_name("weEfm")
            last_elem = elems[-1]

            actions = ActionChains(driver)
            actions.move_to_element(last_elem)
            actions.perform()

        return True
    except:
        return False


if __name__ == "__main__":
    # Driver
    driver = get_driver()
    # ログイン
    login_flg = do_login(driver)
    #スクレイピングしたいユーザーのアカウントのURL
    url = "user_name_you_want_to_scraiping"
    driver.get(url)
    time.sleep(2)
  
    #変数宣言
    hrefList = []
    num = 0
    count_info = 0

    # 全部の投稿のhref属性を取得するコード
    while count_info < MAXPOSTCOUNT:
        #aタグの要素を取得
        #その中のhref属性　pタグを取得
        #リストの中に重複要素が出ないように処理
        mediaList = driver.find_elements_by_tag_name("a")
        for media in mediaList:
            href = media.get_attribute("href")
            if "/p/" in href:
                if not href in hrefList:
                    hrefList.append(href)
        count_info = len(hrefList)
        time.sleep(1)
        print(count_info)
        result_flg = scroll_to_elem(driver, False)
        time.sleep(1)    
    # 画像のhrefを格納した配列でループ処理
    print(len(hrefList))
    for x in hrefList:
         print(x)
    for href in hrefList:
        driver.get(href)
        time.sleep(2)
        # 同じ投稿に画像がある限りその画像を取得する処理。
        # 同じ投稿に画像がなくなった場合次の投稿に行く
        while len(driver.find_elements_by_class_name("_6CZji")) > 0:
            num += 1
            driver.find_elements_by_class_name("_6CZji")[0].click()
            time.sleep(3)
            photo = driver.find_elements_by_class_name(
                "FFVAD")[0].get_attribute("src")
            #ファイルの名前決める
            urllib.request.urlretrieve(
                photo, DIRECTORY + 'hoge' + str(num) + '.png')
    driver.quit()
