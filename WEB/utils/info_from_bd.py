# import seaborn as sns
import sqlite3

from datetime import date
from config import database_url


# Кол-во объявлений за сегодня
def number_ads_today(url):
    today_str = date.today().isoformat()
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        SELECT count(id) FROM info_studios
        WHERE DATE(date_add) = ? AND active = 1
    """, (today_str,))

    row_count = cursor.fetchone()[0]
    db.close()

    return row_count


# Кол-во активных объявлений
def number_active_ads(url):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        SELECT count(id) FROM info_studios
        WHERE active = ?
    """, (1,))

    row_count = cursor.fetchone()[0]
    db.close()

    return row_count


# Кол-во объявлений минимальной цены + 10%
def number_min_or_max_ads(url, min_or_max:str):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    if min_or_max == 'min':
        cursor.execute("""
            SELECT count(id) FROM info_studios
            WHERE active = 1 AND price <= (
                SELECT MIN(price) * 1.3 as price
                FROM info_studios
                WHERE active = 1
            )
        """,)
    elif min_or_max == 'max':
        cursor.execute("""
            SELECT count(id) FROM info_studios
            WHERE active = 1 AND price >= (
                SELECT MAX(price) * 0.9 as price
                FROM info_studios
                WHERE active = 1
            )
        """,)

    row_count = cursor.fetchone()[0]
    db.close()

    return row_count

# Процент от общей доли по разным типам квартир
def percents_types_house(url):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

# Процент 1,2,3 ,4 комн квартир среди всех квартир
    cursor.execute("""
        SELECT 
            num_rooms, 
            COUNT(num_rooms) as count_ads,
            ROUND(COUNT(num_rooms) * 100.0 / (
                SELECT COUNT(*)
                FROM info_studios
                WHERE type_room = 'квартира' AND active = 1
            ), 0) AS percent
        FROM info_studios
        WHERE type_room = 'квартира' AND active = 1
        GROUP BY num_rooms
    """, (1,))

    row_count = cursor.fetchone()[0]
    db.close()

    return row_count


print(number_min_or_max_ads(database_url, 'min'))
