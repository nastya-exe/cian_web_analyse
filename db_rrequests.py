import sqlite3
from config import database_url


# Добавление объявления в бд
def save_info_db(price, name_metro, link, date_add, payment, time_metro,
                 type_transportation, square, price_sq_meter, num_rooms, type_room):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO info_studios(price, name_metro, link, 
            date_add, payment, time_metro, type_transportation, square, price_sq_meter, num_rooms, type_room)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(link) DO UPDATE SET
            price=excluded.price,
            name_metro=excluded.name_metro,
            link=excluded.link,
            date_add=excluded.date_add,
            payment=excluded.payment,
            time_metro=excluded.time_metro,
            type_transportation=excluded.type_transportation
    """, (price, name_metro, link, date_add, payment, time_metro,
          type_transportation, square, price_sq_meter, num_rooms, type_room))

    db.commit()
    db.close()


# Список ссылок из всех активных ссылок
def find_active_ads():
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        SELECT link FROM info_studios
        WHERE active = TRUE
    """)

    rows = [row[0] for row in cursor.fetchall()]
    db.close()

    return rows


# Изменение статуса активности объявления
def change_status_active(link):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        UPDATE info_studios
        SET active = FALSE
        WHERE link = ?
    """, (link,))

    db.commit()
    db.close()


# Изменение данных объявления
def data_change(price_new, link, payment_new, price_sq_meter_new):
    db = sqlite3.connect(database_url)
    cursor = db.cursor()

    cursor.execute("""
        UPDATE info_studios
        SET price = ?, payment = ?, price_sq_meter = ?
        WHERE link = ?
    """, (price_new, payment_new, price_sq_meter_new, link))

    db.commit()
    db.close()