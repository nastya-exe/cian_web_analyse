import sqlite3

from datetime import date
from config import database_url


class InfoBd:
    def __init__(self, url, is_active=None, metro=None, price=None, rooms=None, type_premises=None):
        self.url = url
        self.is_active = is_active
        self.metro = metro
        self.price = price
        self.rooms = rooms
        self.type_premises = type_premises

    def _connect(self):
        return sqlite3.connect(self.url)

    def filters(self):
        filters = []

        if self.is_active:
            filters.append("active = 1" if self.is_active == 'yes' else "active in (0, 1)")
        if self.metro:
            filters.append(f'name_metro = "{self.metro}"')
        if self.price:
            filters.append(f'price <= {self.price}')
        if self.rooms:
            if str(self.rooms).isnumeric():
                filters.append(f'num_rooms = {self.rooms}')
            else:
                filters.append(f'num_rooms = "{self.rooms}"')
        if self.type_premises:
            filters.append(f'type_room = "{self.type_premises}"')

        return " AND ".join(filters) if filters else "1=1"

    # Кол-во объявлений за сегодня
    def number_ads_today(self):
        today_str = date.today().isoformat()
        act = self.filters()

        query = f"""
            SELECT count(id) FROM info_studios
            WHERE DATE(date_add) = '{today_str}' AND {act}
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchone()[0]

    # Кол-во всех/активных объявлений
    def all_ads(self):
        act = self.filters()

        query = f"""
            SELECT
                COUNT(*)
            FROM info_studios
            WHERE {act}
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchone()[0]

    # Топ 5 мин макс объявлений по м2 активные и все объявления
    def top_five_ads(self, max_min):
        act = self.filters()
        group = "" if self.metro else f"GROUP BY name_metro"

        if self.metro:
            path = f"""
            SELECT
                name_metro,
                ROUND(price_sq_meter, 0) AS avg_price
            FROM info_studios
            WHERE {act} 
            """
        else:
            path = f"""
            SELECT
                name_metro,
                ROUND(AVG(price_sq_meter), 0) AS avg_price
            FROM info_studios
            WHERE {act}
            {group}   
            """


        order = 'DESC' if max_min == 'max' else 'ASC'

        query = f"""
            {path}
            ORDER BY avg_price {order}
            LIMIT 5;
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    # Кол-во разных типов помещений
    def premises_quantity(self):
        act = self.filters()

        query = f"""
            SELECT
                type_room,
                count(id) as count_id
            FROM info_studios
            WHERE {act}
            GROUP BY type_room
            ORDER BY count_id DESC
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def histogram_info(self):
        act = self.filters()

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
            WHERE {act}
            GROUP BY price_range
            ORDER BY
                MIN(price);
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def all_name_metro(self):
        query = f"""
            SELECT
            DISTINCT(name_metro)
            FROM info_studios
            ORDER BY name_metro
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def heatmap(self, max_min):
        act = self.filters()
        order = 'DESC' if max_min == 'max' else 'ASC'

        query = f"""
            SELECT 
                ROUND(square / 5) * 5 AS square_group,
                ROUND(price / 5000) * 5 AS price_group,
                COUNT(*) AS count
            FROM info_studios
            WHERE {act}
            GROUP BY square_group, price_group
            ORDER BY price_group {order}
            LIMIT 5;
        """

        with self._connect() as db:
            cursor = db.cursor()
            cursor.execute(query)
            return cursor.fetchall()

q = InfoBd(database_url, metro='Шелепиха')
print(q.heatmap('max'))
print(q.heatmap('min'))





