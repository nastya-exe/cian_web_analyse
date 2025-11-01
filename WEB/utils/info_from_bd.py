import sqlite3

from datetime import date
from config import database_url


# Кол-во объявлений за сегодня
def number_ads_today(url):
    today_str = date.today().isoformat()
    db = sqlite3.connect(url)
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
    db = sqlite3.connect(url)
    cursor = db.cursor()

    cursor.execute("""
        SELECT count(id) FROM info_studios
        WHERE active = 1
    """, )

    row_count = cursor.fetchone()[0]
    db.close()

    return row_count


# Топ 5 мин макс объявлений по м2
def top_five_ads(url, max_min):
    db = sqlite3.connect(url)
    cursor = db.cursor()

    if max_min == 'max':
        cursor.execute("""
            SELECT 
                name_metro,
                ROUND(AVG(price_sq_meter), 0) AS avg_price
            FROM info_studios
            GROUP BY name_metro
            ORDER BY avg_price DESC
            LIMIT 5;
        """, )
    elif max_min == 'min':
        cursor.execute("""
            SELECT 
                name_metro,
                ROUND(AVG(price_sq_meter), 0) AS avg_price
            FROM info_studios
            GROUP BY name_metro
            ORDER BY avg_price
            LIMIT 5;
        """, )

    rows = cursor.fetchall()
    return rows


# Кол-во разных типов помещений
def premises_quantity(url):
    db = sqlite3.connect(url)
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            type_room,
            count(id) as count_id
        FROM info_studios
        GROUP BY type_room
        ORDER BY count_id DESC
    """, )

    rows = cursor.fetchall()
    return rows


def histogram_info(url):
    db = sqlite3.connect(url)
    cursor = db.cursor()

    cursor.execute("""
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
            ELSE '> 500'
        END AS price_range,
        COUNT(*) AS count_ads
    FROM info_studios
    GROUP BY price_range
    ORDER BY 
        MIN(price);
    """, )

    rows = cursor.fetchall()
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
