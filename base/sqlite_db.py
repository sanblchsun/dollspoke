from datetime import datetime
import sqlite3 as sq


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.con = sq.connect(database)
        self.con.row_factory = sq.Row
        self.cur = self.con.cursor()

    def start(self):
        with self.con:
            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS product(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 img TEXT NOT NULL,
                                 name TEXT NOT NULL,
                                 description TEXT NOT NULL,
                                 price TEXT NOT NULL,
                                 count TEXT NOT NULL,
                                 like INTEGER DEFAULT 0,
                                 dislike INTEGER DEFAULT 0,
                                 heard INTEGER DEFAULT 0);
                             """)
            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS customer(
                                 id INTEGER PRIMARY KEY,
                                 date TEXT NOT NULL,
                                 telefon TEXT,
                                 delivery TEXT,
                                 name TEXT,
                                 email TEXT,
                                 card TEXT);
                             """)
            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS prod_cust(
                                 prodict_id INTEGER NOT NULL,
                                 customer_id INTEGER NOT NULL,
                                 FOREIGN KEY (prodict_id) REFERENCES product(id),
                                 FOREIGN KEY (customer_id) REFERENCES customer(id));
                             """)
            self.cur.execute("""
                             CREATE TABLE IF NOT EXISTS info(
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 telefon TEXT DEFAULT None,
                                 full_name TEXT DEFAULT None,
                                 operating_mode TEXT DEFAULT None,
                                 delivery TEXT DEFAULT None);
                             """)
            self.cur.execute("INSERT OR IGNORE  INTO info ('id') VALUES (1)")

    async def sql_add_product(self, photo, name, description, price, count):
        with self.con:
            return self.cur.execute("INSERT INTO 'product' ("
                                    "img,"
                                    "name,"
                                    "description,"
                                    "price,"
                                    "count"
                                    ") VALUES(?,?,?,?,?)", (photo, name, description, price, count))

    async def sql_get_product(self, last=False):
        with self.con:
            if last:
                return self.cur.execute('SELECT * FROM product ORDER BY id DESC LIMIT 1;')
            return self.cur.execute('SELECT * FROM "product"')

    async def sql_del_product(self, id):
        with self.con:
            return self.cur.execute('DELETE FROM "product" WHERE `id` == ?', (id,))

    async def sql_get_info(self):
        with self.con:
            return self.cur.execute('SELECT * FROM "info"')

    async def sql_set_info(self,
                           tlf,
                           full_name,
                           operating_mode,
                           delivery):
        with self.con:
            return self.cur.execute('UPDATE "info" SET '
                                    '"telefon"=?,'
                                    ' "full_name"=?,'
                                    ' "operating_mode"=?,'
                                    ' "delivery"=?'
                                    ' WHERE id=1;',
                                    (tlf, full_name, operating_mode, delivery))

    async def sql_set_new_like(self, id_product, like=None, dislike=None, heard=None):
        with self.con:
            return self.cur.execute('UPDATE "product" SET '
                                    '"like"=?,'
                                    ' "dislike"=?,'
                                    ' "heard"=?'
                                    ' WHERE id=?;',
                                    (like, dislike, heard, id_product))

    async def sql_get_like(self, id_product):
        with self.con:
            return self.cur.execute(f'SELECT "like", "dislike", "heard" from "product" WHERE "id"={id_product}')

    async def sql_add_cart_and_customer(self, id_product, id_customer):
        with self.con:
            self.cur.execute("""INSERT INTO customer (id, date) VALUES (?, ?)""",
                             (id_customer, datetime.now()))
            self.cur.execute("""INSERT INTO prod_cust (prodict_id, customer_id) VALUES (?, ?)""",
                             (id_product, id_customer))

    async def sql_add_cart_only(self, id_product, id_customer):
        with self.con:
            self.cur.execute("""INSERT INTO prod_cust (prodict_id, customer_id) VALUES (?, ?)""",
                             (id_product, id_customer))

    async def sql_get_cart_count_customer(self, id_customer):
        with self.con:
            return self.cur.execute(f"""SELECT c2.id, COUNT(pc.prodict_id) as count from customer c2 JOIN 
            prod_cust pc on c2.id = pc.customer_id WHERE c2.id = {id_customer} GROUP BY c2.id """)


def main():
    import asyncio
    sql_obj = SQLighter('db.db')
    res = asyncio.run(sql_obj.sql_get_info())
    print(res["id"])


if __name__ == '__main__':
    main()
