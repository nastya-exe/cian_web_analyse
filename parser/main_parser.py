import time
import traceback
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options

from db_rrequests import find_active_ads, save_info_db, change_status_active, data_change
from config import url_new, database_url
from functions import datetime_of_publication, payment_upon_entry, type_housing


def extract_hrefs(links):
    hrefs = []
    for link in links:
        try:
            href = link.get_attribute("href")
            if href:
                hrefs.append(href)
        except StaleElementReferenceException:
            continue
    return hrefs


def find_links(driver, pages=5):
    hrefs = []

    for page in range(1, pages + 1):
        try:
            links = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'media')]"))
            )
        except TimeoutException:
            print(f"Не нашлось на стр {page}")
            break

        # добавляем ссылки
        hrefs += extract_hrefs(links)
        print(f"Всего {len(hrefs)} ссылок после стр. {page}")

        # переход на сл старницу
        if page < pages:
            try:
                next_page = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//a[@rel='noopener' and span[text()='{page + 1}']]"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                time.sleep(1)
                next_page.click()
                time.sleep(2)
            except Exception:
                print(f"Не перешло на страницу {page + 1}")
                break

    return hrefs


def parser(driver, url):
    driver.get(url)

    hrefs = find_links(driver, 5)
    active_ads = find_active_ads()
    count = 0

    for href in hrefs:
        # Добавление новых объявлений в бд
        if href not in active_ads:
            try:
                if "объявление снято с публикации" in driver.page_source.lower() or "страница не найдена" in driver.page_source.lower():
                    print(f"снято с публикации: {href}")
                    continue
                driver.get(href)

                # Название объявления (кол-во комнат, тип жилья, площадь)
                name = driver.find_element(By.CSS_SELECTOR, "div[data-name='OfferTitleNew'] h1").text
                name_list = name.split()

                # Цена и оплата при заселении
                price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='price-amount'] span"))
                )

                price_int = int(''.join(num for num in price.text if num.isdigit()))

                payment_info = driver.find_elements(By.CSS_SELECTOR, "div[data-name='OfferFactItem'] span")
                payment = payment_upon_entry(payment_info[3].text, payment_info[5].text, payment_info[7].text,
                                             price_int)

                # Название ближайшего метро, время до не него, тип передвижения
                underground_items = driver.find_elements(By.CSS_SELECTOR, "li[data-name='UndergroundItem']")

                name_metro = underground_items[0].find_element(By.CSS_SELECTOR, "a")
                time_elem = underground_items[0].find_element(By.CSS_SELECTOR,
                                                              "span[data-name='UndergroundTime'], span[class*='underground_time']")
                time_elem_int = int(time_elem.text.split(' ')[0])

                svg_elem = time_elem.find_element(By.TAG_NAME, "svg")
                paths = svg_elem.find_element(By.TAG_NAME, "path")
                icon_type = "транспорт" if paths.get_attribute("fill-rule") == "evenodd" else "пешком"

                # Площадь квартиры и цена за м2
                square_float = float(name_list[-2].replace(',', '.'))
                price_sq_meter = round(price_int / square_float, 2)

                # Кол-во комнат и тип квартиры
                type_room = type_housing(name_list)[0]
                num_rooms = type_housing(name_list)[1]

                # Время последнего обновления объявления
                last_update = (driver.find_elements(By.CSS_SELECTOR, "div[data-testid='metadata-updated-date'] span"))[
                    0]
                date_time_obj = datetime_of_publication(last_update.text)

                save_info_db(price_int, name_metro.text, href, date_time_obj, payment, time_elem_int, icon_type,
                             square_float, price_sq_meter, num_rooms, type_room)
                count += 1
                print(f'добавлено {count}')

            except Exception as e:
                print(f'Ссылка {href}, ошибка {e}')
                print(traceback.format_exc())
                continue


# Обновление данных в бд в 15:00 и 20:00
def update_add(driver, hrefs):
    time_now = datetime.now().time().strftime("%H:%M")
    num_act = 0
    num_non_act = 0

    if '14:50' <= time_now < '15:00' or '20:00' <= time_now < '20:10':

        for href in hrefs:
            driver.get(href)
            if "объявление снято с публикации" in driver.page_source.lower() or "страница не найдена" in driver.page_source.lower():
                print(f"снято с публикации: {href}")
                change_status_active(href)
                num_non_act += 1
                print(f'неактивные: {num_non_act}')
                continue

            try:
                # price = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='price-amount'] span"))
                # )
                # payment_info = driver.find_elements(By.CSS_SELECTOR, "div[data-name='OfferFactItem'] span")
                #
                # price_int = int(''.join(num for num in price.text if num.isdigit()))
                # payment = payment_upon_entry(payment_info[3].text, payment_info[5].text, payment_info[7].text,
                #                              price_int)
                #
                # name = driver.find_element(By.CSS_SELECTOR, "div[data-name='OfferTitleNew'] h1").text
                # square_float = float(name.split()[-2].replace(',', '.'))
                # price_sq_meter = round(price_int / square_float, 2)
                #
                # data_change(price_int, href, payment, price_sq_meter)

                num_act += 1
                print(f'активные: {num_act}')

            except Exception as e:
                print(f'Ссылка {href}, ошибка {e}')
                print(traceback.format_exc())
                continue

        print(f'обработано: {num_act + num_non_act}')


def start(url):
    while True:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # не грузить картинки

        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.stylesheets": 2,
            "profile.default_content_setting_values.media_stream": 2,
        })

        driver = webdriver.Chrome(options=chrome_options)

        update_add(driver, find_active_ads())
        parser(driver, url)
        driver.quit()
        time.sleep(600)


start(url_new)
