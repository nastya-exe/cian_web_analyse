import sqlite3

from datetime import date
from config import database_url


# Кол-во объявлений за сегодня
def number_ads_today(url, metro=None, price=None, rooms=None, type_premises=None):
    today_str = date.today().isoformat()
    db = sqlite3.connect(url)
    cursor = db.cursor()
    act = ''

    if metro:
        act += f' AND name_metro = "{metro}"'
    if price:
        act += f' AND price <= {price}'
    if rooms:
        act += f' AND num_rooms = {rooms}'
    if type_premises:
        act += f' AND type_room = "{type_premises}"'

    query = f"""
        SELECT count(id) FROM info_studios
        WHERE DATE(date_add) = "{today_str}"{act}
    """

    cursor.execute(query)
    rows = cursor.fetchone()
    db.close()
    return rows[0]

print(number_ads_today(database_url))


# Кол-во всех/активных объявлений
def all_ads(url, active, metro=None, price=None, rooms=None, type_premises=None):
    db = sqlite3.connect(url)
    cursor = db.cursor()

    act = 'WHERE active = 1' if active else ''
    if metro:
        act += f' AND name_metro = "{metro}"'
    if price:
        act += f' AND price <= {price}'
    if rooms:
        act += f' AND num_rooms = {rooms}'
    if type_premises:
        act += f' AND type_room = "{type_premises}"'

    query = f"""
        SELECT 
            COUNT(*) AS total
        FROM info_studios
        {act};
    """

    cursor.execute(query)
    rows = cursor.fetchone()
    db.close()
    return rows[0]


# Топ 5 мин макс объявлений по м2 активные и все объявления
def top_five_ads(url, max_min, active):
    db = sqlite3.connect(url)
    cursor = db.cursor()

    order = 'DESC' if max_min == 'max' else 'ASC'
    act = 'WHERE active = 1' if active else ''

    query = f"""
        SELECT 
            name_metro,
            ROUND(AVG(price_sq_meter), 0) AS avg_price
        FROM info_studios
        {act}
        GROUP BY name_metro
        ORDER BY avg_price {order}
        LIMIT 5;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows


# Кол-во разных типов помещений
def premises_quantity(url, active, metro=None, price=None, rooms=None, type_premises=None):
    db = sqlite3.connect(url)
    cursor = db.cursor()
    act = 'WHERE active = 1' if active else ''
    if metro:
        act += f' AND name_metro = "{metro}"'
    if price:
        act += f' AND price <= {price}'
    if rooms:
        act += f' AND num_rooms = {rooms}'
    if type_premises:
        act += f' AND type_room = "{type_premises}"'

    query = f"""
        SELECT 
            type_room,
            count(id) as count_id
        FROM info_studios
        {act}
        GROUP BY type_room
        ORDER BY count_id DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows


def histogram_info(url, active, metro=None, price=None, rooms=None, type_premises=None):
    db = sqlite3.connect(url)
    cursor = db.cursor()
    act = 'WHERE active = 1' if active else ''
    if metro:
        act += f' AND name_metro = "{metro}"'
    if price:
        act += f' AND price <= {price}'
    if rooms:
        act += f' AND num_rooms = {rooms}'
    if type_premises:
        act += f' AND type_room = "{type_premises}"'

    query = f"""
        SELECT
        CASE 
            WHEN price < 40000 THEN '< 40'
            WHEN price BETWEEN 40000 AND 59999 THEN '40-60'
            WHEN price BETWEEN 60000 AND 79999 THEN '60-80'
            WHEN price BETWEEN 80000 AND 99999 THEN '80-100'
            WHEN price BETWEEN 100000 AND 119999 THEN '100-120'
            WHEN price BETWEEN 120000 AND 139999 THEN '120-140'
            WHEN price BETWEEN 140000 AND 159999 THEN '140-160'
            WHEN price BETWEEN 160000 AND 179999 THEN '160-180'
            WHEN price BETWEEN 180000 AND 199999 THEN '180-200'
            WHEN price BETWEEN 200000 AND 299999 THEN '200-300'
            WHEN price BETWEEN 300000 AND 499999 THEN '300-500'
            WHEN price BETWEEN 500000 AND 699999 THEN '500-700'
            WHEN price BETWEEN 700000 AND 899999 THEN '700-900'
            ELSE '> 900'
        END AS price_range,
        COUNT(*) AS count_ads
        FROM info_studios
        {act}
        GROUP BY price_range
        ORDER BY 
            MIN(price);
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows


def all_name_metro(url):
    db = sqlite3.connect(url)
    cursor = db.cursor()
    cursor.execute("""
        SELECT
        DISTINCT(name_metro)
        FROM info_studios
        ORDER BY name_metro
    """, )
    rows = cursor.fetchall()
    return rows
