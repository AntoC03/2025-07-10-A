from database.DB_connect import DBConnect
from model.prodotti import Prodotto


class DAO:

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()
        if conn is None:
            print("Connessione fallita")
        else:
            results = []

            cursor = conn.cursor(dictionary=True)
            query = "SELECT distinct (order_date) from orders o order by order_date"

            cursor.execute(query)

            for row in cursor:
                results.append(row["order_date"])

            first = results[0]
            last = results[-1]

            cursor.close()
            conn.close()
        return first, last

    @staticmethod
    def get_product():
        cnx = DBConnect.get_connection()
        a = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query1 = """SELECT DISTINCT category_name as pn
                           FROM categories
                        """
            cursor.execute(query1)
            for row in cursor:
                a.append(row["pn"])
            cursor.close()
            cnx.close()
        return a


    @staticmethod
    def get_prodotti(categoria, data1, data2):

        cnx = DBConnect.get_connection()
        a = []

        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query1 = """SELECT p.*
                        FROM products p, categories c
                        WHERE c.category_id = p.category_id and c.category_name = %s"""
            cursor.execute(query1, (categoria,))
            for row in cursor:
                a.append(Prodotto(**row))


            query2 = """SELECT p.*, count(*) as num_vendite
                        FROM products p, order_items oi, orders o, categories c
                        WHERE p.product_id = oi.product_id AND oi.order_id = o.order_id AND p.category_id = c.category_id AND category_name = %s and (DATE(order_date) BETWEEN %s AND %s)
                        group by  p.product_id"""
            cursor.execute(query2, (categoria, data1, data2,))
            rows = list(cursor)
            for i in a:
                for row in rows:
                    if i.product_id == row["product_id"]:
                        i.num_vendite = row["num_vendite"]


            cursor.close()
            cnx.close()
        return a


if __name__ == '__main__':
    DAO = DAO()
    print(DAO.get_prodotti("Road Bikes", "2016-01-01", "2018-12-28"))