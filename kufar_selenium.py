import os
import threading
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parsers import parser_chats

import pickle
from fake_useragent import UserAgent


def accept_cookie(driver, username):
    accept_button = driver.find_element(By.XPATH, '//button[text()="Принять"]')
    if accept_button:
        accept_button.click()
        print(f"{username}: accept cookie (button)")


def save_cookie(driver, username):
    with open(f'cookies/{username}_cookies.pickle', 'wb') as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookie(driver, username):
    with open(f'cookies/{username}_cookies.pickle', 'rb') as f:
        for cookie in pickle.load(f):
            driver.add_cookie(cookie)
    print(f'{username}: load cookie')


def login(driver, username, password):
    try:
        wait = WebDriverWait(driver, 10)

        login_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
        login_input.clear()
        login_input.send_keys(username)
        print(f'{username}: Entered username')

        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys(password)
        print(f'{username}: Entered password')

        password_input.send_keys(Keys.ENTER)
        print(f'{username}: Logging in...')

    except TimeoutException:
        print(f"{username}:Element did not show up")


def get_all_chats(driver, username):
    print(f'{username}: go to /messaging/')
    driver.get("https://www.kufar.by/account/messaging/")
    print(f'{username}: get and sleep 3 sec')

    time.sleep(3)
    # Прокрутите страницу до элемента
    try:
        # Найти элемент ul внутри styles_menu-conversations-list__n7m8b
        chats_element = driver.find_element(By.CSS_SELECTOR, ".styles_menu-conversations-list__n7m8b ul")

        # Получаем высоту элемента ul
        ul_height = driver.execute_script("return arguments[0].scrollHeight", chats_element)
        # print(f'ul height {ul_height}')
        # Прокручиваем до конца
        while True:
            # Прокручиваем элемент ul
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chats_element)

            # Подождать некоторое время, чтобы содержимое успело подгрузиться
            time.sleep(2)
            print('scroll chats for load')
            # Получаем новую высоту элемента ul после прокрутки
            new_ul_height = driver.execute_script("return arguments[0].scrollHeight", chats_element)
            # print(f'new ul height {new_ul_height}')

            # Если высота не изменилась, значит мы достигли конца списка
            if new_ul_height == ul_height:
                break
                print(f'{username}: scroll end...')

            # Обновляем высоту элемента ul
            ul_height = new_ul_height
        time.sleep(3)
    finally:
        # Закрыть браузер после выполнения
        pass
    # Прокрутка страницы
    chats = driver.find_element(By.XPATH, '//div[@class="styles_menu-conversations-list__n7m8b"]')
    chats_html = chats.get_attribute("outerHTML")
    # Сохраните содержимое страницы в файл

    with open(f'chats/{username}_chats.html', 'w', encoding='utf-8') as f:
        f.write(str(chats_html))
    parser_chats(username=username)
    print(f'{username}: chats_save')


def session(username, password):
    url = 'https://www.kufar.by/login'
    user_agent = UserAgent()
    print(user_agent.random)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = 'normal'
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument(f"--user-agent={user_agent.random}")

    driver = webdriver.Chrome(options=chrome_options)
    print(f'{username}: start...')
    driver.get(url)

    time.sleep(2)
    #
    accept_cookie(driver, username)

    if not os.path.exists(f"{username}_cookies.pickle"):
        print(f'{username}: cookie is not exists')
        login(driver=driver, username=username, password=password)
        driver.refresh()
        time.sleep(3)
        save_cookie(driver=driver, username=username)
    else:
        print(f'{username}: cookie is exists')
        # Если файл cookie есть, загружаем его
        load_cookie(drive=driver, username=username)
        print(f'{username}: reload page')
        driver.get(url)

    get_all_chats(driver, username)

    # print('sleep 5 sec')
    # driver.get(f"https://www.kufar.by/account/messaging/{chat_id}")
    # time.sleep(5)
    # textarea = driver.find_element(By.XPATH,'//textarea[@name="message_textarea"]')
    # textarea.clear()
    # textarea.send_keys('!!!')
    # textarea.send_keys(Keys.ENTER)
    # time.sleep(10)
    # print('отправил сообщение')
    # print('end...')


def main():
    accounts = [
        {"username": "raman.kutuzau@gmail.com", "password": "12345Hacintosh09876!"},
        {"username": "roman.kutuzov@deltaunion.by", "password": "12345Hacintosh09876!"},
        # Добавьте другие аккаунты по мере необходимости
    ]

    threads = []
    for account in accounts:
        thread = threading.Thread(target=session, args=(account["username"], account["password"]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
