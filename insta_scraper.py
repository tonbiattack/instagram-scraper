from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib.request

# 定数の定義
DOMAIN_BASE = "https://www.instagram.com/"
CHROMEDRIVER_PATH = "path_to_chromedriver"
LOGIN_ID = "your_instagram_id"
PASSWORD = "your_password"
DIRECTORY = "directory_path"
MAX_POST_COUNT = 100  # 例: 最大投稿数を100に設定

def get_driver():
    """Seleniumドライバーのインスタンスを初期化し、返却する関数。
    Chromeブラウザをヘッドレスモードで起動するためのオプションを設定する。"""
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    return driver

def do_login(driver):
    """Instagramにログインを試みる関数。
    ユーザー名とパスワードを入力し、ログインボタンをクリックする。
    ログイン成功の確認は、URLがログインページから変更されたかで判断する。"""
    login_url = DOMAIN_BASE + "accounts/login/"
    driver.get(login_url)
    try:
        elem_id = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        elem_password = driver.find_element_by_name("password")
        if elem_id and elem_password:
            elem_id.send_keys(LOGIN_ID)
            elem_password.send_keys(PASSWORD)
            login_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )
            login_button.click()
            time.sleep(3)
            return driver.current_url != login_url
    except:
        return False

def scroll_to_last_element(driver, footer_move_flag):
    """ページの最後までスクロールする関数。
    footer_move_flagがTrueの場合、ページの最下部までスクロールする。
    Falseの場合、ページ上の最後の要素までスクロールする。"""
    try:
        if footer_move_flag:
            last_elem = driver.find_element_by_id("fb-root")
        else:
            elems = driver.find_elements_by_class_name("weEfm")
            last_elem = elems[-1] if elems else None

        if last_elem:
            ActionChains(driver).move_to_element(last_elem).perform()
            return True
        return False
    except:
        return False

def scrape_posts(driver, user_url, max_post_count):
    """指定されたユーザーのInstagramページから投稿のURLを収集する関数。
    最大投稿数に達するまでページをスクロールし、各投稿のリンクをリストに保存する。"""
    driver.get(user_url)
    time.sleep(2)

    href_list = []
    while len(href_list) < max_post_count:
        media_list = driver.find_elements_by_tag_name("a")
        for media in media_list:
            href = media.get_attribute("href")
            if "/p/" in href and href not in href_list:
                href_list.append(href)
        print(len(href_list))
        scroll_to_last_element(driver, False)
        time.sleep(1)

    return href_list

def download_images(driver, href_list):
    """収集した投稿のURLから画像をダウンロードする関数。
    各投稿にアクセスし、画像をローカルに保存する。"""
    for num, href in enumerate(href_list, start=1):
        driver.get(href)
        time.sleep(2)
        while len(driver.find_elements_by_class_name("_6CZji")) > 0:
            driver.find_element_by_class_name("_6CZji").click()
            time.sleep(3)
            photo = driver.find_element_by_class_name("FFVAD").get_attribute("src")
            filename = f"{DIRECTORY}/image{num}.png"
            urllib.request.urlretrieve(photo, filename)

if __name__ == "__main__":
    driver = get_driver()
    if do_login(driver):
        user_url = "user_name_you_want_to_scrape"
        href_list = scrape_posts(driver, user_url, MAX_POST_COUNT)
        download_images(driver, href_list)
    driver.quit()
