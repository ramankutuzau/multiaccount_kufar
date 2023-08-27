import os
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

import parsers


def accept_cookie(driver):
    accept_button = driver.find_element(By.XPATH, '//button[text()="Принять"]')
    if accept_button:
        accept_button.click()
        print("accept cookie")

def save_cookie(driver):
    with open('cookies.pickle', 'wb') as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookie(driver):
    with open('cookies.pickle', 'rb') as f:
        for cookie in pickle.load(f):
            driver.add_cookie(cookie)
    print('load cookie')

def login(driver, username, password):
    try:
        wait = WebDriverWait(driver, 10)

        login_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
        login_input.clear()
        login_input.send_keys(username)
        print('Entered username')

        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.clear()
        password_input.send_keys(password)
        print('Entered password')

        password_input.send_keys(Keys.ENTER)
        print('Logging in...')

    except TimeoutException:
        print("Element did not show up")

def get_all_chats(driver):
    print('go to /messaging/')
    driver.get("https://www.kufar.by/account/messaging/")
    print('get and sleep 3 sec')

    time.sleep(3)
    # Прокрутите страницу до элемента
    try:
        wait = WebDriverWait(driver, 10)

        # Найти элемент ul внутри styles_menu-conversations-list__n7m8b
        chats_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_menu-conversations-list__n7m8b ul"))) # main scroller chat


        # Получаем высоту элемента ul
        ul_height = driver.execute_script("return arguments[0].scrollHeight", chats_element)
        # print(f'ul height {ul_height}')
        # Прокручиваем до конца
        while True:
            # Прокручиваем элемент ul
            script = "arguments[0].scrollTop = arguments[0].scrollHeight"
            # Подождать некоторое время, чтобы содержимое успело подгрузиться
            var = wait.until(EC.presence_of_element_located(chats_element)).location_once_scrolled_into_view
            driver.execute_script(script, element)

            print('scroll chats for load')

            # Получаем новую высоту элемента ul после прокрутки
            new_ul_height = driver.execute_script("return arguments[0].scrollHeight", chats_element)
            # print(f'new ul height {new_ul_height}')

            # Если высота не изменилась, значит мы достигли конца списка
            if new_ul_height == ul_height:
                break
                print('scroll end...')

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

    with open('chats.html', 'w', encoding='utf-8') as f:
        f.write(str(chats_html))
    parser_chats()
    print('chats_save')

    # for el in elements:
    #     print(f"chat id : {el.get_attribute('data-conversation-id')}")
    #
    # chat_id = elements[2].get_attribute('data-conversation-id')
    #


def main():
    url = 'https://www.kufar.by/login'
    user_agent = UserAgent()
    print(user_agent.random)
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.page_load_strategy = 'normal'
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument(f"--user-agent={user_agent.random}")


    driver = webdriver.Chrome(options=chrome_options)
    print('start...')
    driver.get(url)

    time.sleep(2)
    #
    accept_cookie(driver)

    if not os.path.exists("cookies.pickle"):
        print('cookie is not exists')
        username = "raman.kutuzau@gmail.com"
        password = "12345Hacintosh09876!"
        login(driver=driver,username=username,password=password)
        driver.refresh()
        time.sleep(3)
        save_cookie(driver)
    else:
        print('cookie is not exists')
        # Если файл cookie есть, загружаем его
        load_cookie(driver)
        print('reload page')
        driver.get(url)



    get_all_chats(driver)

    # print('accept cookie')



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




if __name__ == "__main__":
    main()



